
// React Hook Form (UI 组件)

"use client"; // 这行非常重要！Next.js 默认所有组件都是在服务器跑的，但表单需要用户的交互，所以必须声明它是客户端组件。

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { agentSchema, AgentFormValues } from "../lib/schemas/agentSchema";

export default function AgentConfigForm() {
  // 这是今天最核心的一行
  const { 
    register,          // 就像贴纸，贴在输入框上，用来收集数据
    handleSubmit,      // 一个包装函数，它会先让 Zod 校验，通过了才会执行你自己的提交逻辑
    formState: { errors } // 这是一个“错误账本”，如果校验失败，错误信息会自动出现在这里
  } = useForm<AgentFormValues>({
    resolver: zodResolver(agentSchema), // 告诉管家：校验规则请看 agentSchema
  });

  // 校验通过后才会运行的函数
  const onSubmit = (data: AgentFormValues) => {
    console.log("最终提交的数据:", data);
    alert("创建成功！");
  };

  return (
    // 下面开始写 HTML 结构
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {/* 待会儿我们在这里填入输入框 */}
      <div>
        <label>Agent 名称：</label>
        {/* {...register("name")} 是精髓。它把这个输入框和 Schema 里的 "name" 绑定了 */}
        <input {...register("name")} className="border p-2 block w-full" />
        
        {/* 如果 Schema 校验没通过，这里就会显示错误提示 */}
        {errors.name && <p className="text-red-500 text-sm">{errors.name.message}</p>}
      </div>
      <div>
        <label>Agent 角色：</label>
        <select {...register("role")} className="border p-2 block w-full">
          <option value="">请选择...</option>
          <option value="translator">翻译官</option>
          <option value="coder">程序员</option>
          <option value="writer">作家</option>
        </select>
        {errors.role && <p className="text-red-500 text-sm">{errors.role.message}</p>}
      </div>
      <div>
        <label>Agent 温度: </label>
        <input {...register("temperature")} className="border p-2 block w-full" />
        {errors.temperature && <p className="text-red-500 text-sm">{errors.temperature.message}</p>}
      </div>

       {/* 关键：添加提交按钮 */}
      <button 
        type="submit" 
        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg transition-colors"
      >
        立即创建 Agent
      </button>
    </form>
  );
}