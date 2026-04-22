
"use client"

import React, { useState } from 'react';
import { Play, AlertTriangle, Moon, Settings, RefreshCcw } from 'lucide-react';

export const DeviceCard = () => {
    // 模拟设备状态: 'idle', 'active', 'error'
    const [status, setStatus] = useState< 'idle' | 'active' | 'error' >('idle');

    const configs = {
        idle: { 
        icon: Moon, 
        color: 'text-slate-400', 
        bg: 'bg-slate-900/50', 
        label: 'Standby' ,
        animate: ' '
        },
        active: { 
            icon: Play, 
            color: 'text-emerald-400', 
            bg: 'bg-emerald-900/20', 
            label: 'Running',
            animate: 'animate-pulse' 
        },
        error: { 
            icon: AlertTriangle, 
            color: 'text-rose-500', 
            bg: 'bg-rose-900/30', 
            label: 'System Failure',
            animate: 'animate-bounce' 
        }
    };

    const CurrentIcon = configs[status].icon;

    return (
        <div className={`p-6 rounded-2xl border transition-all duration-500 ${configs[status].bg} border-white/10 w-64`}>
            <div className="flex justify-between items-start mb-8">
                <div className={`p-3 rounded-xl bg-black/40 ${configs[status].color} ${configs[status].animate}`}>
                    <CurrentIcon size={28} strokeWidth={2.5} />
                </div>
                
                <Settings className="text-slate-600 hover:rotate-90 transition-transform cursor-pointer" size={20} />
            </div>
            
            <div>
                <h3 className="text-white font-bold text-lg leading-none">{configs[status].label}</h3>
                <p className="text-slate-500 text-sm mt-2">Device ID: TX-7240</p>
            </div>

            {/* 模拟状态切换按钮 */}
            <div className="mt-6 flex gap-2">
                {(['idle', 'active', 'error'] as const) .map(s => (
                    <button 
                        key={s}
                        onClick={() => setStatus(s)}
                        className="px-2 py-1 text-xs rounded bg-white/5 text-slate-300 hover:bg-white/10 capitalize"
                    >
                        {s}
                    </button>
                    ))
                }
            </div>
        </div>
    );
};