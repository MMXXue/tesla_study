import { Zap, AlertCircle, Activity, ArrowUpRight, ArrowDownRight } from 'lucide-react';

interface StatsGridProps {
    activeRate: string;
    errorCount: number;
    avgTemp: number;
}

export function StatsGrid({ activeRate, errorCount, avgTemp }: StatsGridProps) {
    const stats = [
        {
            label: "今日开机率",
            value: activeRate,
            icon: Zap,
            color: "text-emerald-400",
            bg: "bg-emerald-500/10",
            trend: "+0.2%",
            isPositive: true
        },
        {
            label: "故障设备数",
            value: errorCount.toString().padStart(2, '0'),
            icon: AlertCircle,
            color: "text-rose-500",
            bg: "bg-rose-500/10",
            trend: errorCount > 0 ? `+${errorCount}` : "0",
            isPositive: errorCount === 0
        },
        {
            label: "系统平均温度",
            value: `${avgTemp}°C`,
            icon: Activity,
            color: "text-sky-400",
            bg: "bg-sky-500/10",
            trend: "-2°C",
            isPositive: true
        }
    ];

    return (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {stats.map((stat, index) => (
                <div key={index} className="bg-slate-900/40 border border-white/5 p-6 rounded-2xl relative overflow-hidden group hover:border-white/10 transition-colors">
                    <div className="flex justify-between items-start relative z-10">
                        <div>
                            <p className="text-slate-500 text-xs font-bold uppercase tracking-widest">{stat.label}</p>
                            <h3 className="text-3xl font-mono font-bold text-white mt-2">{stat.value}</h3>
                        </div>
                        <div className={`p-3 rounded-xl ${stat.bg} ${stat.color}`}>
                            <stat.icon size={24} />
                        </div>
                    </div>
                    <div className="mt-4 flex items-center text-xs relative z-10">
                        {stat.isPositive ? (
                            <ArrowUpRight size={14} className="text-emerald-400 mr-1" />
                        ) : (
                            <ArrowDownRight size={14} className="text-rose-400 mr-1" />
                        )}
                        <span className={stat.isPositive ? "text-emerald-400" : "text-rose-400"}>
                            {stat.trend}
                        </span>
                        <span className="text-slate-600 ml-2 font-medium text-[10px] uppercase">vs 前一小时</span>
                    </div>
                    {/* 背景装饰光晕 */}
                    <div className={`absolute -right-8 -bottom-8 size-32 rounded-full opacity-[0.03] blur-3xl ${stat.bg}`} />
                </div>
            ))}
        </div>
    );
}