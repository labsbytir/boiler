// SPDX-License-Identifier: Apache-2.0
// Copyright (c) 2026 labsbytir. All rights reserved.

import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "builder-repo",
  description: "Production-grade agentic monorepo template featuring Next.js 15, autonomous loop protocols, and self-hosted AI gateway observability.",
  openGraph: {
    title: "builder-repo",
    description: "Production-grade agentic monorepo template featuring Next.js 15, autonomous loop protocols, and self-hosted AI gateway observability.",
    images: [{ url: "/social-share.png", width: 1200, height: 630, alt: "builder-repo Social Share" }],
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "builder-repo",
    description: "Production-grade agentic monorepo template featuring Next.js 15, autonomous loop protocols, and self-hosted AI gateway observability.",
    images: ["/social-share.png"],
    creator: "@tirlabs",
  },
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
