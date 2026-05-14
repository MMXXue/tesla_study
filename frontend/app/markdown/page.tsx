
"use client";

import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import rehypeHighlight from 'rehype-highlight';

// 必须引入的外部样式
import 'katex/dist/katex.min.css'; // 数学公式样式
import 'highlight.js/styles/github-dark.css'; // 代码高亮样式

const initialContent = `# Day 47: 智能 Markdown 预览器 🚀

## 1. 工业级表格 (GFM)
使用 \`remark-gfm\` 插件支持的专业表格：

| 模块 | 功能 | 状态 |
| :--- | :--- | :---: |
| 解析器 | React Markdown | ✅ |
| 公式 | LaTeX (KaTeX) | ✅ |
| 样式 | Tailwind Prose | ✅ |

## 2. 数学公式 (Math)
这是行内公式：$E = mc^2$。

这是块级公式（质能方程的完整形式）：
$$E^2 = (mc^2)^2 + (pc)^2$$

## 3. 代码高亮 (Highlight)
\`\`\`javascript
function geminiWelcome() {
  console.log("你好！这是实时渲染的代码块");
}
\`\`\`

> **提示**：左边输入，右边实时同步样式。
`;

export default function MarkdownPreview() {
  const [content, setContent] = useState(initialContent);

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-8">
      <div className="max-w-7xl mx-auto flex flex-col lg:flex-row gap-6">
        
        {/* 左侧：输入编辑区 */}
        <div className="flex-1">
          <label className="block mb-2 text-sm font-bold text-gray-700">Markdown 编辑器</label>
          <textarea
            className="w-full h-[70vh] p-4 text-sm font-mono border border-gray-300 rounded-xl shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="在这里输入 Markdown..."
          />
        </div>

        {/* 右侧：实时预览区 */}
        <div className="flex-1">
          <label className="block mb-2 text-sm font-bold text-gray-700">实时预览</label>
          <div className="w-full h-[70vh] p-6 bg-white border border-gray-300 rounded-xl shadow-sm overflow-y-auto">
            {/* 这里的 prose 是关键：它让 Tailwind 自动美化 Markdown 标签 */}
            <article className="prose prose-slate max-w-none prose-table:border prose-th:bg-gray-50 prose-th:px-4 prose-td:px-4">
              <ReactMarkdown
                remarkPlugins={[remarkGfm, remarkMath]}
                rehypePlugins={[rehypeKatex, rehypeHighlight]}
              >
                {content}
              </ReactMarkdown>
            </article>
          </div>
        </div>

      </div>
    </div>
  );
}