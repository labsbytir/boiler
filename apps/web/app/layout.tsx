// SPDX-License-Identifier: Apache-2.0
// Copyright (c) 2026 labsbytir. All rights reserved.

import "./globals.css";

export const metadata = {
  title: "labsbytir | builder-repo",
  description: "High-performance headless web platform on Next.js 15 & Cloudflare CDN",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
