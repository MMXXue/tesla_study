'use client';

import React, { useEffect, useState, useRef } from 'react';

export default function Page() {
  const [status, setStatus] = useState('未连接');
  
  // 📦 准备三个“共享抽屉”，用来存放连接钥匙和两枚定时器炸弹
  const wsRef = useRef<WebSocket | null>(null);
  const pingIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const pongTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(function () {
    
    function connectWS() {
      setStatus('🟡 正在连接中...');
      console.log('🔄 开始尝试建立连接...');
      
      // 【第一步：建立通道】
      const ws = new WebSocket('wss://echo.websocket.org');
      wsRef.current = ws; 

      // 【第二步：监听开门】🟢 在这里拉起心跳发射器
      ws.onopen = function () {
        setStatus('🟢 已连接 (心跳守护中)');
        console.log('--- 管道建立成功，启动心跳守护 ---');
        
        // 🚀 启动心跳机制
        startHeartbeat();
      };

      // 【第三步：监听消息】💬 只要对方说话，就证明活着，立刻重置心跳
      ws.onmessage = function (event) {
        console.log('收到服务器回音：', event.data);
        
        // 🚨 极其重要：收到任何消息，都说明连接健康，重新计算心跳倒计时
        startHeartbeat();
      };

      // 【第四步：监听报错】
      ws.onerror = function (error) {
        console.error('WebSocket 发生错误');
      };

      // 【第五步：监听关闭】🔴 连接死了，必须“收尸”并“重连”
      ws.onclose = function () {
        setStatus('🔴 连接已断开，3秒后自动重连...');
        console.log('--- 管道断开了！清理残留定时器，准备重连 ---');

        // 🚨 1. 收尸：必须清空心跳定时器，否则断线后后台还会疯狂报错
        clearAllTimers();

        // 🚨 2. 重连：3秒后拉活
        setTimeout(function () {
          console.log('🔄 3秒时间到，正在发起重新连接...');
          connectWS(); 
        }, 3000); 
      };
    }

    // 💓 核心防御武器：启动/重置心跳的函数
    function startHeartbeat() {
      // 每次重新计算前，先清理掉上一次的旧定时器
      clearAllTimers();

      // A 闹钟：每隔 5 秒钟，催促前端发一个 "ping"
      pingIntervalRef.current = setTimeout(function () {
        if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
          console.log('💓 前端发射: ping');
          wsRef.current.send('ping'); // 顺着管道发给服务器
          
          // B 闹钟（炸弹）：发射 "ping" 的瞬间，埋下一个 3 秒后爆炸的炸弹
          pongTimeoutRef.current = setTimeout(function () {
            console.warn('💀 警报！3秒内未收到服务器对暗号，判定为假死！强行掐断！');
            if (wsRef.current) wsRef.current.close(); // 掀翻桌子，这会自动触发 onclose 里的重连
          }, 3000);
        }
      }, 5000);
    }

    // 🧹 专门用来清空抽屉里定时器的工具函数
    function clearAllTimers() {
      if (pingIntervalRef.current) clearTimeout(pingIntervalRef.current);
      if (pongTimeoutRef.current) clearTimeout(pongTimeoutRef.current);
    }

    // 启动大坝
    connectWS();

    // 离开页面时的终极清理
    return function cleanup() {
      clearAllTimers();
      if (wsRef.current) wsRef.current.close();
    };
  }, []); 

  // 手动掐断按钮（用来测试假死和重连）
  function handleDisconnect() {
    if (wsRef.current) {
      console.log('💥 玩家手动拔掉了网线！');
      wsRef.current.close();
    }
  }

  return (
    <div className="w-full min-h-screen p-6 bg-zinc-950 text-zinc-100 flex flex-col items-center justify-center gap-4">
      <div className="w-full max-w-md p-6 bg-zinc-900 rounded-xl border border-zinc-800 shadow-2xl text-center">
        <h3 className="text-zinc-100 font-medium mb-4 text-lg">WebSocket 终极防御系统 (Day 49)</h3>
        
        <div className="text-xl font-bold px-4 py-3 bg-zinc-950 rounded-lg border border-zinc-850 inline-block text-emerald-400 mb-6">
          {status}
        </div>
        
        <div>
          <button 
            onClick={handleDisconnect}
            className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white font-medium rounded-lg text-sm transition-colors shadow-lg"
          >
            💥 模拟突然断网
          </button>
        </div>

        <p className="text-xs text-zinc-500 mt-4">
          保存后请紧盯 F12 控制台。你会看到每隔 5 秒自动发射一次 ping，并且服务器会秒回。
        </p>
      </div>
    </div>
  );
}