import type { Metadata } from "next";

// 1. 依然是这个页面的专属“电子条形码标签”
export const metadata: Metadata = {
  title: "雷达传感器异常诊断中心",
  description: "Day 55 实验：用于测试内网搜索引擎对故障页面的元数据索引效率。",
};

// 2. 使用 Tailwind CSS 重新打磨的暗黑科技风界面
export default function SeoTestPage() {
  return (
    <div className="min-h-screen bg-black text-white p-10 font-sans flex flex-col justify-center items-center">
      <div className="max-w-2xl w-full border border-zinc-8xl border-zinc-800 bg-zinc-900/50 p-8 rounded-xl backdrop-blur-md shadow-2xl">
        
        {/* 标题区域：带有一点特斯拉红的警告感 */}
        <div className="flex items-center gap-3 border-b border-zinc-8xl border-zinc-800 pb-4 mb-6">
          <span className="animate-pulse flex h-3 w-3 rounded-full bg-red-500" />
          <h1 className="text-2xl font-bold tracking-wider text-red-500">
            ⚙️ TESLA 实时雷达监控模拟端
          </h1>
        </div>

        {/* 核心状态提示 */}
        <p className="text-zinc-400 text-base mb-6 leading-relaxed">
          当前页面已成功加装强类型元数据（Metadata API），正在接受企业内网搜索引擎的实时拓扑索引。
        </p>

        {/* 实验目标面板 */}
        <div className="bg-zinc-950 border border-zinc-800 p-6 rounded-lg">
          <h2 className="text-zinc-200 font-semibold mb-3 tracking-wide">
            🎯 大厂级全栈实验观察点：
          </h2>
          <ul className="space-y-3 text-sm text-zinc-400 list-disc list-inside">
            <li>
              抬头看浏览器标签栏，确认标题已自动触发模板拼接，变成：
              <span className="text-emerald-400 font-mono block mt-1 ml-5">
                雷达传感器异常诊断中心 | TESLA STUDY OS
              </span>
            </li>
            <li>
              右键点击网页空白处选择 <span className="text-zinc-200 underline decoration-zinc-600">“查看网页源代码”</span>。
            </li>
            <li>
              在顶部的 <code className="text-zinc-300 font-mono bg-zinc-900 px-1 py-0.5 rounded">&lt;head&gt;</code> 标签内，检查爬虫规则与关键词是否被无缝编译为标准的 HTML Meta 标签。
            </li>
          </ul>
        </div>

        {/* 底部小字注脚 */}
        <div className="mt-6 text-right">
          <span className="text-xs text-zinc-600 font-mono">
            STATUS: SECURE INTERPRETED // DAY 55
          </span>
        </div>

      </div>
    </div>
  );
}