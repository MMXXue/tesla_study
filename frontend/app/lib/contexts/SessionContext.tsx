
"use client"; // Context 必须在客户端运行

import React, { createContext, useContext, useState } from "react";

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
    // 这里就是存数据的地方，即使下面的 Form 销毁了，这里的状态也还在
    const [status, setStatus] = useState("idle");
    const [lastChecked, setLastChecked] = useState("2026-04-23");

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