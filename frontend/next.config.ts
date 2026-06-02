import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* 在这里配置我们的设备快照图像优化策略 */
  images: {
    // 1. 允许 Next.js 后端服务将图片智能重新编码为 AVIF 和 WebP。会优先尝试压缩率更高的 AVIF
    formats: ['image/avif', 'image/webp'],
    
    // 2. 外部图片域名白名单。允许 Next.js 拦截并优化来自 Unsplash 的高清图片源
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'images.unsplash.com',
      },
    ],
  },
};

export default nextConfig;