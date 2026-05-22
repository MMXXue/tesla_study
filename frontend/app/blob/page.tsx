'use client';

import React, { useState } from 'react';

export default function Page() {
  // 控制视频加载状态的开关
  const [isVideoLoading, setIsVideoLoading] = useState(true);

  return (
    <div className="w-full min-h-screen bg-zinc-950 text-zinc-100 flex flex-col items-center justify-center p-6">
      <div className="w-full max-w-xl p-6 bg-zinc-900 rounded-xl border border-zinc-800 shadow-2xl flex flex-col gap-4">
        
        {/* 顶部状态栏 */}
        <div className="flex justify-between items-center border-b border-zinc-800 pb-2">
          <h3 className="text-zinc-200 text-xs font-semibold tracking-wide">TESLA AUTOPILOT VIDEO STREAM</h3>
          <span className={`text-[10px] font-mono px-1.5 py-0.5 rounded ${isVideoLoading ? 'bg-zinc-800 text-zinc-400 animate-pulse' : 'bg-emerald-950 text-emerald-400'}`}>
            {isVideoLoading ? '⏳ STREAM_BUFFERING' : '🎯 STREAM_LIVE'}
          </span>
        </div>

        {/* 16:9 视频视窗 */}
        <div className="relative w-full aspect-video rounded-lg overflow-hidden bg-zinc-950 border border-zinc-850 flex items-center justify-center">
          
          {/* 【第一道防线：视频骨架屏】如果视频还没准备好，闪烁占位 */}
          {isVideoLoading && (
            <div className="absolute inset-0 w-full h-full bg-zinc-900 animate-pulse p-4 flex flex-col justify-between z-10">
              <div className="w-32 h-3 bg-zinc-800 rounded"></div>
              <div className="w-full h-24 bg-zinc-850 rounded border border-dashed border-zinc-700 opacity-50 flex items-center justify-center">
                <span className="text-[10px] text-zinc-500 font-mono">CONNECTING TO VIDEO WATER-TAP...</span>
              </div>
              <div className="w-1/2 h-2.5 bg-zinc-800 rounded"></div>
            </div>
          )}

          {/* 【第二道防线：现代视频消费引擎】 */}
          <video 
            // 🚀 核心看点：src 直接指向我们刚刚手写的后端切香肠接口！
            src="/api/video" 
            autoPlay 
            muted 
            loop 
            controls
            className="w-full h-full object-cover"
            // 🚨 秘密侦听器：onCanPlay 意思是浏览器顺着水龙头抠出来的二进制肉块，
            // 已经足够开始播放第一帧了！
            onCanPlay={function() {
              console.log('🎬 浏览器报告：视频流前几块肉已经咬住了，可以丝滑播放！');
              setIsVideoLoading(false); // 关掉骨架屏，露出一边下载一边播放的视频
            }}
          />

        </div>

        {/* 底部调试文字 */}
        <div className="bg-zinc-950 p-2 rounded border border-zinc-850 text-center">
          <p className="text-[10px] text-zinc-500 font-mono">
            Source Endpoint: <span className="text-zinc-400">/api/video (HTTP Progressive Chunked Stream)</span>
          </p>
        </div>

      </div>
    </div>
  );
}