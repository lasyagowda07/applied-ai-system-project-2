import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PawPal AI Planner",
  description: "Local AI pet care scheduling assistant",
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