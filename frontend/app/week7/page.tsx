'use client';

import React, { useEffect, useState, useRef } from 'react';
import * as echarts from 'echarts';

export default function DiagnosticsDashboard() {
    // --- 状态管理：仅用于控制终端文本和连接状态 ---
    const [terminalLogs, setTerminalLogs] = useState<string>("");
    const [inputCommand, setInputCommand] = useState<string>("");
    const [wsStatus, setWsStatus] = useState<"CONNECTING" | "ONLINE" | "OFFLINE">("CONNECTING");

    // --- 引用管理 (useRef)：榨干 Canvas 性能，规避 React 频繁重绘引起的卡顿 ---
    const socketRef = useRef<WebSocket | null>(null);
    const chartContainerRef = useRef<HTMLDivElement | null>(null);
    const chartInstanceRef = useRef<echarts.ECharts | null>(null);
    const terminalScrollRef = useRef<HTMLDivElement | null>(null);

    // 滑动窗口队列：在内存中维护最近 30 次的硬件传感器数据
    const cpuDataQueue = useRef<number[]>([]);
    const timelineQueue = useRef<string[]>([]);

    // ==========================================
    // ⚙️ 核心一：初始化 ECharts 渲染树 
    // ==========================================
    useEffect(() => {
        if (chartContainerRef.current) {
            const chart = echarts.init(chartContainerRef.current, 'dark');
            chartInstanceRef.current = chart;

            chart.setOption({
                backgroundColor: 'transparent',
                title: { text: 'REAL-TIME TELEMETRY MATRIX', textStyle: { color: '#00ff00', fontSize: 12, fontFamily: 'monospace' } },
                tooltip: { trigger: 'axis' },
                xAxis: { type: 'category', data: [], axisLine: { lineStyle: { color: '#333' } } },
                yAxis: { type: 'value', min: 0, max: 100, splitLine: { lineStyle: { color: '#222' } }, axisLine: { lineStyle: { color: '#333' } } },
                series: [{
                    name: 'CPU_LOAD',
                    type: 'line',
                    smooth: true,
                    showSymbol: false,
                    data: [],
                    lineStyle: { color: '#00ff00', width: 2 },
                    areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{ offset: 0, color: 'rgba(0,255,0,0.3)' }, { offset: 1, color: 'transparent' }]) }
                }]
            });
        }

        const handleResize = () => chartInstanceRef.current?.resize();
        window.addEventListener('resize', handleResize);

        return () => {
            window.removeEventListener('resize', handleResize);
            chartInstanceRef.current?.dispose();
        };
    }, []);

    // ==========================================
    // 📡 核心二：打通全双工 WebSocket 网络 (实现分拣分流)
    // ==========================================
    useEffect(() => {
        const connectWebSocket = () => {
            console.log("[+] 正在尝试挂载车载 WebSocket 全双工通道...");
            const ws = new WebSocket("ws://localhost:8000/ws/diagnostics");
            socketRef.current = ws;

            ws.onopen = () => setWsStatus("ONLINE");

            ws.onmessage = (event) => {
                const msg = JSON.parse(event.data);

                // 🌟 分拣器 A：高频遥测数据通过 useRef 增量式直接灌入 Canvas (60FPS)
                if (msg.type === "telemetry") {
                    const nowStr = new Date().toLocaleTimeString([], { hour12: false });
                    
                    cpuDataQueue.current.push(msg.data.cpu);
                    timelineQueue.current.push(nowStr);
                    if (cpuDataQueue.current.length > 30) {
                            cpuDataQueue.current.shift();
                            timelineQueue.current.shift();
                    }

                    // 核心更新：绕过 React state，直接操作 ECharts 实例更新画布
                    chartInstanceRef.current?.setOption({
                            xAxis: { data: timelineQueue.current },
                            series: [{ data: cpuDataQueue.current }]
                        });
                } 
                // 🌟 分拣器 B：AI 文本及系统通知灌入 React State，追加进控制台
                else if (msg.type === "ai_text" || msg.type === "system_status") {
                    setTerminalLogs((prev) => prev + msg.data);
                }
            };

            ws.onclose = () => {
                setWsStatus("OFFLINE");
                setTimeout(connectWebSocket, 3000); // 3秒自动断线重连
            };
        };

        connectWebSocket();

        return () => socketRef.current?.close();
    }, []);

    // ==========================================
    // 📜 核心三：自动触底滚动优化
    // ==========================================
    useEffect(() => {
        if (terminalScrollRef.current) {
            terminalScrollRef.current.scrollTop = terminalScrollRef.current.scrollHeight;
        }
    }, [terminalLogs]);

    // 发送上行控制原语
    const executeCommand = () => {
        if (!inputCommand.trim() || wsStatus !== "ONLINE") return;
        socketRef.current?.send(JSON.stringify({ prompt: inputCommand }));
        setInputCommand("");
    };

    return (
        <div className="min-h-screen bg-black text-green-500 p-6 font-mono flex flex-col justify-between selection:bg-green-500 selection:text-black">
            {/* 头部状态栏 */}
            <header className="border-b border-zinc-800 pb-4 flex justify-between items-center">
                <div>
                    <h1 className="text-xl font-black tracking-widest text-white animate-pulse">TS-79 AI DIAGNOSTIC PANEL</h1>
                    <p className="text-xs text-zinc-500 mt-1">SYSTEM ARCHITECTURE // FULL-DUPLEX WEBSOCKET ENGINE</p>
                </div>
                <div className="flex items-center gap-3 bg-zinc-900 px-4 py-2 border border-zinc-800 rounded-sm">
                    <span className={`h-2.5 w-2.5 rounded-full ${wsStatus === 'ONLINE' ? 'bg-green-500 animate-ping' : 'bg-red-500'}`} />
                    <span className="text-xs tracking-wider text-zinc-400">CORE_LINK: {wsStatus}</span>
                </div>
            </header>

            {/* 核心双屏交互区 */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 my-6 flex-1 items-stretch">
                {/* 左屏：ECharts 实时滚动脉搏 */}
                <div className="lg:col-span-2 border border-zinc-800 bg-zinc-950 p-4 rounded-sm flex flex-col">
                    <div ref={chartContainerRef} className="w-full flex-1 min-h-[300px]" />
                </div>

                {/* 右屏：流式 AI 黑客控制台 */}
                <div className="border border-zinc-800 bg-zinc-950 p-4 rounded-sm flex flex-col justify-between">
                    <div className="text-xs text-zinc-500 border-b border-zinc-900 pb-2 mb-2">
                        [CONSOLE] STREAMING DIAGNOSTIC LOGS
                    </div>
                    <div 
                        ref={terminalScrollRef}
                        className="flex-1 text-zinc-200 text-sm overflow-y-auto leading-relaxed max-h-[280px] pr-2"
                    >
                        <span className="text-zinc-600 font-bold">&gt;_ CHANNEL ACTIVE. AWAITING CONTROL PRIMITIVES...</span>
                        <div className="mt-2 whitespace-pre-wrap">{terminalLogs}</div>
                    </div>
                </div>
            </div>

            {/* 底部指令控制台 */}
            <footer className="flex gap-4 items-center bg-zinc-950 border border-zinc-800 p-3 rounded-sm">
                <span className="text-green-500 font-bold text-lg pl-2">&gt;</span>
                <input
                    type="text"
                    value={inputCommand}
                    onChange={(e) => setInputCommand(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && executeCommand()}
                    disabled={wsStatus !== "ONLINE"}
                    placeholder={wsStatus === "ONLINE" ? "注入诊断控制指令 (例如: run powertrain high-load)" : "正在尝试重连底层通信网关..."}
                    className="flex-1 bg-transparent px-2 py-1 text-green-400 font-mono text-sm focus:outline-none placeholder-zinc-700"
                />
                <button
                    onClick={executeCommand}
                    disabled={wsStatus !== "ONLINE"}
                    className="bg-green-500 hover:bg-green-400 text-black font-black px-6 py-2 text-sm tracking-wider transition-all duration-200 disabled:bg-zinc-800 disabled:text-zinc-600"
                >
                    EXECUTE
                </button>
            </footer>
        </div>
    );
}