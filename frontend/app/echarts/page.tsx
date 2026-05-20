'use client';

import React, { useEffect, useState } from 'react';

export default function Page() {
  const [status, setStatus] = useState('未连接');

  useEffect(function () {
    // 🛠️ 核心改变：我们把 WebSocket 的初始化打包成一个可以反复调用的“功能包”
    function connectWS() {
      setStatus('🟡 正在连接中...');
      
      // 【第一步：建立通道】
      const ws = new WebSocket('wss://echo.websocket.org');

      // 【第二步：监听开门】
      ws.onopen = function () {
        setStatus('🟢 已连接到 WS 服务器');
        console.log('--- 管道建立成功 ---');
      };

      // 【第三步：监听消息】
      ws.onmessage = function (event) {
        console.log('收到回音：', event.data);
      };

      // 【第四步：监听报错】只负责打日志
      ws.onerror = function (error) {
        console.error('WebSocket 发生错误');
      };

      // 【第五步：监听关闭】🚨 重连的秘密基地就在这里！
      ws.onclose = function () {
        setStatus('🔴 连接已断开，3秒后尝试自动重连...');
        console.log('--- 管道断开了！触发防御机制 ---');

        // 🛠️ 关键动作：定一个 3 秒后的闹钟，闹钟一响，重新执行 connectWS()
        setTimeout(function () {
          console.log('🔄 3秒时间到，正在发起重新连接...');
          connectWS(); // 自己调用自己，重新走一遍第一步
        }, 3000); 
      };
    }

    // 🚀 页面刚打开时，我们手动推一把，启动第一次连接
    connectWS();

  }, []); // 空数组，确保整个机制只在页面初次加载时拉起一次

  return (
    <div className="w-full min-h-screen p-6 bg-zinc-950 text-zinc-100 flex flex-col items-center justify-center">
      <div className="w-full max-w-md p-6 bg-zinc-900 rounded-xl border border-zinc-800 shadow-2xl text-center">
        <h3 className="text-zinc-100 font-medium mb-4 text-lg">WebSocket 防御系统：第一层（重连）</h3>
        <div className="text-xl font-bold px-4 py-3 bg-zinc-950 rounded-lg border border-zinc-850 inline-block text-amber-400">
          {status}
        </div>
        <p className="text-xs text-zinc-500 mt-4">
          提示：可以通过断开 Wi-Fi 或等待公共服务器波动来测试重连日志。
        </p>
      </div>
    </div>
  );
}