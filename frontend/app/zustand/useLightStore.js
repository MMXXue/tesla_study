
// 创建你的“中央情报局” (Store)
// Zustand 白板

import { create } from 'zustand';

const useLightStore = create ((set) => ({
    isLightOn: false,

    toggleLight: () => set((state) => ({isLightOn: !state.isLightOn}))
}))

export default useLightStore;