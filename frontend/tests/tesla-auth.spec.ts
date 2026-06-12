
// playwright的测试脚本

import { test, expect } from "@playwright/test";

// 让 Playwright 忽略本地自签名证书的 HTTPS 警告
test.use({ ignoreHTTPSErrors: true });

test("Tesla Edge Guard - 验证没有 Token 时是否会被无情驱逐", async ({ page }) => {
  // 1. 让虚拟用户直接强闯高密重地 /errorboundary
  await page.goto("https://localhost:3000/errorboundary");

  // 2. 核心断言 (Assert)：因为我们没带 Cookie，中间件保安应该在一瞬间把我们一脚踢回主页 "/"
  // Playwright 会盯着网址，看它最终是不是变成了首页的 URL
  await expect(page).toHaveURL("https://localhost:3000/");
});

test("Tesla Edge Guard - 验证注入正确 Token 后是否能丝滑通关", async ({ page, context }) => {
  // 1. 自动化神技：在发起请求前，全自动往浏览器的抽屉里塞入高密 Cookie
  // 这就是我们昨天手动在 F12 填表的自动化平替！
  await context.addCookies([
    {
      name: "tesla_auth_token",
      value: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoibWF4dWV5dWFuIiwicm9sZSI6IlNlbmlvciBBSSBFbmdpbmVlciIsImV4cCI6NDExMDIwMTYwMH0.fake_signature", // 塞入你手搓的防伪工牌
      domain: "localhost",
      path: "/",
    },
  ]);

  // 2. 此时再次命令虚拟用户驶向 /errorboundary
  await page.goto("https://localhost:3000/errorboundary");

  // 3. 核心断言：由于带着防伪工牌，网址应该稳稳停留在 /errorboundary，而不会被踢走！
  await expect(page).toHaveURL("https://localhost:3000/errorboundary");
});