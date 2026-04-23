"use client";

import { usePathname } from "next/navigation";
import { TopNav } from "@/components/layout/top-nav";

export function SiteShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  return (
    <div className="flex min-h-screen flex-col">
      <TopNav pathname={pathname} />
      <main className="mx-auto flex w-full max-w-6xl flex-1 flex-col px-3 py-6 sm:px-4">{children}</main>
    </div>
  );
}
