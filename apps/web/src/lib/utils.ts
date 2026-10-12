// SPDX-License-Identifier: Apache-2.0
// Copyright (c) 2026 labsbytir. All rights reserved.

import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}
