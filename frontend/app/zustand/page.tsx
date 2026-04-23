
// 开关灯的实例

import Switch from './Switch'
import Light from './Light'

export default function Page() {
  return (
    // 使用 Tailwind 布局：左边放开关，右边放灯
    <div className="min-h-screen bg-slate-50 flex items-center justify-center">
      <div className="bg-white shadow-2xl rounded-2xl flex overflow-hidden">
        <Switch />
        <Light />
      </div>
    </div>
  )
}