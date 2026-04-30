function Bomb() {
    // 1. 定义一个“陷阱”变量
    const data = null;

    // 2. 故意触发错误
    // 使用 (data as any) 骗过 TypeScript，让它以为 data 有 value 属性
    return (
        <div className="p-4 border border-gray-200 rounded-lg shadow-sm bg-white">
            <h4 className="font-bold text-gray-800">实时监控模块</h4>
            <p className="text-sm text-gray-600">
                数值: {(data as any).value} 
            </p> 
        </div>
    );
}

export default Bomb;