"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { BookMarked, MoonStar, PenSquare, Sparkles, UserRound } from "lucide-react";
import { useThemeMode } from "@/components/providers/theme-provider";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const links = [
  { href: "/", label: "صفحہ اول", icon: Sparkles },
  { href: "/create", label: "بنائیں", icon: PenSquare },
  { href: "/profile", label: "پروفائل", icon: UserRound },
];

const quickSections = ["غزل", "نظم", "دو مصرعے", "محبت", "اداسی", "نئے شعرا"];

export function TopNav({ pathname }: { pathname: string }) {
  const { toggleMode } = useThemeMode();

  return (
    <motion.header
      initial={{ opacity: 0, y: -14 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      className="sticky top-0 z-30 border-b bg-[color:var(--surface)]/95 backdrop-blur-sm"
    >
      <div className="mx-auto flex w-full max-w-6xl items-center justify-between gap-3 px-3 py-3 sm:px-4">
        <Link href="/" className="flex items-center gap-2 text-lg font-semibold tracking-wide sm:text-xl">
          <BookMarked className="size-5" />
          Naeem Writes
        </Link>

        <nav className="hidden items-center gap-2 rounded-full border bg-white/60 p-1 shadow-sm md:flex dark:bg-zinc-900/70">
          {links.map(({ href, label, icon: Icon }) => {
            const active = pathname === href;
            return (
              <Link key={href} href={href}>
                <span
                  className={cn(
                    "inline-flex items-center gap-2 rounded-full px-3 py-2 text-sm transition",
                    active
                      ? "bg-zinc-900 text-zinc-50 dark:bg-zinc-100 dark:text-zinc-900"
                      : "text-zinc-700 hover:bg-zinc-200/70 dark:text-zinc-300 dark:hover:bg-zinc-800",
                  )}
                >
                  <Icon className="size-4" />
                  <span className="hidden sm:inline">{label}</span>
                </span>
              </Link>
            );
          })}
        </nav>

        <Button variant="soft" size="sm" onClick={toggleMode} className="gap-2">
          <MoonStar className="size-4" />
          <span className="hidden sm:inline">تھیم</span>
        </Button>
      </div>

      <div className="mx-auto flex w-full max-w-6xl flex-wrap items-center gap-2 px-3 pb-3 sm:px-4">
        {quickSections.map((section) => (
          <span
            key={section}
            className="rounded-md border bg-white/70 px-3 py-1 text-xs text-zinc-700 dark:bg-zinc-900 dark:text-zinc-200"
          >
            {section}
          </span>
        ))}
      </div>
    </motion.header>
  );
}
