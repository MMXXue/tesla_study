import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* 保持我们的图像极致优化配置 */
  images: {
    formats: ['image/avif', 'image/webp'],
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'images.unsplash.com',
      },
    ],
  },
};

export default nextConfig;