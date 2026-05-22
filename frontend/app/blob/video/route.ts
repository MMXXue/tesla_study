
// 假装自己是一个正在高频抓取车端画面的 AI 视频流服务器

import { NextResponse } from 'next/server';

// 🚨 这是一段全栈硬核代码：模拟后端视频流接口
export async function GET() {
  // 1. 我们找一个公开的、高清的 Tesla 官方超跑测试视频网址作为源头
  const videoUrl = 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4';
  
  // 2. 后端服务器向这个网址发起请求，拿到这个视频的“原始大水管”（ReadableStream）
  const response = await fetch(videoUrl);
  
  if (!response.body) {
    return new NextResponse('视频源连接失败', { status: 500 });
  }

  // 3. ✨ 关键黑科技：Next.js 后端不把视频整个下载完，而是直接把这根“原始大水管”
  // 塞进 Response 盒子里，直接原封不动地递给前端！
  return new NextResponse(response.body, {
    headers: {
      // 告诉前端浏览器：“我给你的是一段没有尽头的、原汁原味的视频二进制流，你准备好边拿边播！”
      'Content-Type': 'video/mp4',
      'Transfer-Encoding': 'chunked', // 意思是分块传输，切香肠模式开启
    },
  });
}