// src/app/page.tsx
import {MyButton} from "../components/MyButton";

export default function Day31() {
  // 模拟从数据库拿到的 AI 学习进度
  const progressData = [
    { id: 1, task: "环境搭建", status: "已完成" },
    { id: 2, task: "RSC 理论", status: "已完成" },
    { id: 3, task: "混合组件实战", status: "进行中" },
  ];

  return (
    <main className="p-10 bg-slate-50 min-h-screen">
      <h1 className="text-2xl font-bold mb-6">Sheldon 的 AI 工程师进度表</h1>
      
      <div className="space-y-4">
        {progressData.map((item) => (
          <div key={item.id} className="p-4 bg-white shadow rounded-lg flex justify-between">
            <span>{item.task}</span>
            <span className="text-blue-500 font-mono">{item.status}</span>
          </div>
        ))}
      </div>

      {/* 把数据传给 Client 组件 */}
      <div className="mt-8">
        <MyButton message={`当前你有 ${progressData.length} 项任务`} />
      </div>
    </main>
  );
}