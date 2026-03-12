import "./globals.css";
import type { ReactNode } from "react";

export const metadata = {
  title: "Blaze Media Host Popularity Desk",
  description: "Editorial-style internal dashboard for Blaze Media host popularity and sentiment tracking",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
