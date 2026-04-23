"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Heart, Share2, Bookmark, BookmarkCheck, Play } from "lucide-react";
import { PoetryPost } from "@/lib/types";
import { cn, formatDate } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { usePoetryStore } from "@/store/use-poetry-store";
import { useRef } from "react";

const themeClassMap: Record<string, string> = {
  mist: "from-zinc-100/90 to-slate-200/70 dark:from-zinc-900 dark:to-zinc-800",
  sunset: "from-amber-100/95 to-rose-100/85 dark:from-amber-950 dark:to-rose-950",
  noir: "from-zinc-800 to-zinc-900 text-zinc-100",
  sage: "from-emerald-100/90 to-lime-100/75 dark:from-emerald-950 dark:to-lime-950",
};

const sizeClassMap = {
  small: "min-h-48",
  medium: "min-h-60",
  large: "min-h-80",
  full: "min-h-[28rem]",
};

export function PostCard({ post, index }: { post: PoetryPost; index: number }) {
  const { toggleLike, toggleSave, sharePost } = usePoetryStore();
  const videoRef = useRef<HTMLVideoElement | null>(null);

  return (
    <motion.article
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: 0.45, ease: "easeOut", delay: index * 0.04 }}
      className="mb-4 break-inside-avoid"
    >
      <Link href={`/post/${post.id}`} className="block">
        <div
          className={cn(
            "group relative overflow-hidden rounded-2xl border bg-gradient-to-br p-4 shadow-sm transition-transform duration-300 hover:-translate-y-0.5",
            sizeClassMap[post.size],
            themeClassMap[post.theme || "mist"],
          )}
        >
          {post.type === "image" && post.mediaUrl ? (
            <div className="relative overflow-hidden rounded-2xl">
              <img
                src={post.mediaUrl}
                alt={post.title || "اردو شاعری تصویر"}
                className="h-full max-h-[32rem] w-full object-cover transition duration-500 group-hover:scale-105"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/65 via-black/25 to-transparent p-5 text-zinc-100">
                <p className="mt-auto whitespace-pre-line text-sm leading-7 tracking-wide sm:text-base">
                  {post.overlayText || post.content}
                </p>
              </div>
            </div>
          ) : null}

          {post.type === "video" && post.mediaUrl ? (
            <div className="relative overflow-hidden rounded-2xl">
              <video
                ref={videoRef}
                src={post.mediaUrl}
                muted
                loop
                playsInline
                className="h-full max-h-[30rem] w-full object-cover"
                onMouseEnter={() => videoRef.current?.play()}
                onMouseLeave={() => videoRef.current?.pause()}
              />
              <div className="absolute inset-0 flex items-center justify-center bg-black/15 opacity-0 transition group-hover:opacity-100">
                <Play className="size-12 text-white/90" />
              </div>
            </div>
          ) : null}

          {post.type === "text" ? (
            <div
              className={cn(
                "flex h-full min-h-44 flex-col justify-center gap-3",
                post.alignment === "center" && "items-center text-center",
                post.alignment === "right" && "items-end text-right",
              )}
            >
              {post.title ? <h3 className="text-lg font-semibold">{post.title}</h3> : null}
              <p className="whitespace-pre-line text-base leading-8 tracking-[0.01em]">{post.content}</p>
            </div>
          ) : null}

          {post.type !== "text" && post.caption ? (
            <p className="mt-4 text-sm leading-7 text-zinc-700 dark:text-zinc-300">{post.caption}</p>
          ) : null}

          <div className="mt-4 flex items-center justify-between border-t pt-3 text-xs text-zinc-700 dark:text-zinc-300">
            <span>{formatDate(post.createdAt)}</span>
            <div className="flex items-center gap-2" onClick={(e) => e.preventDefault()}>
              <Button
                variant="ghost"
                size="sm"
                className={cn(post.isLiked && "text-rose-500")}
                onClick={() => toggleLike(post.id)}
              >
                <Heart className="mr-1 size-4" />
                {post.likes}
              </Button>
              <Button variant="ghost" size="sm" onClick={() => toggleSave(post.id)}>
                {post.isSaved ? (
                  <BookmarkCheck className="mr-1 size-4" />
                ) : (
                  <Bookmark className="mr-1 size-4" />
                )}
                محفوظ
              </Button>
              <Button variant="ghost" size="sm" onClick={() => sharePost(post.id)}>
                <Share2 className="mr-1 size-4" />
                {post.shares}
              </Button>
            </div>
          </div>
        </div>
      </Link>
    </motion.article>
  );
}
