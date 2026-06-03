"use client";

import { useState, useEffect } from 'react';

export default function Bomb() {
  const [shouldCrash, setShouldCrash] = useState(false);

  // 1. 防御性代码：如果是 Next.js 后端服务器在编译预渲染，绝对不执行崩溃逻辑
  useEffect(() => {
    // 这里可以放那些只有浏览器才支持的 DOM 操作
  }, []);

  // 2. 如果触发了崩溃状态，抛出错误供 ErrorBoundary 捕获
  if (shouldCrash) {
    throw new Error("🚨 传感器硬件通信中断！触发系统级熔断保护。");
  }

  return (
    <div className="p-4 bg-red-50 rounded-xl border border-red-100 flex flex-col justify-between">
      <div>
        <h4 className="font-medium text-red-800 mb-2">雷达传感器状态</h4>
        <div className="text-xs text-red-600">正在高频接收硬件遥测数据...</div>
      </div>
      
      {/* 3. 通过用户手动点击，在客户端现场“引爆炸弹”，这样绝对不会阻碍编译打包 */}
      <button 
        onClick={() => setShouldCrash(true)}
        className="mt-4 px-3 py-1.5 bg-red-600 hover:bg-red-700 text-white font-mono text-[11px] rounded transition-colors self-start"
      >
        模拟切断硬件线缆 (引发崩溃)
      </button>
    </div>
  );
}