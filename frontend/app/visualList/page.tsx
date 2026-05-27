"use client"; // 1. 告诉 Next.js 这是一个客户端渲染组件（必须写在第一行）

import React, { useState, useRef } from 'react';

// ==================== 1. 虚拟列表组件类型定义 ====================
interface VirtualListProps {
  listData: string[];
  itemHeight?: number;
  screenHeight?: number;
}

// ==================== 2. 虚拟列表核心组件 ====================
const TailwindVirtualList: React.FC<VirtualListProps> = ({ 
  listData = [], 
  itemHeight = 40, 
  screenHeight = 400 
}) => {
  const containerRef = useRef<HTMLDivElement>(null);

  const visibleCount = Math.ceil(screenHeight / itemHeight);

  const [start, setStart] = useState<number>(0);
  const [end, setEnd] = useState<number>(visibleCount);
  const [startOffset, setStartOffset] = useState<number>(0);

  const visibleData = listData.slice(start, Math.min(end, listData.length));

  const onScroll = () => {
    if (!containerRef.current) return;
    
    const scrollTop = containerRef.current.scrollTop;
    const currentStart = Math.floor(scrollTop / itemHeight);
    
    setStart(currentStart);
    setEnd(currentStart + visibleCount);
    setStartOffset(currentStart * itemHeight);
  };

  return (
    <div
      ref={containerRef}
      onScroll={onScroll}
      className="relative overflow-y-auto border border-slate-800 rounded-lg bg-slate-900 text-slate-200 shadow-xl"
      style={{ height: `${screenHeight}px` }}
    >
      {/* 撑高层 */}
      <div 
        className="absolute left-0 top-0 right-0 -z-10 pointer-events-none"
        style={{ height: `${listData.length * itemHeight}px` }}
      />
      
      {/* 数据层 */}
      <div 
        className="absolute left-0 right-0 top-0 will-change-transform"
        style={{ transform: `translate3d(0, ${startOffset}px, 0)` }}
      >
        {visibleData.map((item, index) => {
          const actualIndex = start + index;
          return (
            <div 
              key={actualIndex} 
              className="flex items-center px-4 border-b border-slate-800 hover:bg-slate-800/50 font-mono text-sm"
              style={{ height: `${itemHeight}px` }}
            >
              <span className="text-emerald-500 mr-3 select-none">[{actualIndex}]</span>
              <span className="truncate">{item}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

// ==================== 3. Next.js 路由主页面 (必须用 export default) ====================
export default function VisualListPage() {
  // 模拟生成 10,000 条历史日志数据
  const mockLogs = Array.from({ length: 10000 }, (_, i) => {
    const timestamps = new Date(Date.now() - i * 1000).toISOString();
    return `${timestamps} - USER_ACTION - Clicked button #${i} - Status 200`;
  });

  return (
    <div className="p-8 bg-slate-950 min-h-screen flex flex-col justify-center items-center">
      <div className="w-full max-w-2xl">
        <h1 className="text-xl font-bold text-white mb-4">Tesla Log Viewer (10,000 条日志)</h1>
        <TailwindVirtualList listData={mockLogs} itemHeight={40} screenHeight={450} />
      </div>
    </div>
  );
}