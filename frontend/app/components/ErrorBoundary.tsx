'use client';

import React, { ReactNode, ErrorInfo } from 'react';

// 1. 定义组件接收的参数类型 (Props)
interface Props {
  // children 代表被包裹的子组件
  children: ReactNode; 
  // fallback 是可选的，允许你从外部传入一个自定义的报错界面
  fallback?: ReactNode; 
}

// 2. 定义组件内部存储的状态类型 (State)
interface State {
  hasError: boolean;
  error: Error | null;
}

// 3. 将类型传给 React.Component<Props, State>
class ErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    // 初始化状态，默认没有错误
    this.state = { hasError: false, error: null };
  }

  // 当子组件报错时，TS 会自动调用这个方法并传入错误对象
  static getDerivedStateFromError(error: Error): State {
    // 更新状态，这将触发渲染降级 UI
    return { hasError: true, error };
  }

  // 记录错误堆栈，用于生产环境调试
  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.group("🚀 工业级错误隔离报告");
    console.error("错误详情:", error);
    console.error("组件堆栈:", errorInfo.componentStack);
    console.groupEnd();
  }

  // 重置方法：点击按钮尝试恢复正常
  handleReset = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError) {
      // 使用 Tailwind CSS 渲染精美的降级 UI
      return (
        <div className="flex flex-col items-center justify-center p-8 m-4 border-2 border-dashed border-red-200 rounded-2xl bg-red-50/50 backdrop-blur-sm transition-all">
          <div className="flex items-center justify-center w-14 h-14 mb-4 bg-red-100 rounded-full shadow-inner">
            <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          
          <h3 className="mb-2 text-xl font-bold text-red-900 tracking-tight">模块诊断异常</h3>
          
          <p className="mb-6 text-sm text-red-700 text-center max-w-sm leading-relaxed">
            系统已自动隔离该故障模块以保护全局面板。您可以尝试重置该组件。
            <span className="block mt-3 p-3 bg-red-100/50 rounded-lg font-mono text-xs text-red-800 border border-red-200 italic break-all">
              {this.state.error?.name}: {this.state.error?.message}
            </span>
          </p>

          <button
            onClick={this.handleReset}
            className="px-6 py-2.5 text-sm font-semibold text-white bg-red-600 rounded-xl shadow-lg shadow-red-200 hover:bg-red-700 active:scale-95 transition-all duration-200"
          >
            重置并重新加载
          </button>
        </div>
      );
    }

    // 没报错时，直接原样渲染里面的子组件
    return this.props.children;
  }
}

export default ErrorBoundary;