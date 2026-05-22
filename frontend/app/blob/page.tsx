
// 纯手工打造一个 AI 多模态骨架屏（Skeleton Screen）

'use client';

// 1. 从 React 发动机仓库里，把“开关把手”（useState）和“副作用定时器”（useEffect）召唤出来
import React, { useState, useEffect } from 'react';

export default function Page() {
  // 2. 核心状态：图片是否下载完毕的开关（默认是 false，代表还没下载完）
  const [isLoaded, setIsLoaded] = useState(false);

  // 3. 模拟网络延迟：利用 useEffect 机制，在网页刚打开时，埋下一个 3 秒后的定时器
  useEffect(function () {
    console.log('🎬 网页已打开，AI 正在后台拼命推理，请静候 3 秒...');
    
    const timer = setTimeout(function () {
      console.log('⚡ 3秒时间到！AI 把多模态图片的数据推过来了！');
      // 拨动开关！整个页面会重新执行一遍（电影胶片切到下一帧）
      setIsLoaded(true); 
    }, 3000);

    // 🧹 还记得昨天的规矩吗？走人时顺手把定时器砸烂，防止内存泄漏
    return function () {
      clearTimeout(timer);
    };
  }, []); // 后面跟着空数组，意思是这个定时器“一生只在刚开门时启动一次”

  return (
    // 最外层的暗黑背景大底座
    <div className="w-full min-h-screen bg-zinc-950 text-zinc-100 flex flex-col items-center justify-center p-6">
      
      {/* 居中对齐的卡片大盒子 */}
      <div className="w-full max-w-md p-6 bg-zinc-900 rounded-xl border border-zinc-800 shadow-2xl flex flex-col gap-4">
        
        {/* 顶部标签区域 */}
        <div className="flex justify-between items-center border-b border-zinc-800 pb-2">
          <h3 className="text-zinc-200 text-xs font-semibold tracking-wide">TESLA VISION PERCEPTION</h3>
          <span className={`text-[10px] font-mono px-1.5 py-0.5 rounded ${isLoaded ? 'bg-emerald-950 text-emerald-400' : 'bg-zinc-800 text-zinc-400 animate-pulse'}`}>
            {isLoaded ? '🎯 LIVE' : '⏳ COMPUTING'}
          </span>
        </div>

        {/* 🖼️ 核心战区：16:9 的多模态显示视窗 */}
        <div className="relative w-full aspect-video rounded-lg overflow-hidden bg-zinc-950 border border-zinc-850">
          
          {/* 【防线一：骨架屏】如果 isLoaded 是假的，就死死锁在这里进行呼吸闪烁 */}
          {!isLoaded && (
            <div className="absolute inset-0 w-full h-full bg-zinc-900 animate-pulse p-4 flex flex-col justify-between">
              {/* 模拟顶部的 AI 绿色目标识别文本块 */}
              <div className="w-24 h-3 bg-zinc-800 rounded"></div>
              {/* 模拟中央大卡车的虚拟虚线识别框 */}
              <div className="w-full h-20 bg-zinc-850 rounded border border-dashed border-zinc-700 opacity-50"></div>
              {/* 模拟底部的置信度百分比进度条 */}
              <div className="w-1/2 h-2.5 bg-zinc-800 rounded"></div>
            </div>
          )}

          {/* 【防线二：真实的 AI 车辆多模态图片】 */}
          {/* 无论开关如何，它都在后台悄悄下载。通过 transition-opacity 实现 0.5 秒丝滑淡入 */}
          <img 
            src="https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=800&q=80" 
            alt="Tesla Cybertruck Camera"
            className={`w-full h-full object-cover transition-opacity duration-500 ${isLoaded ? 'opacity-100' : 'opacity-0'}`}
          />

        </div>

        {/* ℹ️ 底部调试提示文字 */}
        <p className="text-[11px] text-zinc-500 text-center font-mono">
          {isLoaded ? 'Grid view stabilized. Cache cleared.' : 'Simulating network latency via setTimeout...'}
        </p>

      </div>
    </div>
  );
}