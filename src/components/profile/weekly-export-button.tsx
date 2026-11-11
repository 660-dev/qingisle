"use client";

import { useState } from "react";

export function WeeklyExportButton() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function exportReport() {
    setLoading(true);
    setError("");
    try {
      const res = await fetch("/api/reports/weekly?format=md");
      if (res.status === 401) {
        setError("请先登录");
        return;
      }
      if (!res.ok) {
        setError("导出失败，请稍后重试");
        return;
      }
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      const stamp = new Date().toISOString().slice(0, 10);
      a.href = url;
      a.download = `qingisle-weekly-${stamp}.md`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    } catch {
      setError("网络异常");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col items-end gap-1">
      <button
        type="button"
        onClick={exportReport}
        disabled={loading}
        className="rounded-md border border-white/12 bg-white/[0.04] px-3 py-1.5 text-xs text-white/80 transition hover:bg-white/[0.08] disabled:opacity-50"
      >
        {loading ? "正在生成…" : "导出本周周报"}
      </button>
      {error ? <p className="text-[11px] text-red-300/80">{error}</p> : null}
    </div>
  );
}
