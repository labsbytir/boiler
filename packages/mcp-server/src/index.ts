// SPDX-License-Identifier: Apache-2.0
// Copyright (c) 2026 TIR Labs. All rights reserved.

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { exec } from "child_process";
import { promisify } from "util";
import fs from "fs/promises";
import path from "path";

const execAsync = promisify(exec);
const REPO_ROOT = process.env.REPO_ROOT || process.cwd();

const server = new Server(
  {
    name: "builder-repo-mcp",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Register Available Tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "preflight_check",
        description:
          "Runs the deterministic 4-stage quality gate (Typecheck → Lint → Test → Audit). Halts on first failure.",
        inputSchema: {
          type: "object",
          properties: {
            doctor: {
              type: "boolean",
              description: "If true, previews the plan without executing.",
              default: false,
            },
          },
        },
      },
      {
        name: "get_loop_state",
        description: "Reads the current contents and status from LOOP_STATE.md.",
        inputSchema: {
          type: "object",
          properties: {},
        },
      },
      {
        name: "update_loop_state",
        description:
          "Records a completed bounded action, exit code, and next step in LOOP_STATE.md.",
        inputSchema: {
          type: "object",
          properties: {
            passNumber: { type: "number", description: "Current iteration pass number" },
            actionTaken: { type: "string", description: "Summary of single bounded change" },
            targetFiles: { type: "string", description: "Path to modified files" },
            exitCode: { type: "number", description: "0 for pass, 1 for fail" },
            nextStep: { type: "string", description: "Next immediate subtask" },
            diagnostic: { type: "string", description: "Optional diagnostic error snippet" },
          },
          required: ["passNumber", "actionTaken", "targetFiles", "exitCode", "nextStep"],
        },
      },
      {
        name: "get_repo_map",
        description:
          "Returns the verified directory structure, conventions, and pinned tech stack.",
        inputSchema: {
          type: "object",
          properties: {},
        },
      },
      {
        name: "ponytail_audit",
        description:
          "Evaluates a proposed diff or task against Ponytail YAGNI principles (detects unnecessary dependencies or speculative wrappers).",
        inputSchema: {
          type: "object",
          properties: {
            proposedChanges: {
              type: "string",
              description: "Summary or code snippet of the proposed change",
            },
          },
          required: ["proposedChanges"],
        },
      },
    ],
  };
});

// Handle Tool Execution
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case "preflight_check": {
        const cmd = args?.doctor ? "pre-flight-check doctor" : "pre-flight-check run";
        try {
          const { stdout, stderr } = await execAsync(cmd, { cwd: REPO_ROOT });
          return {
            content: [{ type: "text", text: stdout || stderr || "Quality gate passed cleanly." }],
          };
        } catch (error: any) {
          return {
            isError: true,
            content: [{ type: "text", text: error.stdout || error.stderr || error.message }],
          };
        }
      }

      case "get_loop_state": {
        const filePath = path.join(REPO_ROOT, "LOOP_STATE.md");
        const content = await fs.readFile(filePath, "utf-8");
        return {
          content: [{ type: "text", text: content }],
        };
      }

      case "update_loop_state": {
        const filePath = path.join(REPO_ROOT, "LOOP_STATE.md");
        const statusEmoji = args.exitCode === 0 ? "✅ Exit 0 (Passed)" : "❌ Exit 1 (Failed)";
        const logEntry = `\n| ${args.passNumber} | ${args.actionTaken} | \`${args.targetFiles}\` | ${statusEmoji} | Recorded |`;

        let current = await fs.readFile(filePath, "utf-8");
        current += logEntry;
        if (args.diagnostic) {
          current += `\n\n### Evidence (Pass ${args.passNumber}):\n\`\`\`\n${args.diagnostic}\n\`\`\``;
        }
        await fs.writeFile(filePath, current, "utf-8");

        return {
          content: [{ type: "text", text: `LOOP_STATE.md successfully updated for pass ${args.passNumber}.` }],
        };
      }

      case "get_repo_map": {
        const map = `
apps/web/               - Next.js 15 (App Router), React 19, Tailwind CSS v4
apps/docs/              - Quartz v4 static documentation site
services/api-python/    - Python 3.12 headless service (uv)
services/api-php/       - PHP 8.3 headless service (composer)
tests/e2e/              - Playwright E2E test specs
packages/mcp-server/    - Model Context Protocol server
.githooks/pre-push      - Pre-flight quality gate hook
        `;
        return {
          content: [{ type: "text", text: map.trim() }],
        };
      }

      case "ponytail_audit": {
        const text = String(args.proposedChanges).toLowerCase();
        const warnings: string[] = [];

        if (text.includes("axios")) warnings.push("VIOLATION: axios is banned. Use native fetch.");
        if (text.includes("lodash")) warnings.push("VIOLATION: lodash is banned. Use modern JavaScript.");
        if (text.includes("moment")) warnings.push("VIOLATION: moment is banned. Use native Intl/Date.");
        if (text.includes("wrapper") || text.includes("factory")) {
          warnings.push("WARNING: Potential speculative abstraction detected. Keep code minimal.");
        }

        const report = warnings.length > 0
          ? `❌ Ponytail Audit Failed:\n- ${warnings.join("\n- ")}`
          : "✅ Ponytail Audit Passed: Minimal, YAGNI-compliant change.";

        return {
          content: [{ type: "text", text: report }],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error: any) {
    return {
      isError: true,
      content: [{ type: "text", text: `Error executing ${name}: ${error.message}` }],
    };
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("builder-repo MCP Server running on stdio");
}

main().catch((err) => {
  console.error("Fatal error starting MCP Server:", err);
  process.exit(1);
});
