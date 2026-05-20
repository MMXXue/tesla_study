'use client';

import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

export  function Page() {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(function () {
    if (!containerRef.current) return;

    // 初始化图表，指定高性能的 canvas 渲染器
    const chartInstance = echarts.init(containerRef.current, 'dark', {
      renderer: 'canvas',
    });

    // 1. 初始化内存队列，先用 200 个空白数据把图表撑开
    const MAX_DATA_COUNT = 200;
    let dataQueue: number[] = Array(MAX_DATA_COUNT).fill(0);
    let timeQueue: string[] = Array(MAX_DATA_COUNT).fill('');

    // 2. 写入融入了 Canvas 优化指令的 Option
    const option = {
      title: { 
        text: '传感器高频实时频率 (60FPS)',
        textStyle: { color: '#f4f4f5' }
      },
      // 🚨 优化策略一：死死关掉全局动画，释放 CPU 算力
      animation: false,
      animationDurationUpdate: 0,
      
      grid: { top: 60, bottom: 40, left: 50, right: 20 },
      xAxis: { 
        type: 'category', 
        boundaryGap: false, // 让折线紧贴两边，没有留白，视觉更平滑
        data: timeQueue,
        axisLine: { lineStyle: { color: '#3f3f46' } },
        splitLine: { show: false } // 实时流图表不需要横向网格，减少绘制
      },
      yAxis: { 
        type: 'value',
        scale: true, // 极其重要！自动缩放 Y 轴刻度，否则折线波幅太小看不清
        splitLine: { lineStyle: { color: '#27272a' } }
      },
      series: [{ 
        type: 'line', 
        data: dataQueue,
        // 🚨 优化策略二：关闭折线上的小圆点，只画线，不画点
        showSymbol: false,
        lineStyle: { color: '#3b82f6', width: 2 },
      }]
    };

    chartInstance.setOption(option);

    // 3. 开启 60FPS 高频数据模拟器
    let count = 0;
    let animationFrameId: number;

    function simulateSensorStream() {
      count++;
      
      // 生成当前时间戳（精确到毫秒）
      const now = new Date();
      const timeStr = now.toLocaleTimeString('zh-CN', { hour12: false }) + '.' + Math.floor(performance.now() % 1000);
      
      // 模拟一个波动的传感器频率数据（围绕 50Hz 波动）
      const mockValue = 50 + Math.sin(count * 0.1) * 8 + (Math.random() - 0.5) * 4;

      // 🚨 优化策略三：先进先出队列控制
      timeQueue.push(timeStr);
      dataQueue.push(Number(mockValue.toFixed(2)));

      if (timeQueue.length > MAX_DATA_COUNT) {
        timeQueue.shift();
        dataQueue.shift();
      }

      // 听令行事：把最新队列的数据喂给图表，Canvas 会瞬间高速重绘
      chartInstance.setOption({
        xAxis: { data: timeQueue },
        series: [{ data: dataQueue }]
      });

      // 💡 告诉浏览器：紧紧对齐显示器的刷新率（大约每 16.7ms 执行下一次循环）
      animationFrameId = requestAnimationFrame(simulateSensorStream);
    }

    // 启动高频循环
    animationFrameId = requestAnimationFrame(simulateSensorStream);

    // 自动适配窗口大小
    const handleResize = () => chartInstance.resize();
    window.addEventListener('resize', handleResize);

    // 清理小机关
    return function cleanup() {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener('resize', handleResize);
      chartInstance.dispose();
    };
  }, []);

  return (
    <div className="w-full min-h-screen p-6 bg-zinc-950 text-zinc-100 flex flex-col items-center justify-center">
      <div className="w-full max-w-5xl p-6 bg-zinc-900 rounded-xl border border-zinc-800 shadow-2xl">
        <h3 className="text-zinc-100 font-medium mb-4 flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></span>
          Day 48 核心实战：Canvas 性能优化看板
        </h3>
        <div ref={containerRef} className="w-full h-[450px]" />
      </div>
    </div>
  );
}