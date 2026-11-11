"use server";

import { headers } from "next/headers";
import { redirect } from "next/navigation";
import { auth } from "@/lib/auth";

export type AuthFormState = {
  ok: boolean;
  message: string;
} | null;

export async function loginAction(
  _prev: AuthFormState,
  formData: FormData,
): Promise<AuthFormState> {
  const email = String(formData.get("email") || "")
    .trim()
    .toLowerCase();
  const password = String(formData.get("password") || "");
  if (!email || !password) {
    return { ok: false, message: "请输入邮箱和密码" };
  }
  try {
    await auth.api.signInEmail({
      body: { email, password },
      headers: await headers(),
    });
  } catch (error) {
    const message = error instanceof Error ? error.message : "登录失败";
    if (message.toLowerCase().includes("invalid")) {
      return { ok: false, message: "邮箱或密码错误" };
    }
    return { ok: false, message: message || "登录失败，请重试" };
  }
  redirect("/dashboard");
}

export async function registerAction(
  _prev: AuthFormState,
  formData: FormData,
): Promise<AuthFormState> {
  const name = String(formData.get("name") || "").trim();
  const email = String(formData.get("email") || "")
    .trim()
    .toLowerCase();
  const password = String(formData.get("password") || "");
  const confirm = String(formData.get("confirm") || "");
  if (password !== confirm) {
    return { ok: false, message: "两次输入的密码不一致" };
  }
  if (password.length < 8) {
    return { ok: false, message: "密码至少需要 8 位" };
  }
  try {
    await auth.api.signUpEmail({
      body: { name, email, password },
      headers: await headers(),
    });
    await auth.api.signInEmail({
      body: { email, password },
      headers: await headers(),
    });
  } catch (error) {
    const message = error instanceof Error ? error.message : "注册失败";
    const lower = message.toLowerCase();
    if (lower.includes("exist")) {
      return { ok: false, message: "该邮箱已注册，请直接登录" };
    }
    return { ok: false, message: message || "注册失败，请重试" };
  }
  redirect("/dashboard");
}
