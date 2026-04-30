import ErrorBoundary from '../components/ErrorBoundary';
import Bomb from './Bomb';

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      {/* 顶部标题栏 */}
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">工业设备监控系统</h1>
        <p className="text-gray-500">Day 43: 故障容错与错误边界处理实战</p>
      </header>

      <div className="grid grid-cols-12 gap-6">
        
        {/* 左侧：系统状态 (正常组件) */}
        <div className="col-span-4 space-y-6">
          <section className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <h3 className="text-lg font-semibold mb-4 flex items-center">
              <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
              系统核心服务
            </h3>
            <ul className="space-y-3 text-sm text-gray-600">
              <li className="flex justify-between"><span>数据库连接</span> <span className="text-green-600 font-medium">运行中</span></li>
              <li className="flex justify-between"><span>API 网关</span> <span className="text-green-600 font-medium">运行中</span></li>
            </ul>
          </section>
        </div>

        {/* 右侧：动态监测区 (包含潜在崩溃风险的组件) */}
        <div className="col-span-8">
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 min-h-[400px]">
            <h3 className="text-lg font-semibold mb-6">实时诊断面板</h3>
            
            <div className="grid grid-cols-2 gap-6">
              {/* 正常的监测组件 */}
              <div className="p-4 bg-blue-50 rounded-xl border border-blue-100">
                <h4 className="font-medium text-blue-800 mb-2">电池健康度</h4>
                <div className="text-2xl font-bold text-blue-900">98%</div>
              </div>

              {/* 【实验区】被错误边界保护的炸弹组件 */}
              <ErrorBoundary>
                <Bomb />
              </ErrorBoundary>
            </div>

            <div className="mt-8 p-4 bg-gray-50 rounded-xl text-xs text-gray-400 italic">
              提示：上方的“实时监控模块”是一个故意制造崩溃的组件。
              由于它被 ErrorBoundary 包裹，它的崩溃不会导致左侧的“系统核心服务”或整个页面消失。
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}