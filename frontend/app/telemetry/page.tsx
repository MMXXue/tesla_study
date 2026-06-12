
// 遥感页面

"use client";

import { useEffect, useState } from "react";

// 模拟 50 辆 Tesla 汽车的初始 ID 名单, 一秒钟凭空造出 50 辆车的名字。
const CAR_IDS = Array.from({ length: 50 }, (_, i) => `TSLA-MODEL-${i + 1}`);

export default function TelemetryPage() {
  const [metrics, setMetrics] = useState<{ [key: string]: number }>({});

//   useEffect(() => {
//     // 📊 模拟 50+ 实时数据流同时高频刷新（每 50 毫秒轰炸一次！）
//     const timer = setInterval(() => {
//       const updatedMetrics = { ...metrics };
      
//       CAR_IDS.forEach((id) => {
//         // 模拟车机传回来的高频 FSD 神经网络置信度百分比
//         updatedMetrics[id] = Math.floor(Math.random() * 100);
//       });

//       setMetrics(updatedMetrics);
//     }, 50);

//     // 💣 【高能注意】：大厂特级禁忌！
//     // 我们故意在这里【不写】 return () => clearInterval(timer);
//     // 这意味着每当你刷新这个页面，或者来回切换路由时，旧的定时器会永远残留在内存里，
//     // 并且由于闭包死死抓着 metrics 状态，浏览器内存会以恐怖的速度雪崩式泄露！

//   }, [metrics]); // 故意让 metrics 变成依赖项，导致组件每次更新都在疯狂创建新的定时器！





useEffect(() => {
    // 📊 1. 唯一启动：整个生命周期里，定时器只在页面打开时启动【唯一的一次】
    const timer = setInterval(() => {
      
      // 💡 2. 函数式更新：直接拿取上一次的旧状态 prevMetrics，彻底切断对外部 metrics 的依赖！


      //   一上来就把原先metrics里的数据就给到了prevMetrics,然后,再执行他后面{}里的内容
      setMetrics((prevMetrics) => {
        const updatedMetrics = { ...prevMetrics }; // 在肚子里安全复印账本
        CAR_IDS.forEach((id) => {
          updatedMetrics[id] = Math.floor(Math.random() * 100);
        });
        return updatedMetrics;
      });

    }, 50);

    // 🛡️ 3. 留下遗嘱：当用户切换页面、或者刷新组件销毁时，立刻物理掐死定时器！
    return () => clearInterval(timer);

  }, []); // 🌟 依赖项变回空数组 []！彻底切断套娃回路！





  return (
    <div className="p-8 bg-gray-900 text-white min-h-screen">
      <h1 className="text-3xl font-bold mb-6 text-red-500">🏎️ 特斯拉 AI 实时遥测数据流大屏 (50+ 并发压测)</h1>
      <div className="grid grid-cols-5 gap-4">
        {CAR_IDS.map((id) => (
          <div key={id} className="bg-gray-800 p-4 rounded-lg border border-gray-700">
            <div className="text-xs text-gray-400">{id}</div>
            <div className="text-2xl font-mono text-green-400 mt-2">
              FSD Confidence: {metrics[id] || 0}%
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}