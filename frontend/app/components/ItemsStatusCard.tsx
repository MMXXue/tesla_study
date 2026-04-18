
import { Play, AlertTriangle, Moon, LucideIcon } from 'lucide-react';

// 定义状态类型，方便复用
type DeviceStatus = 'Activate' | 'Error' | 'Pending';

interface ItemsStatusCardProps {
    deviceId: string;
    status: DeviceStatus;
    healthy: number | string; // 建议支持数字
    temperature: number | string;
    battery: number | string;
}

interface StatusConfig {
    icon: LucideIcon;
    color: string;
    bg: string;
    label: string;
}

export function ItemsStatusCard({deviceId, status, healthy, temperature, battery}: ItemsStatusCardProps){
    // 显式定义 Record 类型，确保 key 覆盖了所有状态
    const configs: Record<DeviceStatus, StatusConfig> = {
        Pending: { 
            icon: Moon, 
            color: 'text-slate-400', 
            bg: 'bg-slate-900/50', 
            label: 'Standby' 
        },
        Activate: { 
            icon: Play, 
            color: 'text-emerald-400', 
            bg: 'bg-emerald-900/20', 
            label: 'Running'
        },
        Error: { 
            icon: AlertTriangle, 
            color: 'text-rose-500', 
            bg: 'bg-rose-900/30', 
            label: 'System Failure'
        }
    };

    // 1. 增加安全性检查：如果 status 不在 configs 中，使用 Pending 作为默认值
    const config = configs[status] || configs.Pending; 
    
    // 2. 现在 config 绝对不会是 undefined，读取 icon 也就安全了
    const Icon = config.icon;

    return (
        <div className={`rounded-xl p-4 border border-white/10 ${config.bg} transition-all`}>
            <div className="flex justify-between items-start mb-4">
                <div>
                    <h3 className="text-xl font-medium text-slate-400 uppercase tracking-wider">
                        {deviceId}
                    </h3>
                    <p className={`text-xs font-bold mt-1 ${config.color}`}>
                        {config.label}
                    </p>
                </div>
                <div className={`${config.color} p-2 rounded-lg bg-black/20`}>
                    <Icon size={24} strokeWidth={2.5} />
                </div>
            </div>

            <div className="flex gap-4 items-end">
                <div>
                    <span className="text-2xl font-bold text-white">{healthy}</span>
                    <span className="text-sm text-slate-500 ml-1">%</span>
                    <p className="text-[10px] text-slate-500 uppercase">Health</p>
                </div>
                <div className="border-l border-white/10 pl-4">
                    <span className="text-2xl font-bold text-white">{temperature}</span>
                    <span className="text-sm text-slate-500 ml-1">°C</span>
                    <p className="text-[10px] text-slate-500 uppercase">Temp</p>
                </div>
                <div className="border-l border-white/10 pl-4">
                    <span className="text-2xl font-bold text-white">{battery}</span>
                    <span className="text-sm text-slate-500 ml-1">%</span>
                    <p className="text-[10px] text-slate-500 uppercase">Battery</p>
                </div>
            </div>
        </div>
    );
}