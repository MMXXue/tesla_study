
// 手搓的parser

class MarkdownStreamParser {
    constructor() {
        this.buffer = '';
        this.decoder = new TextDecoder('utf-8');
    }

    /**
     * @param {Uint8Array} chunk 
     * @param {Function} onMessage 解析出完整消息后的回调
     */
    parse(chunk, onMessage) {
        // 1. 解码并追加，{ stream: true } 处理跨 Chunk 的字节截断
        this.buffer += this.decoder.decode(chunk, { stream: true });

        // 2. 按 SSE 规范切割
        const lines = this.buffer.split('\n\n');

        // 3. 弹出不完整的尾巴存回 buffer
        this.buffer = lines.pop() || '';

        for (const line of lines) {
            const target = line.trim();
            if (target.startsWith('data: ')) {
                const content = target.substring(6);
                if (content === '[DONE]') continue;
                
                // 尝试解析 JSON 或返回纯文本
                try {
                    const json = JSON.parse(content);
                    onMessage(json.content || json);
                } catch (e) {
                    onMessage(content);
                }
            }
        }
    }
}