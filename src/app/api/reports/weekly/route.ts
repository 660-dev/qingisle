import { NextResponse } from "next/server";
import { getAuthUser } from "@/lib/auth-utils";
import { buildWeeklyExport } from "@/lib/reports/weekly-export";

export async function GET(request: Request) {
  const user = await getAuthUser();
  if (!user) {
    return NextResponse.json({ error: "unauthorized" }, { status: 401 });
  }

  const format = new URL(request.url).searchParams.get("format") ?? "md";
  const data = await buildWeeklyExport(user.id, user.name);
  const filename = `qingisle-weekly-${data.weekEnd}.md`;

  if (format === "json") {
    return NextResponse.json(data);
  }

  return new NextResponse(data.markdown, {
    headers: {
      "Content-Type": "text/markdown; charset=utf-8",
      "Content-Disposition": `attachment; filename="${filename}"`,
      "Cache-Control": "no-store",
    },
  });
}
