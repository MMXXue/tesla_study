"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

export function ToggleCard() {
    const [isVisible, setIsVisible] = useState(true);

    return (
        <div>
        <button onClick={() => setIsVisible(!isVisible)}>显示 / 隐藏</button>
            {/* 必须用 AnimatePresence 包裹条件渲染的部分 */}
            <AnimatePresence>
                {isVisible && (
                // 翻译：
                // "isVisible 是 true 吗？" 
                // "如果是，那就把括号里的 <motion.div /> 渲染出来。"
                // "如果不是，那就当我没写过这段代码。"
                    <motion.div
                        initial={{ opacity: 0, scale: 0.8 }} // 入场开始
                        animate={{ opacity: 1, scale: 1 }}   // 入场结束
                        
                        // --- 这一关的重点 ---
                        exit={{ opacity: 0, scale: 0.5, transition: { duration: 0.2 } }} 
                        // -------------------
                        
                        style={{ width: 100, height: 100, background: "blue" }}
                    />
                )}
            </AnimatePresence>
        </div>
    );
}