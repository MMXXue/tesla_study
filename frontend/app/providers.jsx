"use client"; // 只有这个小盒子是客户端模式

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState } from 'react';

export default function Providers({ children }) {
    // 确保 QueryClient 只被创建一次
    const [queryClient] = useState(() => new QueryClient());

    return (
        // QueryClientProvider 提供“联网和缓存”的能力。
        <QueryClientProvider client={queryClient}> 
        {children}
        </QueryClientProvider>
    );
}