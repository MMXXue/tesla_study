
// (写 use client): 只把那个需要点击弹窗的按钮，拆成一个小组件。

"use client"; // 只有这个小零件是客户端的

export function MyButton({ message }: { message: string }) {
  return (
    <button 
      onClick={() => alert(message)}
      className="
        relative px-8 py-3 font-medium text-white transition-all duration-300 
        bg-neutral-900 rounded-md overflow-hidden group
        hover:bg-neutral-800 active:scale-95 shadow-lg
      "
    >
      {/* 这是一个发光特效的背景 */}
      <span className="absolute inset-0 w-full h-full bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></span>
      
      <span className="relative">
        点击测试交互
      </span>
    </button>
  );
}