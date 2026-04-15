
// src/components/StatusCard.tsx

import { StatusDot } from './StatusDot';

interface StatusCardProps {
  title: string;
  status: 'Done' | 'In Progress' | 'Pending' | 'Error'; // 严格限定状态类型
}

export default function StatusCard({ title, status }: StatusCardProps) {
  return (
    <div className="p-4 md:p-6 bg-white/5 border border-white/10 rounded-xl hover:border-white/30 hover:-translate-y-1 transition-all shadow-xl">
      <div className="flex justify-between items-center">
        {/* 使用了我们昨天学的 flex-1 和 truncate */}
        <span className="text-lg font-medium truncate flex-1 mr-4 text-white">
          {title}
        </span>
        {/* 使用刚才定义的原子组件 */}
        <StatusDot status={status} />
      </div>
      
      <p className="mt-4 text-[10px] text-gray-500 uppercase tracking-[0.2em]">
        System Status: {status}
      </p>
    </div>
  );
}