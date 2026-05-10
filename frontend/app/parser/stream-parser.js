
/**
 * 进阶版流式解析器
 * 核心设计目标：高性能、容错性、兼容多种 SSE 变体
 */

class MarkdownStreamParser {
    constructor() {
        // 缓冲区：存储尚未凑成完整一行的字符串片段
        this.buffer = '';
        // 文本解码器：将后端的二进制字节流(Uint8Array)转换为字符串
        this.decoder = new TextDecoder('utf-8');
    }

    /**
     * @param {Uint8Array} chunk - 浏览器 fetch 读到的原始字节块
     * @param {Function} onMessage - 成功解析出内容片段时的回调函数
     */
    parse(chunk, onMessage) {
        /**
         * 1. 解码字节流
         * { stream: true } 非常重要！
         * 如果一个 UTF-8 字符（如 Emoji 🦁）被拆分在两个 chunk 中，
         * decoder 会自动保留残缺字节，等下一个 chunk 凑齐后再解码。
         */
        this.buffer += this.decoder.decode(chunk, { stream: true });

        /**
         * 2. 循环提取“行”
         * 为什么不直接 split('\n')？
         * 因为 split 会一次性创建大量子字符串数组，在大文件流下非常耗内存。
         * 使用 indexOf + slice 是更高效的“指针滑动”策略。
         */
        let lineEndIndex;
        // 只要 buffer 里还有换行符，说明至少有一行完整数据可以处理
        while ((lineEndIndex = this.buffer.indexOf('\n')) !== -1) {
            
            // 提取从开头到换行符的内容，并去除首尾空格
            const line = this.buffer.slice(0, lineEndIndex).trim();
            
            // 【关键】更新缓冲区：把已经处理过的这行连同换行符一起删掉
            this.buffer = this.buffer.slice(lineEndIndex + 1);

            // 3. SSE 协议校验：标准格式必须以 "data: " 开头
            if (line.startsWith('data: ')) {
                // 剪掉前 6 个字符，获取核心载荷
                const content = line.slice(6);

                // 如果是 SSE 的结束信号，直接退出
                if (content === '[DONE]') return;

                try {
                    // 4. 多重降级解析
                    const json = JSON.parse(content);
                    
                    /**
                     * 这里的链式逻辑是为了兼容不同的 API 格式：
                     * - json.choices?.[0]?.delta?.content (OpenAI 官方标准)
                     * - json.content (常见自定义后端)
                     * - json (后端直接传个对象)
                     */
                    const delta = json.choices?.[0]?.delta?.content || json.content || json;
                    
                    // 如果解析出有效内容，通过回调传给前端渲染
                    if (delta) onMessage(delta);
                } catch (e) {
                    /**
                     * 5. 容错逻辑
                     * 如果后端没有传 JSON 而是传了纯文本，直接透传。
                     * 这样你的 Parser 就能同时兼容“流式 JSON”和“普通流”。
                     */
                    onMessage(content);
                }
            }
        }
    }

    /**
     * 强行刷新缓冲区
     * 场景：如果流结束了，但最后一行没有换行符，
     * 那么 while 循环会漏掉最后一点点数据，调用此方法可以确保“颗粒归仓”。
     */
    flush(onMessage) {
        if (this.buffer.trim()) {
            // 将剩余部分视为完整一行处理
            this.parse(new Uint8Array(), onMessage);
            this.buffer = ''; // 清空
        }
    }
}

export { MarkdownStreamParser };