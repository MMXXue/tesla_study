
// 模拟后端的数据请求

export async function GET() {
    const encoder = new TextEncoder();
    const mockData = [
        'data: {"content": "你好"}\n\n',
        'data: {"content": "！我"}\n\n',
        'data: {"content": "是一个"}\n\n',
        'data: {"content": "全栈"}\n\n',
        'data: {"content": "工程师"}\n\n',
        'data: {"content": "练习生。"}\n\n',
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