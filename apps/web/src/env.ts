// SPDX-License-Identifier: Apache-2.0
// Copyright (c) 2026 labsbytir. All rights reserved.

import { z } from "zod";

const envSchema = z.object({
  NODE_ENV: z.enum(["development", "test", "production"]).default("development"),
  API_BASE_URL: z.string().url().default("http://localhost:3000/api"),
  NEXT_PUBLIC_APP_URL: z.string().url().default("http://localhost:3000"),
  AI_GATEWAY_URL: z.string().url().default("https://subdomain.domain.com/v1"),
});

export const env = envSchema.parse({
  NODE_ENV: process.env.NODE_ENV,
  API_BASE_URL: process.env.API_BASE_URL,
  NEXT_PUBLIC_APP_URL: process.env.NEXT_PUBLIC_APP_URL,
  AI_GATEWAY_URL: process.env.AI_GATEWAY_URL,
});
