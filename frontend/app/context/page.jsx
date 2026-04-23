
// 挂载发射塔 (Provider Injection)

import { SessionProvider } from "../lib/contexts/SessionContext";
import AgentConfigForm from "../components/AgentConfigForm";
import DiagnosticDisplay from "../components/DiagnosticDisplay"; // 我们等下创建这个

export default function Home() {
    return (
        <main className="p-24 bg-slate-900 min-h-screen text-white">
        {/* 核心：用 Provider 包裹住所有需要共享数据的组件 */}
            <SessionProvider>
                <h1 className="text-3xl font-bold mb-10">Tesla AI 工程看板</h1>
                
                <div className="grid grid-cols-2 gap-10">
                    {/* 左边是表单（改数据的工具） */}
                    <section className="bg-slate-800 p-6 rounded-xl">
                        <h2 className="mb-4 text-xl">配置 Agent</h2>
                        <AgentConfigForm />
                    </section>

                    {/* 右边是显示器（看状态的黑板） */}
                    <section className="bg-slate-800 p-6 rounded-xl border border-blue-500/30">
                        <h2 className="mb-4 text-xl">实时诊断状态</h2>
                        <DiagnosticDisplay />
                    </section>
                </div>
            </SessionProvider>
        </main>
    );
}