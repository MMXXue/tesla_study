import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// 1. 保安的拦截名单
export const config = {
  matcher: [
    "/seo-test/:path*", 
    "/telemetry/:path*", 
    "/errorboundary/:path*"
  ],
};

export function middleware(request: NextRequest) {
  // 2. 抓取口袋里的 Tesla 工牌
  const token = request.cookies.get("tesla_auth_token")?.value;

  // 3. 无证直接驱逐
  if (!token) {
    const loginUrl = new URL("/", request.url);
    return NextResponse.redirect(loginUrl);
  }

  try {
    // 4. 拆解 JWT 结构
    const parts = token.split(".");
    if (parts.length !== 3) {
      throw new Error("Invalid Token");
    }

    const payload = JSON.parse(atob(parts[1]));
    if (payload.exp && Date.now() >= payload.exp * 1000) {
      throw new Error("Expired");
    }

    // 5. 放行
    return NextResponse.next();
  } catch (error) {
    // 假证清理驱逐
    const response = NextResponse.redirect(new URL("/", request.url));
    response.cookies.delete("tesla_auth_token");
    return response;
  }
}