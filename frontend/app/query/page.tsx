
// 负责漂亮的

"use client";

import { useQuery } from '@tanstack/react-query';
import { getStudyTasks } from './services/taskService'; // 引入刚才写的管道

export default function QueryPage() {
    // 【核心步骤】使用 useQuery 钩子
    const { data, isLoading, isError, refetch } = useQuery({
        queryKey: ['studyTasks'], // 身份证：给这段数据起个名字叫 studyTasks
        queryFn: getStudyTasks,    // 动作：告诉它去执行你刚才写的函数
        staleTime: 1000 * 5,       // 额外技能：5秒内数据算“新鲜”，切回来不重新请求
    });

    // 1. 加载中状态
    if (isLoading) {
        return (
            <div className="min-h-screen bg-[#0d0d0d] flex items-center justify-center">
                <div className="text-white tracking-[0.3em] animate-pulse">同步 TESLA 任务中...</div>
            </div>
        );
    }

    // 2. 报错状态
    if (isError) {
        return <div className="text-red-500 p-20">系统连接异常，请重试。</div>;
    }

    return (
        <div className="min-h-screen bg-[#0d0d0d] text-neutral-200 p-8">
            <main className="max-w-4xl mx-auto space-y-10">
                <header>
                    <h1 className="text-4xl font-light text-white mb-2">AI Engineer Path</h1>
                    <p className="text-neutral-500 italic">Day 39: Server State Synchronization</p>
                </header>

                {/* 3. 渲染数据：此时 data 就是 getStudyTasks 返回的数组 */}
                <section className="grid gap-4">
                {data?.map((item) => (
                    <div key={item.id} className="p-5 bg-neutral-900/50 border border-neutral-800 rounded-xl flex justify-between items-center">
                        <div>
                            <div className="text-lg font-light">{item.task}</div>
                            <div className="text-xs text-neutral-500 uppercase tracking-tighter">难度: {item.difficulty}</div>
                        </div>
                        <span className={`text-xs uppercase tracking-widest ${item.status === 'Done' ? 'text-green-500' : 'text-blue-500'}`}>
                            {item.status}
                        </span>
                    </div>
                ))}
                </section>

                {/* 手动刷新测试 */}
                <button 
                onClick={() => refetch()}
                className="px-8 py-3 bg-white text-black rounded-full text-xs font-bold active:scale-95 transition-all"
                >
                FORCE RE-SYNC
                </button>
            </main>
        </div>
    );
}