
"use client";

import { useQuery } from '@tanstack/react-query';

export default function SimpleTest() {
    // 1. 定义一个简单的查数逻辑
    const { data, isLoading } = useQuery({
        queryKey: ['testNumber'],
        queryFn: async () => {
        await new Promise(r => setTimeout(r, 2000)); // 假装很忙，等2秒
        return Math.floor(Math.random() * 100);    // 返回一个随机数
        }
    });

    return (
        <div className="p-20 text-black">
            <h1 className="text-xl">随机任务编号: {isLoading ? "计算中..." : data}</h1>
            <p className="text-gray-500 mt-4">
                技巧：试着切换到别的浏览器标签，再切回来。
                你会发现它【自动】变了！这就是它的自动同步功能。
            </p>
        </div>
    );
}