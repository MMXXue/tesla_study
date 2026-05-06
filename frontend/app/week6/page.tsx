'use client';

import RoleContainer from './components/RoleContainer'; // 确保路径指向你保存 RoleContainer 的位置
import { useRoleStore, Role } from './store/useRoleStore';

export default function TeslaDashboardPage() {
    // 从 Store 中获取当前角色和设置角色的函数
    const { role, setRole } = useRoleStore();

    // 核心逻辑：循环切换角色 (Agent -> Admin -> Maintainer)
    const handleToggle = () => {
        const roleSequence: Role[] = ['Agent', 'Admin', 'Maintainer'];
        const nextIndex = (roleSequence.indexOf(role) + 1) % roleSequence.length;
        setRole(roleSequence[nextIndex]);
    };

    return (
        <main className="min-h-screen bg-[#0a0a0a] flex flex-col items-center justify-center p-6">
            {/* 状态指示器与切换按钮 */}
            <div className="w-full max-w-xl mb-8 flex flex-col items-center gap-4">
                <h1 className="text-white/40 font-mono text-[10px] tracking-[0.3em] uppercase">
                    System Control Unit // {role}
                </h1>
                
                <button
                    onClick={handleToggle}
                    className="group relative px-10 py-3 bg-white text-black text-xs font-bold uppercase tracking-widest rounded-sm hover:bg-transparent hover:text-white border border-white transition-all duration-300"
                    >
                    <span className="relative z-10">Switch Perspective</span>
                    {/* 悬停时的背景动效 */}
                    <div className="absolute inset-0 bg-white scale-x-100 group-hover:scale-x-0 transition-transform origin-left duration-300"></div>
                </button>
            </div>

            {/* 你的核心动画容器 */}
            <div className="w-full max-w-xl">
                <RoleContainer />
            </div>

            {/* 底部装饰：体现 State Sync 概念 */}
            <div className="mt-12 flex gap-8">
                {['Agent', 'Admin', 'Maintainer'].map((r) => (
                    <div key={r} className="flex flex-col items-center gap-1">
                        <div className={`h-1 w-8 rounded-full transition-all duration-500 ${role === r ? 'bg-blue-500 shadow-[0_0_8px_#3b82f6]' : 'bg-white/10'}`} />
                        <span className={`text-[8px] font-mono ${role === r ? 'text-white' : 'text-white/20'}`}>{r}</span>
                    </div>
                ))}
            </div>
        </main>
    );
}