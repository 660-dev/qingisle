"use client";

import { useActionState, useState } from "react";
import Link from "next/link";
import { Sparkle, Eye, EyeSlash, ArrowRight } from "@phosphor-icons/react";
import { loginAction, type AuthFormState } from "@/app/(auth)/actions";

export default function LoginPage() {
  const [showPassword, setShowPassword] = useState(false);
  const [state, formAction, pending] = useActionState<AuthFormState, FormData>(
    loginAction,
    null,
  );

  return (
    <div className="w-full">
      <div className="mb-7">
        <div className="mb-4 inline-flex items-center gap-1.5 rounded-full border border-primary/20 bg-primary/10 px-3 py-1 text-[11px] font-medium text-primary">
          <Sparkle className="size-3" weight="fill" />
          <span>欢迎回到学习栖息地</span>
        </div>
        <h1 className="text-[28px] font-semibold leading-tight tracking-tight text-foreground">
          继续你的学习节奏
        </h1>
        <p className="mt-2 text-sm leading-6 text-muted-foreground">
          登录后，今天的计划和专注记录会接着上次继续。
        </p>
      </div>

      {state?.message ? (
        <div
          className={
            state.ok
              ? "mb-4 rounded-xl border border-emerald-500/30 bg-emerald-500/10 px-3 py-2 text-sm text-emerald-700 dark:text-emerald-300"
              : "mb-4 rounded-xl border border-red-500/30 bg-red-500/10 px-3 py-2 text-sm text-red-600 dark:text-red-300"
          }
        >
          {state.message}
        </div>
      ) : null}

      <form action={formAction} className="space-y-4">
        <div className="space-y-1.5">
          <label htmlFor="email" className="block text-xs font-medium text-foreground/70">
            邮箱地址
          </label>
          <input
            id="email"
            name="email"
            type="email"
            placeholder="you@example.com"
            autoComplete="email"
            required
            className="h-12 w-full rounded-xl border border-border/80 bg-background/40 px-4 text-sm text-foreground outline-none transition-all placeholder:text-muted-foreground/40 focus:border-primary/60 focus:bg-background/70 focus:ring-4 focus:ring-primary/10"
          />
        </div>

        <div className="space-y-1.5">
          <label htmlFor="password" className="block text-xs font-medium text-foreground/70">
            密码
          </label>
          <div className="relative">
            <input
              id="password"
              name="password"
              type={showPassword ? "text" : "password"}
              placeholder="输入密码"
              autoComplete="current-password"
              required
              minLength={8}
              className="h-12 w-full rounded-xl border border-border/80 bg-background/40 px-4 pr-11 text-sm text-foreground outline-none transition-all placeholder:text-muted-foreground/40 focus:border-primary/60 focus:bg-background/70 focus:ring-4 focus:ring-primary/10"
            />
            <button
              type="button"
              onClick={() => setShowPassword((s) => !s)}
              className="absolute right-2 top-1/2 flex h-8 w-8 -translate-y-1/2 items-center justify-center rounded-lg text-muted-foreground/60 transition-colors hover:bg-foreground/5 hover:text-foreground"
            >
              {showPassword ? <EyeSlash className="size-4" /> : <Eye className="size-4" />}
            </button>
          </div>
        </div>

        <button
          type="submit"
          disabled={pending}
          className="group relative flex h-12 w-full items-center justify-center gap-2 rounded-xl bg-primary text-sm font-semibold text-primary-foreground shadow-lg shadow-primary/20 transition-all hover:bg-primary/90 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {pending ? "登录中…" : (
            <>
              <span>登录</span>
              <ArrowRight className="size-4" weight="bold" />
            </>
          )}
        </button>
      </form>

      <p className="mt-6 text-center text-sm text-muted-foreground">
        还没有账号？
        <Link href="/register" className="ml-1 font-medium text-primary hover:underline">
          立即注册
        </Link>
      </p>
    </div>
  );
}
