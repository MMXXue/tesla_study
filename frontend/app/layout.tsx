import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Providers from "./providers"; // 1. 引入刚才创建的小盒子

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});


// 派发给 layout.tsx 的总身份证
export const metadata: Metadata = {
  title: {
    default: "TESLA STUDY OS | 智能全栈中央管理系统",
    template: "%s | TESLA STUDY OS" // 👈 就是这个关键的 %s，会动态吃掉子页面的标题
  },
  description: "工业级高频硬件遥测流诊断、虚拟化滚动日志终端及微服务容错控制系统。",
  keywords: ["Tesla", "AI Engineer", "Telemetry", "Next.js"],
  robots: {
    index: true,
    follow: true,
  }
};


export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">
        {/* 2. 用 Providers 把 children 包起来 */}
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}