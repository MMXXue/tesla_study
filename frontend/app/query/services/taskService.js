
// 负责拿数据

/**
 * 模拟从远程服务器获取 AI 学习任务
 * 这是一个异步函数 (async)，因为它需要等待网络响应
 */
export const getStudyTasks = async () => {
    console.log("📡 正在连接 Tesla AI 任务服务器...");

    // 1. 模拟网络延迟 (1.5秒)
    // 在真实场景中，这里是 fetch('https://api.example.com/tasks')
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // 2. 模拟服务器返回的数据包
    const mockData = [
        { id: 1, task: "Zustand 状态持久化", status: "Done", difficulty: "Medium" },
        { id: 2, task: "React Query 环境搭建", status: "Done", difficulty: "Hard" },
        { id: 3, task: "异步数据同步实战", status: "In Progress", difficulty: "Extreme" },
    ];

    // 3. 模拟成功获取
    console.log("✅ 成功获取远程数据！");
    return mockData;
};


// 我们要模拟一个发送给服务器的请求
export const updateTaskStatus = async (taskId, newStatus) => {
    console.log(`正在同步服务器：任务 ${taskId} 状态更新为 ${newStatus}...`);
    
    // 模拟网络延迟
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 模拟随机失败（可选，用来测试系统的健壮性）
    if (Math.random() < 0.1) throw new Error("服务器拒绝了请求");

    return { success: true, taskId, newStatus };
};