'use client';

import React, { useEffect, useState, useRef } from 'react';

export default function Page() {
  const [status, setStatus] = useState('未连接');
  
  // 🛠️ 用一个 useRef 把 ws 实例存起来，这样在函数外面（比如按钮点击时）也能拿到它
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(function () {
    function connectWS() {
      setStatus('🟡 正在连接中...');
      console.log('🔄 开始尝试建立连接...');
      
      const ws = new WebSocket('wss://echo.websocket.org');
      wsRef.current = ws; // 把钥匙存到小抽屉（ref）里

      // 【第二步：监听开门】
      ws.onopen = function () {
        setStatus('🟢 已连接到 WS 服务器');
        console.log('--- 管道建立成功 ---');
        ws.send('哈罗，我是 Sheldon！');
      };

      // 【第三步：监听消息】
      ws.onmessage = function (event) {
        console.log('收到回音：', event.data);
      };

      // 【第四步：监听报错】
      ws.onerror = function (error) {
        console.error('WebSocket 发生错误');
      };

      // 【第五步：监听关闭】🚨 重连大本营
      ws.onclose = function () {
        setStatus('🔴 连接已断开，3秒后尝试自动重连...');
        console.log('--- 管道断开了！触发防御机制 ---');

        setTimeout(function () {
          console.log('🔄 3秒时间到，正在发起重新连接...');
          connectWS(); 
        }, 3000); 
      };
    }

    connectWS();

    return function cleanup() {
      if (wsRef.current) wsRef.current.close();
    };
  }, []); 

  // 🛠️ 按钮点击事件：模拟拔掉网线
  function handleDisconnect() {
    if (wsRef.current) {
      console.log('💥 玩家手动拔掉了网线！');
      wsRef.current.close(); // 强行关闭管道
    }
  }

  return (
    <div className="w-full min-h-screen p-6 bg-zinc-950 text-zinc-100 flex flex-col items-center justify-center gap-4">
      <div className="w-full max-w-md p-6 bg-zinc-900 rounded-xl border border-zinc-800 shadow-2xl text-center">
        <h3 className="text-zinc-100 font-medium mb-4 text-lg">WebSocket 防御系统：第一层（重连）</h3>
        
        <div className="text-xl font-bold px-4 py-3 bg-zinc-950 rounded-lg border border-zinc-850 inline-block text-amber-400 mb-6">
          {status}
        </div>
        
        {/* 🛠️ 手动破坏按钮 */}
        <div>
          <button 
            onClick={handleDisconnect}
            className="px-4 py-2 bg-red-600 hover:bg-red-700 active:bg-red-800 text-white font-medium rounded-lg text-sm transition-colors shadow-lg shadow-red-900/20"
          >
            💥 强行掐断连接（模拟断网）
          </button>
        </div>

        <p className="text-xs text-zinc-500 mt-4">
          点击红色按钮后，紧盯控制台，看它会不会在 3 秒后自动满血复活。
        </p>
      </div>
    </div>
  );
}