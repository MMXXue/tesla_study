
"use client";

import { useSession } from "../lib/contexts/SessionContext";

export default function DiagnosticDisplay() {
  // 1. 拿起对讲机，调到我们定义的频道
    const { status, setStatus, lastChecked } = useSession();

    // 2. 为了演示“状态切换”，我们写一个简单的处理函数
    const handleToggle = () => {
        if (status === "idle") {
            setStatus("scanning");
        } else if (status === "scanning") {
            setStatus("completed");
        } else {
            setStatus("idle");
        }
    };

    return (
        <div className="p-4 rounded-lg border border-slate-700 bg-slate-800/50">
            <div className="flex flex-col gap-3">
                {/* 状态展示 */}
                <div className="flex justify-between items-center">
                    <span className="text-slate-400 text-sm">System Status:</span>
                    <span className={`font-mono font-bold px-2 py-0.5 rounded text-xs ${
                        status === 'completed' ? 'bg-green-500/20 text-green-400' : 
                        status === 'scanning' ? 'bg-blue-500/20 text-blue-400' : 'bg-slate-700 text-slate-300'
                    }`}>
                        {status.toUpperCase()}
                    </span>
                </div>

                {/* 时间戳展示 */}
                <div className="flex justify-between items-center border-t border-slate-700 pt-3">
                    <span className="text-slate-400 text-sm">Last Checked:</span>
                    <span className="text-slate-200 text-sm font-mono">{lastChecked}</span>
                </div>

                {/* 模拟按钮：改变 Context 状态 */}
                <button
                onClick={handleToggle}
                className="mt-4 w-full py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-md text-sm transition-colors"
                >
                    {status === "idle" ? "Start Scan" : status === "scanning" ? "Finish Scan" : "Reset System"}
                </button>
            </div>
        </div>
    );
}