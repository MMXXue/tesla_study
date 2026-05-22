'use client';

import React, { useState, useEffect } from 'react';

export function Page() {
  const [isLoaded, setIsLoaded] = useState(false);
  
  // 🚨 新装配的武器：用来存放浏览器内存提货券网址的“秘密抽屉”
  const [imageSrc, setImageSrc] = useState<string>('');

  useEffect(function () {
    console.log('⏳ 骨架屏开始呼吸。正在后台模拟接收原始二进制 Blob 数据...');

    // 1. 🔬 魔法现场：用 0 和 1 凭空制造一个极小的、货真价实的 GIF 图片二进制肉块
    // 这串数字就是计算机底层的原始肌肉，人类看不懂，但显卡看得懂
    // 替换 useEffect 里面的那段旧 Uint8Array
    const rawBinaryBuffer = new Uint8Array([
        0x47, 0x49, 0x46, 0x38, 0x39, 0x61, 0x02, 0x00, 0x02, 0x00, 0x80, 0x00, 
        0x00, 0xff, 0x00, 0x00, 0xff, 0xff, 0xff, 0x21, 0xf9, 0x04, 0x00, 0x00, 
        0x00, 0x00, 0x00, 0x2c, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x02, 0x00, 
        0x00, 0x02, 0x02, 0x44, 0x01, 0x00, 0x3b
    ]);

    // 2. 🥩 把这串硬邦邦的二进制数字，打包包装成一个真正的【二进制大对象 (Blob)】
    // 并明确告诉浏览器：“这是一张 image/gif 类型的多模态资产”
    const imageBlob = new Blob([rawBinaryBuffer], { type: 'image/gif' });

    // 3. ⏰ 埋下 3 秒延迟炸弹，模拟大文件在网络管道里飞了 3 秒钟才到
    const timer = setTimeout(function () {
      
      // 4. 🎟️ 核心黑科技：把这块生肉丢进浏览器的临时内存，换取一张【内存提货券网址】
      // 它会生成一个长这样的神秘网址：blob:http://localhost:3000/xxx-xxx...
      const blobUrl = URL.createObjectURL(imageBlob);
      console.log('🎫 成功换取浏览器内存提货券：', blobUrl);

      // 5. 把提货券塞进抽屉，并拨动开关！让 React 重新放映下一帧电影
      setImageSrc(blobUrl);
      setIsLoaded(true);

    }, 3000);

    // 🧹 极其严格的防御线：当用户切换页面或者组件死掉时
    // 必须手动把这个临时网址给“销毁”，否则每刷新一次，浏览器内存就会平白无故被吃掉一块！
    return function () {
      clearTimeout(timer);
      if (imageSrc) {
        console.log('🧹 页面销毁，手动释放内存提货券，防止内存爆炸！');
        URL.revokeObjectURL(imageSrc); // 啪的一下，把提货券撕毁，内存瞬间释放
      }
    };
  }, []); 

  return (
    <div className="w-full min-h-screen bg-zinc-950 text-zinc-100 flex flex-col items-center justify-center p-6">
      <div className="w-full max-w-md p-6 bg-zinc-900 rounded-xl border border-zinc-800 shadow-2xl flex flex-col gap-4">
        
        {/* 顶部状态栏 */}
        <div className="flex justify-between items-center border-b border-zinc-800 pb-2">
          <h3 className="text-zinc-200 text-xs font-semibold tracking-wide">TESLA REALTIME BLOB STREAM</h3>
          <span className={`text-[10px] font-mono px-1.5 py-0.5 rounded ${isLoaded ? 'bg-emerald-950 text-emerald-400' : 'bg-zinc-800 text-zinc-400 animate-pulse'}`}>
            {isLoaded ? '🎯 BLOB_LIVE' : '⏳ BLOB_STREAMING'}
          </span>
        </div>

        {/* 16:9 显示视窗 */}
        <div className="relative w-full aspect-video rounded-lg overflow-hidden bg-zinc-950 border border-zinc-850 flex items-center justify-center">
          
          {/* 【第一道防线：骨架屏】 */}
          {!isLoaded && (
            <div className="absolute inset-0 w-full h-full bg-zinc-900 animate-pulse p-4 flex flex-col justify-between z-10">
              <div className="w-32 h-3 bg-zinc-800 rounded"></div>
              <div className="w-full h-20 bg-zinc-850 rounded border border-dashed border-zinc-700 opacity-50 flex items-center justify-center">
                <span className="text-[10px] text-zinc-600 font-mono">WAITING FOR BINARY CHUNK...</span>
              </div>
              <div className="w-2/3 h-2.5 bg-zinc-800 rounded"></div>
            </div>
          )}

          {/* 【第二道防线：吃进提货券网址的真实图片】 */}
          {/* 这里我们不用网络网址，直接喂给它 imageSrc 这个凭空生成的临时内存网址 */}
          {imageSrc && (
            <img 
              src={imageSrc} 
              alt="Generated Blob Asset"
              className={`w-32 h-32 object-contain bg-white rounded-lg shadow-lg transition-opacity duration-500 ${isLoaded ? 'opacity-100' : 'opacity-0'}`}
              // 因为我们现场手捏的这个纯二进制图片只是一个 2x2 像素的超微型红点，所以让它静静呆在中心即可
            />
          )}

        </div>

        {/* 底部调试提示 */}
        <div className="bg-zinc-950 p-2 rounded border border-zinc-850">
          <p className="text-[10px] text-zinc-500 font-mono truncate text-center">
            {isLoaded ? `Current ObjectURL: ${imageSrc}` : 'Generatng Uint8Array Buffer inside factory...'}
          </p>
        </div>

      </div>
    </div>
  );
}