
"use client";

import { motion } from 'framer-motion';
import { useState }  from "react";

export default function LayoutCard() {
    const [isBig, setIsBig] = useState(false);

    return (
        <div className="p-10">
            <button 
                onClick={() => setIsBig(!isBig)}
                className="mb-4 p-2 bg-blue-500 text-white rounded"
                >
                切换大小
            </button>

            {/* 这个 div 加上了 layout 属性 */}
            <motion.div
                layout
                style={{
                width: isBig ? "300px" : "100px",
                height: isBig ? "200px" : "100px",
                backgroundColor: "#ff0055",
                borderRadius: "10px"
                }}
            />
        </div>
    );
}