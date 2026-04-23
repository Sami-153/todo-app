"use client";

import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import { seedPosts } from "@/lib/seed-posts";
import { CreatePostPayload, PoetryPost, PostType } from "@/lib/types";

type PoetryState = {
  posts: PoetryPost[];
  createPost: (payload: CreatePostPayload) => void;
  toggleLike: (id: string) => void;
  toggleSave: (id: string) => void;
  sharePost: (id: string) => void;
  removePost: (id: string) => void;
  getPostById: (id: string) => PoetryPost | undefined;
  getPostsByType: (type: PostType | "all") => PoetryPost[];
};

const sortByNewest = (posts: PoetryPost[]) =>
  [...posts].sort(
    (a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime(),
  );

export const usePoetryStore = create<PoetryState>()(
  persist(
    (set, get) => ({
      posts: sortByNewest(seedPosts),
      createPost: (payload) =>
        set((state) => {
          const nextPost: PoetryPost = {
            id: crypto.randomUUID(),
            createdAt: new Date().toISOString(),
            likes: 0,
            shares: 0,
            isLiked: false,
            isSaved: false,
            ...payload,
          };

          return {
            posts: sortByNewest([nextPost, ...state.posts]),
          };
        }),
      toggleLike: (id) =>
        set((state) => ({
          posts: state.posts.map((post) =>
            post.id === id
              ? {
                  ...post,
                  isLiked: !post.isLiked,
                  likes: post.isLiked ? Math.max(0, post.likes - 1) : post.likes + 1,
                }
              : post,
          ),
        })),
      toggleSave: (id) =>
        set((state) => ({
          posts: state.posts.map((post) =>
            post.id === id ? { ...post, isSaved: !post.isSaved } : post,
          ),
        })),
      sharePost: (id) =>
        set((state) => ({
          posts: state.posts.map((post) =>
            post.id === id ? { ...post, shares: post.shares + 1 } : post,
          ),
        })),
      removePost: (id) =>
        set((state) => ({
          posts: state.posts.filter((post) => post.id !== id),
        })),
      getPostById: (id) => get().posts.find((post) => post.id === id),
      getPostsByType: (type) => {
        const posts = get().posts;
        return type === "all" ? posts : posts.filter((post) => post.type === type);
      },
    }),
    {
      name: "poetry-posts-store",
      storage: createJSONStorage(() => localStorage),
      version: 1,
    },
  ),
);
