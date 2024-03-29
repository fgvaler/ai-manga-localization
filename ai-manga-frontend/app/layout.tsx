import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-sans",
});

export const metadata: Metadata = {
  title: "Create Next App",
  description: "Generated by create next app",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={cn("h-screen min-w-[600px] max-h-[800px] font-sans antialiased bg-yellow-300 border-solid border-2 border-sky-500", inter.variable)}
      >
        {children}
      </body>
    </html>
  );
}
