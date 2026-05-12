
// 模拟后端的数据请求

export async function GET() {
    const encoder = new TextEncoder();
    const mockData = [
        'data: {"content": "# 全栈 AI 挑战测试\\n\\n"}\n\n',
        'data: {"content": "正在启动性能压力测试...\\n\\n"}\n\n',
        'data: {"content": "### 1. 布局稳定性测试\\n"}\n\n',
        'data: {"content": "这是一个超长字符测试，用来检测你的 `break-words` 类名是否能防止容器被撑开：\\n"}\n\n',
        'data: {"content": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\\n\\n"}\n\n',
        'data: {"content": "### 2. 自动滚动压力测试\\n"}\n\n',
        'data: {"content": "接下来的每一行都会触发一次 `useEffect`。如果你的 `isAutoScroll` 逻辑正确，页面会丝滑触底。\\n\\n"}\n\n',
        // 循环生成 20 行数据，确保产生滚动条
        ...Array.from({ length: 50 }).map((_, i) => 
            `data: {"content": "这是自动生成的第 ${i + 1} 行测试数据，观察滚动条是否在平稳下降。\\n"}\n\n`
        ),
        'data: {"content": "\\n### 3. 最终检测\\n"}\n\n',
        'data: {"content": "如果你能看到这一行，并且：\\n"}\n\n',
        'data: {"content": "1. 页面没有横向晃动\\n"}\n\n',
        'data: {"content": "2. 你手动向上滚时，没有被强行拽回底部\\n"}\n\n',
        'data: {"content": "3. 点击“回到底部”按钮能瞬间复位\\n\\n"}\n\n',
        'data: {"content": "**恭喜你，Day 46 任务彻底达成！**"}\n\n',
        'data: [DONE]\n\n',
    ];

    const stream = new ReadableStream({
        async start(controller) {
            for (const chunk of mockData) {
                // 模拟网络延迟，每 200ms 发送一个片段
                await new Promise((r) => setTimeout(r, 200));
                controller.enqueue(encoder.encode(chunk));
            }
            controller.close();
        },
    });

    return new Response(stream, {
        headers: { 'Content-Type': 'text/event-stream' },
    });
}