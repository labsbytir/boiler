// SPDX-License-Identifier: Apache-2.0
// Copyright (c) 2026 TIR Labs. All rights reserved.

import { describe, it, expect } from "vitest";
import { cn } from "./utils";

describe("cn utility", () => {
  it("merges class names correctly", () => {
    expect(cn("px-2 py-1", "bg-red-500")).toBe("px-2 py-1 bg-red-500");
  });

  it("handles tailwind class conflicts", () => {
    expect(cn("p-4", "p-2")).toBe("p-2");
  });

  it("handles conditional classes", () => {
    expect(cn("text-base", false && "hidden", true && "font-bold")).toBe("text-base font-bold");
  });
});
