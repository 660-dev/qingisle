import { betterAuth } from "better-auth";
import { prismaAdapter } from "better-auth/adapters/prisma";
import { nextCookies } from "better-auth/next-js";
import { prisma } from "@/lib/prisma";
import { cloneGuideTemplates } from "@/lib/onboard";

export const auth = betterAuth({
  database: prismaAdapter(prisma, {
    provider: "postgresql",
  }),
  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8,
  },
  databaseHooks: {
    user: {
      create: {
        after: async (user) => {
          try {
            await cloneGuideTemplates(user.id);
          } catch (e) {
            console.error("[onboard] clone guide failed:", e);
          }
        },
      },
    },
  },
  session: {
    cookieCache: {
      enabled: false,
    },
  },
  advanced: {
    useSecureCookies: false,
    defaultCookieAttributes: {
      sameSite: "lax",
      secure: false,
      path: "/",
    },
  },
  trustedOrigins: [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://localhost:3100",
    "http://127.0.0.1:3100",
    "http://127.0.0.1:3000",
    process.env.BETTER_AUTH_URL ?? "",
  ].filter(Boolean),
  plugins: [nextCookies()],
});
