
"use client";

import { motion, AnimatePresence } from "framer-motion";

export function MotionCard() {
    return (
        <motion.div 
            // 1. 初始状态：透明度为0，位置向下偏移 30 像素
            initial={{ opacity: 0, y: 30 }}
            
            // 2. 目标状态：透明度变 1，位置回到原点 (0)
            animate={{ opacity: 1, y: 0 }}
            
            whileHover={{ 
                scale: 1.05,       // 稍微放大一点
                y: -10,            // 往上浮动一点
                boxShadow: "0 20px 25px -5px rgba(0, 0, 0, 0.2)" // 阴影加深，像飘起来了
            }}
            whileTap={{ scale: 0.95 }} // 点下去的时候缩回去，像按下了实体按钮

            // 3. 过渡设置
            transition={{ 
                type: "spring",    // 1. 开启物理引擎
                stiffness: 100,    // 2. 刚度（越高弹得越快，像蹦床）
                damping: 2,       // 3. 阻尼（越低抖动次数越多，越高停得越稳）
                mass: 1            // 4. 质量（数值越大，感觉卡片越重）
            }}
            
            style={{
                width: 200,
                height: 150,
                backgroundColor: "white",
                borderRadius: 12,
                boxShadow: "0 4px 10px rgba(0,0,0,0.1)"
            }}
        >
            <p className = {'text-lg font-medium truncate flex-1 mr-4 text-black'}>这是我的第一个动画卡片</p>
        </motion.div>
    );
}