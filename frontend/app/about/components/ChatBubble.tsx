
// src/components/ChatBubble.tsx

type Role = 'user' | 'assistant';

interface ChatBubbleProps {
  content: string;
  role: Role;
}

export default function ChatBubble({ content, role }: ChatBubbleProps) {
  // 根据角色决定布局：用户在右（blue），AI在左（gray）
  const isUser = role === 'user';

  return (
    <div className={`flex w-full mb-4 ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`
        max-w-[80%] px-4 py-2 rounded-2xl text-sm
        ${isUser 
          ? 'bg-blue-600 text-white rounded-tr-none' // 用户：蓝底，右上角是尖的
          : 'bg-white/10 text-gray-200 rounded-tl-none border border-white/10' // AI：暗色底，左上角是尖的
        }
      `}>
        {content}
      </div>
    </div>
  );
}