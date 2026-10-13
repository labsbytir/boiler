// SPDX-License-Identifier: Apache-2.0
// Copyright (c) 2026 TIR Labs. All rights reserved.

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

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
  const { name } = request.params;
  const args = (request.params.arguments ?? {}) as Record<string, any>;

  try {
    switch (name) {
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
        const text = String(args.proposedChanges ?? "").toLowerCase();
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
