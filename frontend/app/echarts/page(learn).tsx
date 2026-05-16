'use client'; // 🛠️ 告诉 Next.js 这是一个需要在浏览器运行的客户端组件

import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

// 🛠️ 使用 Next.js 强制要求的 export default function Page() 结构
export function Page() {
  
  // 建立一根隐形的线（Ref），用来精准指向底层的 DOM 元素
  const containerRef = useRef<HTMLDivElement>(null);

  // 用 useEffect 守候，等到网页舞台（DOM）渲染完毕后再执行画家逻辑
  useEffect(function () {
    // 安全检查：如果舞台没盖好，先不执行，防止报错
    if (!containerRef.current) return;

    // 舞台盖好了，通知画家初始化 Canvas 像素画布
    const chartInstance = echarts.init(containerRef.current, 'dark', {
      renderer: 'canvas',
    });

    // 准备一份最简单的静态配置，用来测试骨架是否通路
    const option = {
      title: { 
        text: 'ECharts 骨架测试成功',
        textStyle: { color: '#f4f4f5' } // 对齐 Tailwind 的锌色字体
      },
      xAxis: { 
        type: 'category', 
        data: ['A', 'B', 'C', 'D', 'E'],
        axisLine: { lineStyle: { color: '#3f3f46' } }
      },
      yAxis: { 
        type: 'value',
        splitLine: { lineStyle: { color: '#27272a' } }
      },
      series: [{ 
        type: 'bar', 
        data: [10, 20, 15],
        lineStyle: { color: '#3b82f6' } // 使用 Tailwind 蓝
      }]
    };

    // 把配置塞给 ECharts，让它在 Canvas 上画出来
    chartInstance.setOption(option);

    // 工业级规范：组件从屏幕消失时，必须把画家释放掉，防止内存泄漏
    return function cleanup() {
      chartInstance.dispose();
    };
  }, []); // 空数组，确保这段初始化逻辑在页面打开时只执行一次

  return (
    // 🛠️ 纯正的 Tailwind CSS 满屏暗黑布局
    <div className="w-full min-h-screen p-6 bg-zinc-950 text-zinc-100 flex flex-col items-center justify-center">
      
      <div className="w-full max-w-4xl p-6 bg-zinc-900 rounded-xl border border-zinc-800 shadow-2xl">
        <h3 className="text-zinc-100 font-medium mb-4 flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
          工业级传感器监控骨架
        </h3>
        
        {/* 我们的舞台：ref={containerRef} 让上面的钩子精准勾住这个盒子 */}
        {/* w-full h-[400px] 用 Tailwind 牢牢锁死画布的宽高 */}
        <div ref={containerRef} className="w-full h-[400px]" />
      </div>

    </div>
  );
}