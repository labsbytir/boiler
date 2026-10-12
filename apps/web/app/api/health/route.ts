// SPDX-License-Identifier: Apache-2.0
// Copyright (c) 2026 TIR Labs. All rights reserved.

export async function GET() {
  return Response.json({
    success: true,
    data: {
      status: "healthy",
      service: "web",
      version: "1.0.0",
      runtime: "edge",
    },
    error: null,
    meta: {
      timestamp: new Date().toISOString(),
      requestId: `req_${Math.random().toString(36).substring(2, 9)}`,
    },
  }, {
    status: 200,
    headers: {
      "Cache-Control": "public, s-maxage=60, stale-while-revalidate=300",
    },
  });
}
