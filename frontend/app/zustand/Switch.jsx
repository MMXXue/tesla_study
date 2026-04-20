
"use client";

import useLightStore from './useLightStore'

function Switch() {
    // 从白板拿走“开关”这个动作
    const toggle = useLightStore((state) => state.toggleLight);

    return (
        <div className="p-8 border-r border-slate-200">
            <button 
                onClick={toggle}
                className="px-6 py-3 bg-blue-600 text-white rounded-full active:scale-95 transition-transform"
            >
                按下开关
            </button>
        </div>
    )
}

export default Switch;