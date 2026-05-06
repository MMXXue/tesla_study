
// 第一步
// 创建一个专门存放角色信息的 store

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { z } from 'zod';

// 1. 定义角色模型：使用 Zod 确保角色只能是这三个字符串之一
export const RoleSchema = z.enum(['Agent', 'Admin', 'Maintainer']);
export type Role = z.infer<typeof RoleSchema>;  // 这是 Zod 提供的一个工具。它会分析传入的“指纹”，算出它代表的具体类型是什么。

interface RoleState {
  role: Role;
  // 动作：切换角色
  setRole: (newRole: Role) => void;
}

// 2. 创建 Store 并集成 Persist 中间件实现数据持久化
export const useRoleStore = create<RoleState>()(
  persist(
    (set) => ({
      role: 'Agent', // 初始默认角色
      setRole: (newRole) => {
        // 在赋值前进行逻辑校验
        const validatedRole = RoleSchema.parse(newRole); // 确保传进来的字符串合法
        set({ role: validatedRole });
      },
    }),
    {
      name: 'tesla-role-storage', // 存储在 localStorage 中的 key
    }
  )
);