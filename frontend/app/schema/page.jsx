// frontend/app/page.tsx
import AgentConfigForm from "../components/AgentConfigForm";

export default function Home() {
    return (
        <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-[#0d0d0d]">
            <div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm lg:flex flex-col">
                <h1 className="text-4xl font-extrabold mb-8 text-white">
                    Tesla AI Agent 训练营
                </h1>
                <p className="text-slate-600 mb-12 text-lg">
                    Day 40: 高级表单处理 - 正在配置你的数字员工
                </p>
                
                {/* 这里就是挂载点 */}
                <section className="bg-white p-8 rounded-2xl shadow-xl border border-slate-200 w-full max-w-md">
                    <AgentConfigForm />
                </section>
            </div>
        </main>
    );
}