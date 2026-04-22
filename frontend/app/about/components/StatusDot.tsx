type Status = 'Done' | 'In Progress' | 'Pending' | 'Error';

type StatusDotProps = {
  status: Status;
};

export const StatusDot = ({ status }: StatusDotProps) => {
  const colors = {
    'Done': 'bg-green-500 shadow-[0_0_8px_#22c55e]',
    'In Progress': 'bg-blue-500',
    'Pending': 'bg-gray-500',
    'Error': 'bg-red-500 animate-pulse' // 甚至可以加个报警闪烁
  };

  return <span className={`w-2.5 h-2.5 rounded-full ${colors[status]}`} />;
};