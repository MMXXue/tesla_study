
// Schema 是纯逻辑代码，不涉及 UI 渲染，放在 lib (library) 里非常合适。

import { z } from "zod";

// 1. 定义 Schema
export const agentSchema = z.object({
    // 名字必须是字符串，且至少 2 个字符
    name: z.string().min(2, "Agent 名字太短了，至少需要 2 个字符").optional(),
    
    // 角色定位，限制只能从这几个选项中选
    role: z.enum(["translator", "coder", "writer"]).optional(),

    // 创造力参数：必须是 0 到 1.2 之间的数字
    temperature: z.string().min(0).max(1.2, "创造力不能超过 1.2").optional(),
});

// 2. 导出类型 (供后面 React 组件使用)
export type AgentFormValues = z.infer<typeof agentSchema>;