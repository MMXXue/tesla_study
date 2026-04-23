
"use client";

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState } from 'react';
// 导入类型定义
import React from 'react';

// 第一步：定义零件规格
interface ProvidersProps {
    children: React.ReactNode;
}

// 第二步：使用规格
export default function Providers({ children }: ProvidersProps) {
    const [queryClient] = useState(() => new QueryClient());

    return (
        <QueryClientProvider client={queryClient}>
        {children}
        </QueryClientProvider>
    );
}
