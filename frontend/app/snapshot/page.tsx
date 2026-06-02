"use client";

import Image from 'next/image';

// 模拟自动驾驶车载摄像头抓取的历史原始 JPEG 大图（分辨率极高，动辄 2MB+）
const SNAPSHOT_DATA = [
  { id: 'cam-front', title: '前向主摄像头 (Front Main)', src: 'https://images.unsplash.com/photo-1617788138017-80ad40651399?q=80&w=2000' },
  { id: 'cam-left', title: '左前鱼眼镜头 (Left Pillar)', src: 'https://images.unsplash.com/photo-1506012787146-f92b2d7d6d96?q=80&w=2000' },
  { id: 'cam-right', title: '右前鱼眼镜头 (Right Pillar)', src: 'https://images.unsplash.com/photo-1542282088-fe8426682b8f?q=80&w=2000' },
];

export default function SnapshotPage() {
  return (
    <div className="p-8 bg-slate-950 min-h-screen text-slate-200">
      <div className="max-w-5xl mx-auto">
        
        {/* 头部状态条 */}
        <h1 className="text-2xl font-bold font-mono text-white mb-2 flex items-center gap-2">
          <span className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></span>
          Autopilot FSD Snapshot Viewer (设备快照优化)
        </h1>
        <p className="text-sm text-slate-400 mb-8 font-mono">
          当前优化策略：Next.js Image Optimizer + AVIF 极致压缩 + Blur 模糊占位懒加载
        </p>

        {/* 快照网格布局 */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {SNAPSHOT_DATA.map((cam) => (
            <div key={cam.id} className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-2xl flex flex-col">
              
              {/* 图片容器：使用 fill 属性时，父级必须设置 relative 和高度 */}
              <div className="relative h-48 w-full bg-slate-950">
                <Image
                  src={cam.src}
                  alt={cam.title}
                  // 1. fill：让图片自动填满父容器，适合卡片流、瀑布流布局，不用写死固定 width 和 height
                  fill
                  // 2. sizes：告诉浏览器在不同屏幕下图片的大致显示宽度。浏览器会据此下载最合适分辨率的图，防止手机端加载 4K 大图
                  sizes="(max-w-768px) 100vw, (max-w-1200px) 33vw"
                  // 3. quality：图片质量（1-100）。75 是业内公认的黄金平衡点，体积能缩减 70%，但肉眼几乎看不出画质劣化
                  quality={75}
                  // 4. placeholder 和 blurDataURL：在图片还没下载完时，先显示一个高斯模糊的极小底图，用户体验极其平滑
                  placeholder="blur"
                  blurDataURL="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
                  // 5. loading: "lazy"：开启懒加载。图片只有在快要进入视窗（眼皮底下）时才会开始下载
                  loading="lazy"
                  className="object-cover hover:scale-105 transition-transform duration-500"
                />
              </div>
              
              {/* 文字描述区 */}
              <div className="p-4 font-mono mt-auto">
                <div className="text-sm text-emerald-400 font-bold">{cam.id.toUpperCase()}</div>
                <div className="text-xs text-slate-400 mt-1">{cam.title}</div>
              </div>
              
            </div>
          ))}
        </div>
        
      </div>
    </div>
  );
}