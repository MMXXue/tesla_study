
// src/app/page.tsx

import { MyButton } from "../components/MyButton";
import StatusCard from '../components/StatusCard';
import ChatBubble from '../components/ChatBubble';
import { MotionCard } from '../components/MotionCard';
import { ToggleCard } from '../components/ToggleCard';
import LayoutCard from '../components/LayoutCard';
import { DeviceCard } from '../components/DeviceCard';

export default function Day32() {
  const progressData = [
    { id: 1, title: "环境搭建", status: "Done"},
    { id: 2, title: "RSC 架构理解RSC 架构理解RSC 架构理解RSC 架构理解RSC 架构理解RSC 架构理解RSC 架构理解", status: "Done"},
    { id: 3, title: "Tesla UI 实战", status: "In Progress"},
    { id: 4, title: "前端设计", status: "Pending"},
    { id: 5, title: "后端开发", status: "Error"},
    { id: 6, title: "AI实战", status: "In Progress"},
  ];

  const mockChat = [
    { id: 1, role: 'assistant', text: 'System initialized. All nodes active.' },
    { id: 2, role: 'user', text: 'Check the battery status of Robot A1.' },
    { id: 3, role: 'assistant', text: 'Robot A1: Battery at 85%. Temperature nominal.' },
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
      <div className="grid 
        gap-6 
        /* 默认：手机端 1 列 */
        grid-cols-1 
        /* 平板端：2 列 */
        sm:grid-cols-2 
        /* 笔记本/普通显示器：3 列 */
        lg:grid-cols-3 
        /* 超宽屏（Ultrawide）：6 列全开，一字排开 */
        2xl:grid-cols-6 
        
        /* 限制最大宽度，防止在大屏幕上铺得太满 */
        max-w-[1800px] 
        mx-auto"
      >
        {progressData.map(item => (
          <StatusCard 
            key={item.id} 
            title={item.title} 
            status={item.status as any} 
          />
        ))}
      </div>

      {/* 底部按钮区域 */}
      <div className="mt-12 pt-8 border-t border-white/10 flex justify-center">
        <MyButton message={`当前你有 ${progressData.length} 项任务`} />
      </div>

      {/* 新开辟的区域ChatBubble */}
      <div className="mt-10 p-6 bg-black/40 rounded-3xl border border-white/5">
        <h3 className="text-gray-500 text-xs uppercase mb-6 tracking-widest">AI Command Center</h3>
        {mockChat.map(msg => (
          <ChatBubble 
            key={msg.id} 
            content={msg.text} 
            role={msg.role as any} 
          />
        ))}
      </div>

    <div className="mt-12 pt-8 border-t border-white/10 flex justify-center">
      <MotionCard />
      <MotionCard />
      <MotionCard />
      <MotionCard />
      <MotionCard />
    </div>

    <div className="mt-12 pt-8 border-t border-white/10 flex justify-center">
      <ToggleCard />
    </div>

    <div>
      <LayoutCard />
    </div>

    <div className="min-h-screen bg-black flex items-center justify-center">
      <DeviceCard />
    </div>
    

    </main>
  );
}