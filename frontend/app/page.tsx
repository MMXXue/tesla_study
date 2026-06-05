"use client";

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Home() {
  const pathname = usePathname();

  // 导航配置
  const navLinks = [
    { href: '/', label: 'HOME' },
    { href: '/about', label: 'About' },
    { href: '/learn', label: 'Learn' },
    { href: '/dashboard', label: 'Dashboard' },
    { href: '/zustand', label: 'Light' },
    { href: '/query', label: 'Query' },
    { href: '/schema', label: 'Schema' },
    { href: '/context', label: 'Context' },
    { href: '/errorboundary', label: 'Error' },
    { href: '/week6', label: 'WEEK 6' },
    { href: '/parser', label: 'Parser' },
    { href: '/markdown', label: 'Markdown' },
    { href: '/echarts', label: 'Echarts' },
    { href: '/blob', label: 'Blob' },
    { href: '/week7', label: 'WEEK 7' },
    { href: '/visualList', label: 'VisualList' },
    { href: '/snapshot', label: 'Image' },
    { href: '/metadata', label: 'MetadataTest' },
  ];

  return (
    <div className="min-h-screen bg-[#0d0d0d] text-neutral-200 font-sans selection:bg-white selection:text-black">
      
      {/* 顶部导航栏 - Tesla 极简风格 */}
      <nav className="fixed top-0 left-0 w-full z-50 px-8 py-6 bg-[#0d0d0d]/80 backdrop-blur-md border-b border-white/[0.03]">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-baseline gap-4">
          
          {/* Logo 部分 */}
          <div className="text-white font-bold tracking-[0.3em] text-xs transition-opacity hover:opacity-70 shrink-0">
            <Link href="/">TESLA STUDY OS</Link>
          </div>

          {/* 导航 Link 组 - 核心修改点 */}
          <div className="flex flex-wrap justify-start md:justify-end gap-x-8 gap-y-3 max-w-full md:max-w-[80%]">
            {navLinks.map((link) => {
              const isActive = pathname === link.href;
              return (
                <Link 
                  key={link.href} 
                  href={link.href}
                  className={`
                    relative text-[11px] font-bold tracking-widest transition-all duration-300
                    hover:text-white block py-1
                    ${isActive ? 'text-white' : 'text-neutral-500'}
                  `}
                >
                  {link.label}
                  {/* 悬停时的底线动画 */}
                  <span className={`
                    absolute bottom-0 left-0 h-[1px] bg-white transition-all duration-300
                    ${isActive ? 'w-full' : 'w-0 hover:w-full'}
                  `}></span>
                </Link>
              );
            })}
          </div>
        </div>
      </nav>

      {/* 首页大图或欢迎语占位 */}
      <main className="h-screen flex flex-col items-center justify-center pt-20">
        <h1 className="text-[60px] font-extralight tracking-tighter text-white opacity-20 select-none text-center px-4">
          ENGINEERING THE FUTURE
        </h1>
        <div className="mt-8 flex gap-4">
          <div className="w-1 h-1 bg-white rounded-full animate-ping"></div>
          <p className="text-[10px] tracking-[0.4em] text-neutral-600 uppercase">System Active</p>
        </div>
      </main>
      
    </div>
  );
}