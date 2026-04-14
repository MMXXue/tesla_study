// src/app/page.tsx
import { MyButton } from "../components/MyButton";

export default function Day32() {
  const progressData = [
    { id: 1, task: "环境搭建", status: "Done"},
    { id: 2, task: "RSC 架构理解", status: "Done"},
    { id: 3, task: "Tesla UI 实战", status: "In Progress"},
    { id: 4, task: "前端设计", status: "In Progress"},
    { id: 5, task: "后端开发", status: "In Progress"},
    { id: 6, task: "AI实战", status: "In Progress"},
  ];

  return (
    // min-h-screen: 确保黑色背景至少铺满整个屏幕高度
    // p-10: 整个页面四周留出间距
    <main className="min-h-screen bg-[#0d0d0d] p-10 text-white">
      
      <h1 className="text-2xl font-light mb-10 tracking-widest uppercase">
        Sheldon 的 AI 工程师进度表
      </h1>
      
      {/* 核心 Grid 容器 */}
      {/* gap-6: 卡片之间的间隙 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {progressData.map((item) => (
          <div 
            key={item.id} 
            // p-6: 卡片内部的文字不要贴边
            // border: 给卡片加一个淡淡的边框线
            // rounded-xl: 圆角让卡片看起来更现代
            // hover:-translate-y-2: 鼠标悬停时，在 Y 轴（垂直方向）向上移动 0.5rem
            // shadow-2xl: 增加一个巨大的投影，模拟卡片“飞起来”后离背景更远的效果
            className="p-6 bg-white/5 border border-white/10 rounded-xl hover:border-white/30 hover:-translate-y-1 shadow-xl transition-all"
          >
            <div className="flex justify-between items-center">
              <span className="text-lg font-medium">{item.task}</span>
              {/* 动态颜色点 */}
              <span className={`w-2 h-2 rounded-full ${item.status == 'Done' ? 'bg-green-500 shadow-[0_0_8px_#22c55e]' : 'bg-blue-500'}`}></span>
            </div>
            
            <p className="mt-4 text-xs text-gray-500 uppercase tracking-widest">
              Status: {item.status}
            </p>
          </div>
        ))}
      </div>

      {/* 底部按钮区域 */}
      <div className="mt-12 pt-8 border-t border-white/10 flex justify-center">
        <MyButton message={`当前你有 ${progressData.length} 项任务`} />
      </div>
    </main>
  );
}