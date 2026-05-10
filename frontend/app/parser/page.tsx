
"use client"

import { useState } from 'react';
import { MarkdownStreamParser } from './stream-parser' 

export default function ChatPage() {
  const [content, setContent] = useState("");

  const startChat = async () => {
    setContent(""); // 重置内容
    const parser = new MarkdownStreamParser(); // 使用你写的那个类

    const response = await fetch('/parser/mock');
    const reader = response.body?.getReader();

    if (!reader) return;

    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        parser.flush((text: string) => setContent(prev => prev + text));
        break;
      }
      
      // 调用你的 parser 逻辑
      parser.parse(value, (text: string) => {
        setContent(prev => prev + text);
      });
    }
  };

  return (
    <div className="p-8">
      <button 
        onClick={startChat}
        className="px-4 py-2 bg-blue-500 text-white rounded"
      >
        开始接收流式数据
      </button>
      
      <div className="mt-4 p-4 border rounded bg-gray-50 min-h-[100px]">
        {/* 这里展示解析出的内容 */}
        {content}
      </div>
    </div>
  );
}