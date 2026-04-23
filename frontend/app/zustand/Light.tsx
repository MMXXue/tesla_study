
"use client";

import useLightStore from './useLightStore'

function Light() {
    // 从白板拿走“灯的状态”这个数据
    const isOn = useLightStore((state) => state.isLightOn);

    return (
        <div className="p-8 flex flex-col items-center">
        {/* 根据 isOn 的真假，切换 Tailwind 的颜色类名 */}
            <div className={`w-20 h-20 rounded-full transition-all duration-500 ${
                isOn ? 'bg-yellow-400 shadow-[0_0_50px_rgba(250,204,21,0.8)]' : 'bg-slate-300'
            }`} />
            <p className="mt-4 font-bold text-slate-600">
                现在灯是：{isOn ? '亮着的' : '灭的'}
            </p>
        </div>
    )
}

// 必须有这一行，表示把这个组件“导出去”供别人使用
export default Light;