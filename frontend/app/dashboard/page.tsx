import { ItemsStatusCard } from "./components/ItemsStatusCard";
import { StatsGrid } from "./components/StatsGrid";


export default function DashBoard() {
    // 1. 模拟数据源（你可以根据需要在这里添加更多设备）
    const devices = [
        { deviceId: 'FANUC-R2000', status: 'Activate' as const, healthy: 98, temperature: 42, battery: 85 },
        { deviceId: 'KUKA-KR60', status: 'Error' as const, healthy: 45, temperature: 78, battery: 12 },
        { deviceId: 'ABB-IRB6700', status: 'Pending' as const, healthy: 100, temperature: 30, battery: 95 },
        { deviceId: 'TESLA-GIGA-01', status: 'Activate' as const, healthy: 92, temperature: 38, battery: 70 },
        { deviceId: 'TESLA-GIGA-02', status: 'Activate' as const, healthy: 95, temperature: 39, battery: 65 },
        { deviceId: 'FANUC-M710', status: 'Pending' as const, healthy: 88, temperature: 35, battery: 40 },
    ];

    // 2. --- 自动化统计逻辑 ---
    // 计算总数
    const totalCount = devices.length;
    // 计算正常运行数
    const activeCount = devices.filter(d => d.status === 'Activate').length;
    // 计算故障数
    const errorCount = devices.filter(d => d.status === 'Error').length;
    
    // 计算开机率 (百分比字符串)
    const activeRate = totalCount > 0 ? ((activeCount / totalCount) * 100).toFixed(1) + "%" : "0%";
    
    // 计算系统平均温度 (取所有设备温度的平均值)
    const avgTemp = Math.round(
        devices.reduce((acc, curr) => {
            const tempValue = typeof curr.temperature === 'number' ? curr.temperature : parseFloat(curr.temperature);
            return acc + tempValue;
        }, 0) / totalCount
    );

    return (
        // 页面背景采用极深色，符合工业看板审美
        <main className="min-h-screen bg-[#050505] text-slate-300 p-6 lg:p-12">
            <div className="max-w-[1600px] mx-auto">
                
                {/* --- 顶部标题栏 --- */}
                <header className="mb-12 flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-white/5 pb-8">
                    <div>
                        <h1 className="text-4xl font-extralight tracking-[0.3em] text-white uppercase italic">
                            Tesla <span className="font-bold not-italic">Giga</span> Management
                        </h1>
                        <p className="text-slate-500 text-xs mt-2 tracking-widest font-mono">
                            ASSET MONITORING SYSTEM // NODE_SYD_01
                        </p>
                    </div>
                    <div className="flex flex-col items-end">
                        <div className="flex items-center gap-2">
                            <div className="size-2 bg-emerald-500 rounded-full animate-pulse shadow-[0_0_8px_#10b981]" />
                            <span className="text-[10px] text-emerald-500 uppercase font-bold tracking-widest">
                                Live Feed Connected
                            </span>
                        </div>
                        <p className="text-[10px] text-slate-600 font-mono mt-1">
                            LAST UPDATED: {new Date().toLocaleTimeString()}
                        </p>
                    </div>
                </header>

                {/* --- 核心统计网格 (StatsGrid) --- */}
                <section className="mb-16">
                    <StatsGrid 
                        activeRate={activeRate} 
                        errorCount={errorCount} 
                        avgTemp={avgTemp} 
                    />
                </section>

                {/* --- 设备详细清单 (ItemsStatusCard 列表) --- */}
                <section>
                    <div className="flex items-center justify-between mb-8">
                        <h2 className="text-sm font-bold uppercase tracking-widest text-slate-400">
                            设备资产实时清单
                        </h2>
                        <div className="px-3 py-1 bg-white/5 rounded-full border border-white/5 text-[10px] font-mono text-slate-500 uppercase tracking-tighter">
                            Total Nodes: {totalCount.toString().padStart(2, '0')}
                        </div>
                    </div>

                    {/* 响应式栅格系统：手机1列，平板2列，笔记本3列，超大屏6列 */}
                    <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-6">
                        {devices.map(item => (
                            <ItemsStatusCard
                                key={item.deviceId}
                                deviceId={item.deviceId}
                                status={item.status}
                                healthy={item.healthy}
                                temperature={item.temperature}
                                battery={item.battery} 
                            />
                        ))}
                    </div>
                </section>
            </div>
        </main>
    );
}