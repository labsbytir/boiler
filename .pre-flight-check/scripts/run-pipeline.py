#!/usr/bin/env python3
"""Pre-Flight Check pipeline engine.

Auto-detects runtime (Node.js / Python), runs sequential fail-fast quality
gates (typecheck -> lint -> test -> security audit), and emits Markdown
output structured for LLM consumption.

Vanilla Python 3, no third-party deps.
"""

from __future__ import annotations

import argparse
import importlib
import json
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, TypedDict


MAX_CONTEXT_CHARS = 4000

# User-facing stage keys (for --only / --skip) mapped to internal stage names.
STAGE_KEYS = {
    "typecheck": "TYPECHECK",
    "lint": "LINT",
    "test": "TEST",
    "audit": "SECURITY AUDIT",
}


class Stage(TypedDict):
    name: str
    cmd: list[str]


def which(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def file_exists(cwd: Path, name: str) -> bool:
    return (cwd / name).is_file()


def detect_node_pm(cwd: Path) -> str:
    """Pick package manager based on lockfile, then availability."""
    if file_exists(cwd, "pnpm-lock.yaml") and which("pnpm"):
        return "pnpm"
    if file_exists(cwd, "yarn.lock") and which("yarn"):
        return "yarn"
    if file_exists(cwd, "package-lock.json") and which("npm"):
        return "npm"
    for pm in ("pnpm", "yarn", "npm"):
        if which(pm):
            return pm
    return "npm"


def package_json_scripts(cwd: Path) -> dict[str, str]:
    pj = cwd / "package.json"
    if not pj.is_file():
        return {}
    try:
        with pj.open("r", encoding="utf-8") as f:
            data = json.load(f)
        scripts = data.get("scripts") or {}
        if not isinstance(scripts, dict):
            return {}
        return {str(k): str(v) for k, v in scripts.items()}
    except (json.JSONDecodeError, OSError):
        return {}


def has_dep(cwd: Path, dep: str) -> bool:
    pj = cwd / "package.json"
    if not pj.is_file():
        return False
    try:
        with pj.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return False
    for key in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        block = data.get(key) or {}
        if isinstance(block, dict) and dep in block:
            return True
    return False


def pm_run(pm: str, script: str) -> list[str]:
    """Build a 'run <script>' command for the chosen package manager."""
    if pm == "npm":
        return ["npm", "run", script, "--if-present"]
    if pm == "yarn":
        return ["yarn", "run", script]
    return ["pnpm", "run", script]


def pm_exec(pm: str, binary: str, *args: str) -> list[str]:
    """Run a locally-installed binary via the package manager."""
    if pm == "npm":
        return ["npx", "--no-install", binary, *args]
    if pm == "yarn":
        return ["yarn", binary, *args]
    return ["pnpm", "exec", binary, *args]


def build_node_stages(cwd: Path) -> list[Stage]:
    pm = detect_node_pm(cwd)
    scripts = package_json_scripts(cwd)
    stages: list[Stage] = []

    # Typecheck
    if "typecheck" in scripts:
        stages.append({"name": "TYPECHECK", "cmd": pm_run(pm, "typecheck")})
    elif "type-check" in scripts:
        stages.append({"name": "TYPECHECK", "cmd": pm_run(pm, "type-check")})
    elif has_dep(cwd, "typescript") or file_exists(cwd, "tsconfig.json"):
        stages.append({"name": "TYPECHECK", "cmd": pm_exec(pm, "tsc", "--noEmit")})

    # Lint
    if "lint" in scripts:
        stages.append({"name": "LINT", "cmd": pm_run(pm, "lint")})
    elif has_dep(cwd, "eslint"):
        stages.append({"name": "LINT", "cmd": pm_exec(pm, "eslint", ".")})

    # Test — ignore the `npm init` placeholder script that always exits 1.
    test_script = scripts.get("test", "")
    if test_script and "no test specified" not in test_script:
        stages.append({"name": "TEST", "cmd": pm_run(pm, "test")})
    elif has_dep(cwd, "jest"):
        stages.append({"name": "TEST", "cmd": pm_exec(pm, "jest", "--passWithNoTests")})
    elif has_dep(cwd, "vitest"):
        stages.append({"name": "TEST", "cmd": pm_exec(pm, "vitest", "run")})

    # Security audit — requires a lockfile; npm/pnpm/yarn all error without one,
    # which would be a false failure. Skip silently when no lockfile is present.
    if pm == "npm" and file_exists(cwd, "package-lock.json"):
        stages.append({"name": "SECURITY AUDIT", "cmd": ["npm", "audit", "--audit-level=high"]})
    elif pm == "pnpm" and file_exists(cwd, "pnpm-lock.yaml"):
        stages.append({"name": "SECURITY AUDIT", "cmd": ["pnpm", "audit", "--audit-level", "high"]})
    elif pm == "yarn" and file_exists(cwd, "yarn.lock"):
        stages.append({"name": "SECURITY AUDIT", "cmd": ["yarn", "npm", "audit", "--severity", "high"]})

    return stages


def python_runner(cwd: Path) -> list[str]:
    """Prefix to invoke a tool: poetry run X / pip-installed X."""
    if file_exists(cwd, "poetry.lock") and which("poetry"):
        return ["poetry", "run"]
    if file_exists(cwd, "pyproject.toml") and which("poetry"):
        try:
            with (cwd / "pyproject.toml").open("r", encoding="utf-8") as f:
                if "[tool.poetry]" in f.read() and which("poetry"):
                    return ["poetry", "run"]
        except OSError:
            pass
    return []


def build_python_stages(cwd: Path) -> list[Stage]:
    runner = python_runner(cwd)
    stages: list[Stage] = []

    def wrap(tool: str, *args: str) -> list[str] | None:
        if runner:
            return [*runner, tool, *args]
        if which(tool):
            return [tool, *args]
        return None

    # Typecheck
    mypy_cmd = wrap("mypy", ".")
    if mypy_cmd:
        stages.append({"name": "TYPECHECK", "cmd": mypy_cmd})

    # Lint - prefer ruff, fallback flake8
    ruff_cmd = wrap("ruff", "check", ".")
    flake_cmd = wrap("flake8", ".")
    if ruff_cmd:
        stages.append({"name": "LINT", "cmd": ruff_cmd})
    elif flake_cmd:
        stages.append({"name": "LINT", "cmd": flake_cmd})

    # Test
    pytest_cmd = wrap("pytest", "-q")
    if pytest_cmd:
        stages.append({"name": "TEST", "cmd": pytest_cmd})

    # Security audit - prefer pip-audit, fallback bandit
    pip_audit = wrap("pip-audit")
    bandit_cmd = wrap("bandit", "-r", ".", "-q")
    if pip_audit:
        stages.append({"name": "SECURITY AUDIT", "cmd": pip_audit})
    elif bandit_cmd:
        stages.append({"name": "SECURITY AUDIT", "cmd": bandit_cmd})

    return stages


def build_go_stages(cwd: Path) -> list[Stage]:
    stages: list[Stage] = []
    if not which("go"):
        return stages
    # `go build ./...` compiles every package — the closest thing Go has to a
    # standalone typecheck. It emits no artifacts for library packages.
    stages.append({"name": "TYPECHECK", "cmd": ["go", "build", "./..."]})
    if which("golangci-lint"):
        stages.append({"name": "LINT", "cmd": ["golangci-lint", "run"]})
    else:
        stages.append({"name": "LINT", "cmd": ["go", "vet", "./..."]})
    stages.append({"name": "TEST", "cmd": ["go", "test", "./..."]})
    if which("govulncheck"):
        stages.append({"name": "SECURITY AUDIT", "cmd": ["govulncheck", "./..."]})
    return stages


def build_rust_stages(cwd: Path) -> list[Stage]:
    stages: list[Stage] = []
    if not which("cargo"):
        return stages
    stages.append({"name": "TYPECHECK", "cmd": ["cargo", "check", "--all-targets"]})
    if which("cargo-clippy"):
        stages.append({"name": "LINT",
                       "cmd": ["cargo", "clippy", "--all-targets", "--", "-D", "warnings"]})
    stages.append({"name": "TEST", "cmd": ["cargo", "test"]})
    if which("cargo-audit"):
        stages.append({"name": "SECURITY AUDIT", "cmd": ["cargo", "audit"]})
    return stages


def detect_runtime(cwd: Path) -> str:
    if file_exists(cwd, "package.json"):
        return "node"
    if file_exists(cwd, "go.mod"):
        return "go"
    if file_exists(cwd, "Cargo.toml"):
        return "rust"
    for sig in ("pyproject.toml", "poetry.lock", "requirements.txt", "setup.py", "setup.cfg"):
        if file_exists(cwd, sig):
            return "python"
    return "unknown"


def truncate_tail(text: str, limit: int = MAX_CONTEXT_CHARS) -> str:
    text = text.rstrip()
    if len(text) <= limit:
        return text
    return "... [truncated, showing tail] ...\n" + text[-limit:]


def cmd_to_str(cmd: list[str]) -> str:
    """Shell-ish representation of the command for display."""
    parts: list[str] = []
    for tok in cmd:
        if any(c.isspace() for c in tok) or tok == "":
            parts.append(f'"{tok}"')
        else:
            parts.append(tok)
    return " ".join(parts)


def resolve_exe(cmd: list[str]) -> list[str] | None:
    """Resolve cmd[0] to a runnable path, cross-platform.

    On Windows the Node tools (npm, npx, yarn, pnpm, tsc, eslint, …) are
    .cmd/.bat shims that CreateProcess cannot execute directly, so they are
    wrapped in the command interpreter. shutil.which() finds them via PATHEXT.
    Returns None if the executable is not on PATH.
    """
    exe = shutil.which(cmd[0])
    if exe is None:
        return None
    rest = cmd[1:]
    if os.name == "nt" and exe.lower().endswith((".cmd", ".bat")):
        comspec = os.environ.get("COMSPEC", "cmd.exe")
        return [comspec, "/c", exe, *rest]
    return [exe, *rest]


def run_stage(stage: Stage) -> tuple[int, str, str]:
    resolved = resolve_exe(stage["cmd"])
    if resolved is None:
        return 127, "", f"command not found: {stage['cmd'][0]}"
    try:
        proc = subprocess.run(
            resolved,
            capture_output=True,
            text=True,
            check=False,
        )
        return proc.returncode, proc.stdout or "", proc.stderr or ""
    except FileNotFoundError as e:
        return 127, "", f"command not found: {e}"


def emit_failure(stage_name: str, cmd: list[str], stdout: str, stderr: str, rc: int) -> None:
    context = stderr.strip() or stdout.strip() or f"(no output, exit code {rc})"
    context = truncate_tail(context)
    print(f"### ❌ PRE-FLIGHT FAILURE: {stage_name}")
    print(f"**Command Executed:** `{cmd_to_str(cmd)}`")
    print("**Context for AI Fix:**")
    print()
    print("```")
    print(context)
    print("```")


def emit_success() -> None:
    print("### ✅ PRE-FLIGHT PASSED")
    print("All quality gates verified successfully.")


def filter_stages(stages: list[Stage], only: list[str], skip: list[str]) -> list[Stage]:
    """Narrow the stage list per --only / --skip (mutually exclusive upstream)."""
    if only:
        wanted = {STAGE_KEYS[k] for k in only}
        return [s for s in stages if s["name"] in wanted]
    if skip:
        unwanted = {STAGE_KEYS[k] for k in skip}
        return [s for s in stages if s["name"] not in unwanted]
    return stages


def emit_plan(runtime: str, cwd: Path, stages: list[Stage],
              config_note: str | None = None) -> None:
    """Dry-run report: what would run, plus tool availability. Never executes."""
    print(f"# Pre-Flight Check — plan (runtime: {runtime})")
    print(f"Working dir: {cwd}")
    if config_note:
        print(f"Config: {config_note}")
    print()

    if stages:
        print("Stages that will run:")
        for s in stages:
            print(f"  ✓ {s['name']:<16} {cmd_to_str(s['cmd'])}")
    else:
        print("No stages will run.")

    # Show which relevant CLIs are present, so the user can see *why* a gate
    # was skipped. Node tool selection is dep-based, so we report the basics.
    if runtime == "python":
        relevant = ["mypy", "ruff", "flake8", "pytest", "pip-audit", "bandit"]
    elif runtime == "node":
        relevant = ["node", "npm", "pnpm", "yarn", "npx"]
    elif runtime == "go":
        relevant = ["go", "golangci-lint", "govulncheck"]
    elif runtime == "rust":
        relevant = ["cargo", "cargo-clippy", "cargo-audit"]
    else:
        relevant = []
    if relevant:
        print("\nDetected tools:")
        for tool in relevant:
            mark = "✓" if which(tool) else "✗"
            print(f"  {mark} {tool}")


def _load_toml(path: Path) -> dict[str, object]:
    """Parse a TOML file. Returns {} if tomllib is unavailable (Python < 3.11)
    or the file can't be read/parsed — config is always best-effort."""
    try:
        tomllib: Any = importlib.import_module("tomllib")
    except ModuleNotFoundError:
        return {}
    try:
        with path.open("rb") as f:
            data = tomllib.load(f)
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def load_config(cwd: Path) -> dict[str, object]:
    """Read pre-flight-check config: `.pre-flight-check.toml` (top-level keys)
    takes precedence, else `[tool.pre-flight-check]` in pyproject.toml."""
    standalone = cwd / ".pre-flight-check.toml"
    if standalone.is_file():
        return _load_toml(standalone)
    pp = cwd / "pyproject.toml"
    if pp.is_file():
        tool = _load_toml(pp).get("tool", {})
        if isinstance(tool, dict):
            cfg = tool.get("pre-flight-check", {})
            if isinstance(cfg, dict):
                return cfg
    return {}


def config_source(cwd: Path) -> str | None:
    """Human-readable name of the active config file, or None."""
    if (cwd / ".pre-flight-check.toml").is_file():
        return ".pre-flight-check.toml"
    pp = cwd / "pyproject.toml"
    if pp.is_file():
        tool = _load_toml(pp).get("tool", {})
        if isinstance(tool, dict) and isinstance(tool.get("pre-flight-check"), dict):
            return "pyproject.toml [tool.pre-flight-check]"
    return None


def apply_config(stages: list[Stage], cfg: dict[str, object]) -> list[Stage]:
    """Apply `commands` overrides and `disable` from config to the stage list.

    A `commands.<stage>` override replaces (or adds) that stage's command, even
    if auto-detection skipped it. `disable` removes stages. Canonical order is
    preserved: typecheck -> lint -> test -> audit.
    """
    commands = cfg.get("commands", {})
    disable = cfg.get("disable", [])
    if not isinstance(commands, dict):
        commands = {}
    if not isinstance(disable, list):
        disable = []

    by_name = {s["name"]: s for s in stages}
    for key, name in STAGE_KEYS.items():
        override = commands.get(key)
        if isinstance(override, str) and override.strip():
            by_name[name] = {"name": name, "cmd": shlex.split(override)}

    ordered = [STAGE_KEYS[k] for k in ("typecheck", "lint", "test", "audit")]
    disabled = {STAGE_KEYS[k] for k in disable if k in STAGE_KEYS}
    return [by_name[n] for n in ordered if n in by_name and n not in disabled]


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="run-pipeline",
        description="Pre-Flight Check engine: typecheck -> lint -> test -> audit.",
    )
    parser.add_argument(
        "--plan", "--dry-run", dest="plan", action="store_true",
        help="Show which runtime and stages would run, without executing them.",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--only", nargs="+", metavar="STAGE", choices=list(STAGE_KEYS),
        help="Run only these stages (typecheck, lint, test, audit).",
    )
    group.add_argument(
        "--skip", nargs="+", metavar="STAGE", choices=list(STAGE_KEYS),
        help="Run every stage except these.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    only: list[str] = args.only or []
    skip: list[str] = args.skip or []

    cwd = Path(os.getcwd())
    runtime = detect_runtime(cwd)

    if runtime == "node":
        stages = build_node_stages(cwd)
    elif runtime == "python":
        stages = build_python_stages(cwd)
    elif runtime == "go":
        stages = build_go_stages(cwd)
    elif runtime == "rust":
        stages = build_rust_stages(cwd)
    else:
        if args.plan:
            emit_plan("unknown", cwd, [])
            return 0
        print("### ⚠️  PRE-FLIGHT SKIPPED: UNKNOWN RUNTIME")
        print("**Context for AI Fix:** No `package.json`, `pyproject.toml`, "
              "`requirements.txt`, `go.mod`, or `Cargo.toml` found in current "
              "directory. Cannot determine project runtime.")
        return 1

    stages = apply_config(stages, load_config(cwd))
    stages = filter_stages(stages, only, skip)

    if args.plan:
        emit_plan(runtime, cwd, stages, config_source(cwd))
        return 0

    if not stages:
        print(f"### ⚠️  PRE-FLIGHT SKIPPED: NO STAGES RESOLVED ({runtime.upper()})")
        print("**Context for AI Fix:** Runtime detected but no usable tools "
              "(typecheck/lint/test/audit) were found, or all were filtered out "
              "by --only/--skip. Install dev tooling or define `scripts` in "
              "`package.json`.")
        return 1

    print(f"# Pre-Flight Check — runtime: {runtime}", flush=True)
    for stage in stages:
        name = stage["name"]
        cmd = stage["cmd"]
        print(f"\n→ [{name}] {cmd_to_str(cmd)}", flush=True)
        rc, out, err = run_stage(stage)
        if rc != 0:
            print()
            emit_failure(name, cmd, out, err, rc)
            return 1

    print()
    emit_success()
    return 0


if __name__ == "__main__":
    sys.exit(main())
