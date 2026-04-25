
"use client"; // Context 必须在客户端运行

import React, { createContext, useContext, useState, useEffect } from "react";

// 1. 定义我们要共享的数据“形状”
interface SessionContextType {
    status: string;        // 告诉大家：现在是闲置、扫描中还是出错了
    setStatus: (s: string) => void; // 这是一个“遥控器按钮”，允许别人修改状态
    lastChecked: string;   // 记录上次检查的时间，全厂都要看这个    只有数据，没有改数据的函数
}



// 2. 初始化电台
// createContext: 这是 React 提供的工具，用来创建一个“信道”
// 括号里的 undefined 是默认值，意思是如果收不到信号，就返回空
// (undefined): 这是电台的默认状态。如果没有人发射信号，收音机里听到的就是静音。
const SessionContext = createContext<SessionContextType | undefined>(undefined);



// 建立“发射塔” (Provider)
// Provider 是一个特殊的组件。被它包裹住的子组件，才能收到信号。
export function SessionProvider({ children }: { children: React.ReactNode }) {
    // // 1. 初始化时：尝试从 LocalStorage 读数据
    // const [status, setStatus] = useState("idle");
    // const [lastChecked, setLastChecked] = useState("尚未检查");

    // 1. 初始状态统一设为基础值（确保服务器和浏览器第一眼看的一样）
    const [status, setStatus] = useState("idle");
    const [lastChecked, setLastChecked] = useState("尚未检查");
    const [isLoaded, setIsLoaded] = useState(false); // 新增：加载锁

    // 2. 只在页面挂载后的“第一次”去读硬盘
    useEffect(() => {
        const savedStatus = localStorage.getItem("ai_session_status");
        const savedTime = localStorage.getItem("ai_session_time");
        
        if (savedStatus) setStatus(savedStatus);
        if (savedTime) setLastChecked(savedTime);
        
        setIsLoaded(true); // 读完了，开锁
    }, []);

    // 3. 持续监听：只要状态变了，就存入硬盘
    // 当 status 变化时，自动存入 LocalStorage
    // 要利用 useEffect 这个“监控器”。只要 status 或 lastChecked 变了，它就自动往浏览器的“抽屉”（LocalStorage）里塞一份。
    useEffect(() => {
        if (isLoaded) { // 只有加载完成后才允许写入，防止初始值覆盖旧数据
            localStorage.setItem("ai_session_status", status);
            localStorage.setItem("ai_session_time", lastChecked);
            console.log("已保存状态到硬盘:", status);
        }
    }, [status, lastChecked, isLoaded]);

    return (
        // value 属性里放的就是要广播出去的信号
        <SessionContext.Provider value={{ status, setStatus, lastChecked }}>
            {children} 
        </SessionContext.Provider>
    );
}



// 制造“收音机” (useContext)
// 为了让子组件用起来更方便，我们通常会写一个自定义的 Hook，像拿对讲机一样简单。
export function useSession() {
    // 1. 拿起收音机，调到 SessionContext 这个频率
    const context = useContext(SessionContext);
    
    // 2. 安全锁（Senior 工程师必备逻辑）
    if (!context) {
        throw new Error("报警！你正在发射塔覆盖范围之外使用收音机。");
    }
    
    // 3. 吐出信号，供组件使用
    return context;
}