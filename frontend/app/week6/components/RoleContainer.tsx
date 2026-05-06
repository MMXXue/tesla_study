
// 第二步
// 带动画的切换容器

'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { useRoleStore, Role } from '../store/useRoleStore';

const AgentView = () => (
    <div className='p-6 rounded-2xl bg-blue-500/10 border border-blue-500/30 backdrop-blur-md'>
        <h3 className='text-blue-400 font-bold mb-2'>Agent Console</h3>
        <p className='text-grey-300 text-sm'>正在同步 AI 诊断对话上下文</p>
        <div className='mt-4 flex gap-2'>
            <div className='w-2 h-2 rounded-full bg-blue-500 animate-pulse' />
            <div className='text-xs text-blue-300/70'>Neural Link Active</div>
        </div>
    </div>
);

const AdminView = () => (
    <div className='p-6 rounded-2xl bg-purple-500/10 border border-purple-500/30 backdrop-blur-md'>
        <h3 className='text-purple-400 font-bold mb-2'>Admin Dashboard</h3>
        <p className='text-grey-300 text-sm'>全局用户偏好与设备实时状态已就绪</p>
        <div className='mt-4 grid grid-cols-2 gap-4'>
            <div className='h-12 bg-purple-500/20 rounded-lg border border-purple-500/20'></div>
            <div className='h-12 bg-purple-500/20 rounded-lg border border-purple-500/20'></div>
        </div>
    </div>
);

const MaintainerView = () => (
    <div className='p-6 rounded-2xl bg-orange-500/10 border border-orange-500/30 backdrop-blur-md'>
        <h3 className='text-orange-400 font-bold mb-2'>Maintainer Tools</h3>
        <p className='text-grey-300 text-sm'>正在监控 Error Boundary,确保单体组件崩溃不影响全局</p>
        <div className='mt-4 h-16 w-full bg-orange-500/10 border-t-2 border-orange-500/10 flex items-center justify-center text-xs text-orange-200'>
            SYSTEM FAULT TOLERANCE: 100%
        </div>
    </div>
);

export default function RoleContainer() {
    const { role } = useRoleStore();

    return (
        <div className="relative w-full mt-8">
        {/* mode="wait" 确保旧组件完全消失后，新组件才进入 */}
            <AnimatePresence mode="wait">
                <motion.div
                    key={role} // 必须绑定 key，role 变化时 Framer Motion 才知道要执行动画
                    initial={{ opacity: 0, y: 10 }} // 初始状态：透明且向下偏一点
                    animate={{ opacity: 1, y: 0 }}  // 动画状态：显示且回到原位
                    exit={{ opacity: 0, y: -10 }}  // 退出状态：透明且向上偏一点
                    transition={{ duration: 0.3 }} // 动画持续 0.3 秒
                >
                    {role === 'Agent' && <AgentView />}
                    {role === 'Admin' && <AdminView />}
                    {role === 'Maintainer' && <MaintainerView />}
                </motion.div>
            </AnimatePresence>
        </div>
    );
}