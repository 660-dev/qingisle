"use client";

import { useActionState } from "react";
import Link from "next/link";
import { Sparkle, ArrowRight } from "@phosphor-icons/react";
import { registerAction, type AuthFormState } from "@/app/(auth)/actions";

export default function RegisterPage() {
  const [state, formAction, pending] = useActionState<AuthFormState, FormData>(
    registerAction,
    null,
  );

  return (
    <div className="w-full">
      <Link href="/" className="mb-8 inline-flex items-center gap-2 text-sm font-semibold text-foreground lg:hidden">
        <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-primary text-primary-foreground">
          <Sparkle className="size-4" weight="fill" />
        </span>
        知序
      </Link>

      <div className="mb-8">
        <div className="mb-3 inline-flex items-center gap-1.5 rounded-full border border-primary/20 bg-primary/10 px-3 py-1 text-[11px] font-medium text-primary">
          <Sparkle className="size-3" weight="fill" />
          <span>创建账号</span>
        </div>
        <h1 className="text-[28px] font-semibold leading-tight text-foreground">建立你的学习空间</h1>
        <p className="mt-1.5 text-sm text-muted-foreground">开始记录你的成长轨迹</p>
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
          <label htmlFor="name" className="block text-xs font-medium text-muted-foreground">用户名</label>
          <input id="name" name="name" type="text" placeholder="你的名字" required className="h-11 w-full rounded-xl border border-border bg-muted/30 px-4 text-sm outline-none focus:border-primary/50 focus:ring-2 focus:ring-primary/20" />
        </div>
        <div className="space-y-1.5">
          <label htmlFor="email" className="block text-xs font-medium text-muted-foreground">邮箱</label>
          <input id="email" name="email" type="email" placeholder="you@example.com" required className="h-11 w-full rounded-xl border border-border bg-muted/30 px-4 text-sm outline-none focus:border-primary/50 focus:ring-2 focus:ring-primary/20" />
        </div>
        <div className="space-y-1.5">
          <label htmlFor="password" className="block text-xs font-medium text-muted-foreground">密码</label>
          <input id="password" name="password" type="password" placeholder="至少 8 位字符" required minLength={8} className="h-11 w-full rounded-xl border border-border bg-muted/30 px-4 text-sm outline-none focus:border-primary/50 focus:ring-2 focus:ring-primary/20" />
        </div>
        <div className="space-y-1.5">
          <label htmlFor="confirm" className="block text-xs font-medium text-muted-foreground">确认密码</label>
          <input id="confirm" name="confirm" type="password" placeholder="再次输入密码" required minLength={8} className="h-11 w-full rounded-xl border border-border bg-muted/30 px-4 text-sm outline-none focus:border-primary/50 focus:ring-2 focus:ring-primary/20" />
        </div>
        <button type="submit" disabled={pending} className="group relative mt-2 flex h-11 w-full items-center justify-center gap-2 rounded-xl bg-primary text-sm font-semibold text-primary-foreground disabled:opacity-60">
          {pending ? "注册中…" : (
            <>
              <span>注册</span>
              <ArrowRight className="size-4" weight="bold" />
            </>
          )}
        </button>
      </form>

      <p className="mt-6 text-center text-sm text-muted-foreground">
        已有账号？
        <Link href="/login" className="ml-1 font-medium text-primary hover:underline">立即登录</Link>
      </p>
    </div>
  );
}
