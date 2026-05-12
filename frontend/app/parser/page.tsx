"use client"

import { useState, useRef, useEffect } from 'react';
import { MarkdownStreamParser } from './stream-parser';

export default function ChatPage() {
  const [content, setContent] = useState("");
  const [isStreaming, setIsStreaming] = useState(false); // 状态：是否正在传输
  
  // 1. 引用聊天容器和底部锚点
  const scrollRef = useRef<HTMLDivElement>(null);
  const anchorRef = useRef<HTMLDivElement>(null);
  const [isAutoScroll, setIsAutoScroll] = useState(true);

  // 2. 自动滚动逻辑
  useEffect(() => {
    if (isAutoScroll && isStreaming) {
      // 使用 scrollIntoView 触发滚动，behavior: 'instant' 减少高频渲染下的抖动
      anchorRef.current?.scrollIntoView({ behavior: 'instant' });
    }
  }, [content, isStreaming, isAutoScroll]);

  // 3. 监控用户滚动行为
  const handleScroll = () => {
    const container = scrollRef.current;
    if (!container) return;
    
    // 判断是否接近底部 (阈值 100px)
    const isAtBottom = container.scrollHeight - container.scrollTop <= container.clientHeight + 100;
    setIsAutoScroll(isAtBottom);
  };

  const startChat = async () => {
    setContent(""); 
    setIsStreaming(true); // 开始流式传输
    setIsAutoScroll(true); // 初始强制触底
    
    const parser = new MarkdownStreamParser();
    const response = await fetch('/parser/mock');
    const reader = response.body?.getReader();

    if (!reader) {
      setIsStreaming(false);
      return;
    }

    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        parser.flush((text: string) => setContent(prev => prev + text));
        setIsStreaming(false); // 传输结束
        break;
      }
      
      parser.parse(value, (text: string) => {
        setContent(prev => prev + text);
      });
    }
  };

  return (
    <div className="flex flex-col h-screen p-8 bg-gray-100">
      <button 
        onClick={startChat}
        disabled={isStreaming}
        className="px-4 py-2 bg-blue-600 text-white rounded-lg shadow hover:bg-blue-700 disabled:bg-blue-300 transition-colors"
      >
        {isStreaming ? "正在生成..." : "开始接收流式数据"}
      </button>
      
      {/* 
        4. 关键布局优化：
        - flex-1 让容器占满剩余空间
        - overflow-y-auto 开启独立滚动
        - whitespace-pre-wrap 保持换行格式
      */}
      <div 
        ref={scrollRef}
        onScroll={handleScroll}
        className="mt-6 flex-1 p-6 border rounded-xl bg-white shadow-inner overflow-y-auto contain-content"
      >
        <div className="prose prose-slate max-w-none text-gray-800 leading-relaxed whitespace-pre-wrap">
          {content}
          
          {/* 5. 呼吸光标逻辑 */}
          {isStreaming && (
            <span className="inline-block w-1.5 h-5 ml-1 translate-y-1 bg-blue-500 animate-pulse" />
          )}
        </div>

        {/* 6. 隐形锚点：用于 scrollIntoView */}
        <div ref={anchorRef} className="h-px w-full" />
      </div>

      {/* 7. UX 增强：如果不处在自动滚动状态，显示提示（可选实现） */}
      {!isAutoScroll && isStreaming && (
        <div className="fixed bottom-24 left-1/2 -translate-x-1/2">
          <button 
            onClick={() => setIsAutoScroll(true)}
            className="bg-blue-500 text-white px-3 py-1 rounded-full text-sm shadow-lg animate-bounce"
          >
            ↓ 回到底部
          </button>
        </div>
      )}
    </div>
  );
}