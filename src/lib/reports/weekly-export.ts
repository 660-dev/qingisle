import { prisma } from "@/lib/prisma";
import { observe, fallbackAnalysis } from "@/lib/agent/runtime";
import { generateWeeklyReport, formatReportAsMarkdown } from "@/lib/agent/report";

export function getWeekRange(now = new Date()) {
  const weekStart = new Date(now);
  weekStart.setDate(now.getDate() - ((now.getDay() + 6) % 7));
  weekStart.setHours(0, 0, 0, 0);
  const weekEnd = new Date(now);
  weekEnd.setHours(23, 59, 59, 999);
  return { weekStart, weekEnd };
}

export async function buildWeeklyExport(userId: string, userName?: string | null) {
  const { weekStart, weekEnd } = getWeekRange();
  const context = await observe(userId);
  const analysis = fallbackAnalysis(context);
  const report = generateWeeklyReport({
    userId,
    context,
    analysis,
    weekStart: weekStart.toISOString().slice(0, 10),
    weekEnd: weekEnd.toISOString().slice(0, 10),
  });

  const [checkins, focusRecords, doneTasks] = await Promise.all([
    prisma.checkin.findMany({
      where: { userId, checkinDate: { gte: weekStart, lte: weekEnd } },
      select: { checkinDate: true, hours: true, content: true, subject: true },
      orderBy: { checkinDate: "asc" },
    }),
    prisma.studyRecord.findMany({
      where: { userId, date: { gte: weekStart, lte: weekEnd } },
      select: { date: true, totalMinutes: true, subject: true },
      orderBy: { date: "asc" },
    }),
    prisma.planTask.findMany({
      where: { userId, status: "done", completedAt: { gte: weekStart, lte: weekEnd } },
      select: { title: true, completedAt: true },
      orderBy: { completedAt: "asc" },
    }),
  ]);

  const checkinHours = checkins.reduce((s, c) => s + (c.hours || 0), 0);
  const focusMinutes = focusRecords.reduce((s, r) => s + (r.totalMinutes || 0), 0);
  const generated = formatReportAsMarkdown(report);

  const extra = [
    `# 青屿周报`,
    ``,
    `导出时间：${new Date().toISOString().slice(0, 16).replace("T", " ")}`,
    `学习者：${userName || "同学"}`,
    `统计区间：${weekStart.toISOString().slice(0, 10)} ~ ${weekEnd.toISOString().slice(0, 10)}`,
    ``,
    `## 本周数据`,
    ``,
    `- 打卡次数：${checkins.length}`,
    `- 打卡时长：${checkinHours.toFixed(1)} 小时`,
    `- 专注记录：${Math.round(focusMinutes)} 分钟`,
    `- 完成任务：${doneTasks.length} 项`,
    ``,
    generated,
    ``,
    `## 打卡明细`,
    ``,
    ...(checkins.length
      ? checkins.map((c) => {
          const day = c.checkinDate.toISOString().slice(0, 10);
          const subject = c.subject ? ` · ${c.subject}` : "";
          const text = (c.content || "").replace(/\s+/g, " ").slice(0, 80);
          return `- ${day}${subject} · ${c.hours || 0}h${text ? ` · ${text}` : ""}`;
        })
      : ["- 本周还没有打卡记录"]),
    ``,
    `## 完成任务`,
    ``,
    ...(doneTasks.length
      ? doneTasks.map((t) => `- ${t.title}`)
      : ["- 本周还没有完成任务"]),
    ``,
    `---`,
    `由青屿 QingIsle 导出。`,
  ].join("\n");

  return {
    markdown: extra,
    weekStart: weekStart.toISOString().slice(0, 10),
    weekEnd: weekEnd.toISOString().slice(0, 10),
    stats: {
      checkins: checkins.length,
      checkinHours,
      focusMinutes,
      doneTasks: doneTasks.length,
    },
  };
}
