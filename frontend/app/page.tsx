import Link from 'next/link';
import {MyButton} from "./components/MyButton"; // 这里的路径确保指向你的组件文件夹

export default function Day31() {
  // 模拟从数据库拿到的 AI 学习进度
  const progressData = [
    { id: 1, task: "环境搭建", status: "Done", color: "bg-green-500" },
    { id: 2, task: "RSC 架构理解", status: "Done", color: "bg-green-500" },
    { id: 3, task: "Tesla UI 实战", status: "In Progress", color: "bg-blue-500" },
  ];

  return (
    <div className="min-h-screen bg-[#0d0d0d] text-neutral-200 p-8 font-sans">
      {/* 顶部导航栏 - 磨砂效果 */}
      <nav className="max-w-4xl mx-auto flex justify-between items-center mb-12 p-4 rounded-2xl bg-white/5 backdrop-blur-md border border-white/10">
        <div className="font-bold tracking-widest uppercase text-sm">Tesla Study OS</div>
        <div className="flex gap-6 text-sm">
          <Link href="/" className="hover:text-white transition-colors">HOME</Link>
          <Link href="/about" className="hover:text-white transition-colors font-semibold border-b border-white">ABOUT</Link>
          <Link href="/learn" className="hover:text-white transition-colors font-semibold border-b border-white">LEARN</Link>
          <Link href="/dashboard" className="hover:text-white transition-colors font-semibold border-b border-white">DASHBOARD</Link>
        </div>
      </nav>

      <main className="max-w-4xl mx-auto space-y-10">
        {/* 标题部分 */}
        <section>
          <h1 className="text-4xl font-light tracking-tight text-white mb-2">AI Engineer Path</h1>
          <p className="text-neutral-500 italic">Day 31: Mastering Hybrid Components</p>
        </section>

        {/* 进度列表 - 卡片式布局 */}
        <section className="grid gap-4">
          {progressData.map((item) => (
            <div key={item.id} className="group p-5 bg-neutral-900/50 border border-neutral-800 rounded-xl flex justify-between items-center hover:border-neutral-600 transition-all">
              <span className="text-lg font-light">{item.task}</span>
              <div className="flex items-center gap-3">
                <span className={`w-2 h-2 rounded-full ${item.color} animate-pulse`}></span>
                <span className="text-xs uppercase tracking-widest text-neutral-400">{item.status}</span>
              </div>
            </div>
          ))}
        </section>

        {/* 交互区域 */}
        <section className="pt-10 flex flex-col items-center border-t border-neutral-800">
          <p className="text-sm text-neutral-500 mb-6 uppercase tracking-widest">Execute Interaction</p>
          <MyButton message={`当前系统已同步 ${progressData.length} 项核心指标`} />
        </section>
      </main>
    </div>
  );
}