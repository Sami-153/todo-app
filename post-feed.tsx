"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { Search } from "lucide-react";
import { motion } from "framer-motion";
import { PostType } from "@/lib/types";
import { usePoetryStore } from "@/store/use-poetry-store";
import { PostCard } from "@/components/feed/post-card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

const typeFilters: Array<{ label: string; value: "all" | PostType }> = [
  { label: "سب", value: "all" },
  { label: "متن", value: "text" },
  { label: "تصویر", value: "image" },
  { label: "ویڈیو", value: "video" },
];

const PAGE_SIZE = 8;

export function PostFeed() {
  const posts = usePoetryStore((state) => state.posts);
  const [query, setQuery] = useState("");
  const [type, setType] = useState<"all" | PostType>("all");
  const [visibleCount, setVisibleCount] = useState(PAGE_SIZE);
  const sentinelRef = useRef<HTMLDivElement | null>(null);

  const filteredPosts = useMemo(() => {
    return posts.filter((post) => {
      const matchesType = type === "all" || post.type === type;
      const text = [post.title, post.content, post.caption, post.overlayText]
        .join(" ")
        .toLowerCase();
      const matchesQuery = text.includes(query.toLowerCase().trim());
      return matchesType && matchesQuery;
    });
  }, [posts, query, type]);

  useEffect(() => {
    const node = sentinelRef.current;
    if (!node) {
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          setVisibleCount((prev) => Math.min(prev + PAGE_SIZE, filteredPosts.length));
        }
      },
      { rootMargin: "200px" },
    );

    observer.observe(node);
    return () => observer.disconnect();
  }, [filteredPosts.length]);

  const visiblePosts = filteredPosts.slice(0, visibleCount);

  return (
    <section className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45 }}
        className="portal-card p-4"
      >
        <div className="flex flex-col gap-4 sm:flex-row">
          <div className="relative flex-1">
            <Search className="pointer-events-none absolute right-3 top-1/2 size-4 -translate-y-1/2 text-zinc-500" />
            <Input
              value={query}
              onChange={(event) => {
                setQuery(event.target.value);
                setVisibleCount(PAGE_SIZE);
              }}
              placeholder="شاعری، کیپشن یا احساس تلاش کریں..."
              className="pr-10"
            />
          </div>
          <div className="flex flex-wrap items-center gap-2">
            {typeFilters.map((item) => (
              <Button
                key={item.value}
                variant={type === item.value ? "default" : "soft"}
                size="sm"
                onClick={() => {
                  setType(item.value);
                  setVisibleCount(PAGE_SIZE);
                }}
              >
                {item.label}
              </Button>
            ))}
          </div>
        </div>
      </motion.div>

      {visiblePosts.length > 0 ? (
        <div className="grid gap-4 lg:grid-cols-[1.8fr_1fr]">
          <div className="space-y-4">
            <div className="portal-card p-4">
              <h2 className="text-2xl font-semibold">تازہ اردو شاعری</h2>
            </div>
            <div className="columns-1 gap-4 md:columns-2">
              {visiblePosts.map((post, index) => (
                <PostCard key={post.id} post={post} index={index} />
              ))}
            </div>
          </div>

          <aside className="space-y-4">
            <div className="portal-card p-4">
              <h3 className="text-xl font-semibold">آج کا لفظ</h3>
              <p className="mt-2 text-2xl">تخلیق</p>
              <p className="mt-2 text-sm text-zinc-700 dark:text-zinc-300">
                معنی: نئی چیز کو وجود دینا، شعر یا خیال کو لفظوں میں ڈھالنا۔
              </p>
            </div>

            <div className="portal-card p-4">
              <h3 className="text-xl font-semibold">مشہور شعرا</h3>
              <ul className="mt-3 space-y-2 text-sm text-zinc-700 dark:text-zinc-300">
                <li>مرزا غالب</li>
                <li>فیض احمد فیض</li>
                <li>احمد فراز</li>
                <li>پروین شاکر</li>
                <li>جون ایلیا</li>
              </ul>
            </div>

            <div className="portal-card p-4">
              <h3 className="text-xl font-semibold">موضوعاتی شاعری</h3>
              <div className="mt-3 flex flex-wrap gap-2">
                {["محبت", "اداسی", "صوفی", "دو مصرعے", "سماجی", "اسلامی"].map((topic) => (
                  <span
                    key={topic}
                    className="rounded-md border bg-white/80 px-2.5 py-1 text-xs dark:bg-zinc-900"
                  >
                    {topic}
                  </span>
                ))}
              </div>
            </div>
          </aside>
        </div>
      ) : (
        <div className="portal-card border-dashed p-10 text-center text-zinc-600 dark:text-zinc-300">
          کوئی پوسٹ نہیں ملی، تلاش یا فلٹر تبدیل کریں۔
        </div>
      )}

      <div ref={sentinelRef} />
    </section>
  );
}
