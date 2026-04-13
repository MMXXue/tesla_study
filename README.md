# ⚡ Fullstack AI Engineer 365 Days Challenge

## 📅 当前进度 (Current Progress)

- [x] **Day 1**: FastAPI 环境搭建与工程化配置
- [x] **Day 2**: 异步编程初探与并发控制机制
- [x] **Day 3**: 流式响应 (Streaming) 与特权调度逻辑 (超车实验 🚀)
- [x] **Day 4**: 对话记忆与 Session 状态管理 (Memory Chip 🧠)
- [x] **Day 5**: 数据库持久化层与多角色管理系统 (Persistence Layer 🗄️)
- [x] **Day 6**: 全栈链路闭环与赛博 UI 交互系统 (Cyber Interface ⚡)
     - **环境排障**: 攻克 Live Server 监听 DB 导致的循环刷新“幽灵 Bug”。
- [x] **Day 7**: UI 深度进化与 Agent 角色注入 (State & Soul 🧠)
    - **技术突破**: 实现流式 Markdown 实时解析与历史记忆自动回显。
    - **Agent 化**: 后端注入 System Prompt，完成从“聊天框”到“诊断助手 TS-79”的角色转变。
- [x] **Day 8**: 神经元觉醒 - 接入 DeepSeek 大脑 (Intelligence Activation 🧠)
    - **大脑接入**: 彻底舍弃 Mock 模拟数据，通过 httpx 实现异步流式调用 DeepSeek API。
    - **全栈合体**: 打通“前端 -> 后端 -> 数据库 -> 大模型”的完整 AI 应用闭环。
- [x] **Day 9**: PostgreSQL 百万级数据查询优化 (Database Optimization)
    - **GIN索引**: 将关键字检索响应时间从 200ms+ 压缩至毫秒级。
    - **大规模数据生成**: 使用 generate_series 与随机函数灌录 1,000,000 条 模拟 Tesla 运行日志。
- [x] **Day 10**: 分布式架构下的任务自愈系统 (System Resilience 🛡️)
    - **并发锁机制**: 采用 `FOR UPDATE SKIP LOCKED` 行级锁，攻克多 Worker 抢单冲突，确保任务处理的原子性。
    - **分布式状态机**: 利用 Redis 实现“心跳续期 (Heartbeat)”机制，实时监测 Agent 运行状态。
    - **超时补偿逻辑**: 编写 Monitor 巡检脚本，实现僵尸任务自动发现与 PENDING 状态回滚，构建“杀不死”的分布式任务调度闭环。
- [x] **Day 11**: 高并发 I/O 调优与数据库连接池极限压测 (I/O Tuning & Stress Test 🚀)
    - **连接池架构**: 深入调优 SQLAlchemy 异步连接池，通过 `pool_size` 与 `max_overflow` 参数构建高吞吐后端。
    - **性能调优闭环**: 手写并发压测脚本，复现高并发下的“连接饥饿”与 `TimeoutError`，并将系统响应从 5s 优化至 1s。
- [x] **Day 12**: 数据库迁移与版本控制 (Schema Migrations), revision --autogenerate 机制, upgrade（进化）与 downgrade（回退）函数
    - **Alembic 落地**: 成功搭建 Alembic 迁移工作流，实现从 SQLAlchemy 模型到 PostgreSQL 物理表的自动化映射。
    - **生产安全审计**: 意识到自动化脚本的风险，建立起“生成脚本 -> 人工 Review -> 执行升级”的工业级数据库变更标准。
- [x] **Day 13**: 高性能热点缓存策略与对话上下文控制 (Caching & Memory Management 🧠)
    - **旁路缓存 (Cache Aside Pattern)**：
        - **多级存储调度**：构建 `PromptService` 实现“Redis 优先，DB 兜底”逻辑，通过**回填机制 (Backfill)** 将 System Prompt 查询从磁盘 I/O 提升至内存级响应，性能优化达 **50倍+**。
        - **缓存穿透防护**：针对非预设 Role 实现“空值/默认值”缓存，成功拦截无效请求直接穿透至 PostgreSQL，保障存储层在高频访问下的稳定性。
    - **状态管理与滑动窗口 (State Management)**：
        - **Session 隔离机制**：设计 `session:{user_id}:{role}` 命名空间，实现分布式环境下的多租户对话隔离，确保 AI 上下文在并发场景下的绝对准确。
        - **内存容量约束**：利用 Redis 的 `RPUSH` 与 `LTRIM` 原子操作，构建**固定长度 (Fixed-size) 的滑动窗口记忆**，从架构层面根治长对话导致的 Token 费用爆炸及模型窗口溢出。
    - **分布式调试与数据选型**：
        - **全链路追踪**：通过 `redis-cli` 深度调试，攻克从“缓存未命中 (nil)”到“热点命中 (Cache Hit)”的逻辑断层。
        - **多数据结构应用**：深刻理解 **String** (用于静态 Prompt) 与 **List** (用于动态 Session) 的选型边界，确保 Redis 内存利用率的最优化。
- [x] **Day 14**: 分布式锁实战 (Distributed Lock 🔒)
    - **Redis锁**: 实现简单的redis锁
    - **Redlock 算法**：实现多实例环境下的 AI 任务分配唯一性，防止重复消费。
- [x] **Day 15**: Week 2 Project — 高并发诊断日志引擎 (System Design 🚀)
    - **压测根因定位**：复现 `0/1000` 失败，定位核心问题为压测侧连接池等待超时 (`PoolTimeout`)，而非服务逻辑崩溃。
    - **外部并发治理**：通过并发扫频找到系统甜点区间（本机约 `10~20`），避免并发过高进入拥塞区导致 TPS 下降、延迟飙升。
    - **内部热路径优化**：API 保持“只入队不重处理”，采用原始请求体直入 Redis，减少 JSON 解析与请求路径开销。
    - **消费链路优化**：Worker 使用批量 `LPOP` + 批量落库，降低 Redis 往返次数与数据库写入开销。
    - **指标化方法论**：建立 `perf_benchmark.py` 与 `PERF_CHECKLIST.md`，以成功率、TPS、avg、p95、p99 作为统一评估标准。
- [x] **Day 16**: gRPC 定义与工业协议实战 (Protocol Design 📡)
    - **Proto 定义**：编写 `.proto` 文件定义工厂传感器状态上报接口，理解 `message`、`service`、`rpc` 三层结构。
    - **代码生成**：使用 `grpc_tools.protoc` 自动生成 Python stub，掌握 `--python_out` 与 `--grpc_python_out` 的区别与用途。
- [x] **Day 17**: 协议性能测试 (Benchmark 对比 gRPC (Protobuf) 与 REST (JSON) 吞吐量)
    - **性能基准测试**：实现 gRPC 与 REST API 的并发吞吐量对比，量化二进制协议在高负载下的优势。
    - **延迟测量**：通过异步压测脚本，测量端到端响应时间，验证 gRPC 在工业场景下的低延迟特性。
    - **资源消耗分析**：对比 CPU、内存占用，评估协议选择对系统资源的影响。
- [x] **Day 18**: MQTT (既可以发送也可以接收数据,且长连接)
    - **部署补全**：工业级 Mosquitto 一键部署，解决权限与配置文件的“根因故障”。
    - **协议实战**：理解 MQTT 在海量连接下对比 gRPC 的解耦与负载优势。
    - **性能直觉**：通过“刷屏”速率测试系统压力，验证高并发时的可用性与稳定性。
- [x] **Day 19**: WebSocket 状态机 (WS State Machine) (长连接)
    - **连接管理**：实现 `ConnectionManager` 对在线连接进行连接/断开/广播管理。
    - **心跳机制**：客户端定时发送 `ping`，服务端 `pong` 应答，检测断线重连状态。
    - **重连策略**：客户端实现指数退避重连逻辑，`onclose` 后递归重连，10s 限制最高等待。
- [x] **Day 20**: 弹性架构设计 (Resilient Architecture 🛡️)
    - **指数退避重试 (Exponential Backoff)**：利用 Tenacity 实现 `wait_exponential`，通过增加重试间隔解决网络抖动，防止“重试风暴”压垮服务器。
    - **熔断机制 (Circuit Breaker)**：集成 `pybreaker` 实现三色状态机管理（Closed/Open/Half-Open）。在下游服务持续故障时自动“跳闸”拦截请求，保护本地 CPU 与内存资源。
    - **故障可观测性**：建立重试次数与熔断触发的详细 logging 审计，实现对系统“弹性过程”的黑匣子追踪。
- [x] **Day 21**: 分布式流量治理 (Traffic Management 🚦)
    - **令牌桶算法 (Token Bucket)**：深入理解其允许“突发流量”的特性，并对比分析其与“漏桶算法”及“连接池”在资源分配上的本质区别。
    - **Redis + Lua 原子限流**：编写并部署 Lua 脚本至 Redis 内部，实现“读取-计算-写入”的原子化操作，彻底解决分布式环境下的竞态条件 (Race Condition)。
    - **高并发压力验证**：使用 `threading.Thread` 模拟多线程冲击，验证限流器在微秒级竞争下对流量拦截的精确度（如 10/20 成功率）。
- [x] **Day 22**: Week 3 Project — 异构协议网关 (Protocol Gateway 🚦) - MQTT/FastAPI/WebSocket
    - **MQTT 订阅与消息处理**：连接公共 MQTT Broker (broker.emqx.io)，订阅 "tesla/sensors" 主题，实时接收传感器数据。
    - **WebSocket 广播机制**：集成 ConnectionManager，实现 MQTT 消息到 WebSocket 客户端的实时广播。
    - **协议转换逻辑**：将 MQTT 二进制消息解析为 JSON，通过 FastAPI 中间层转发至 WebSocket。
    - **CORS 配置**：修复前端连接时的 403 Forbidden 错误，确保跨域访问。
    - **异步架构**：利用 asyncio 实现高并发消息处理，支持多客户端同时监控。
- [x] **Day 23**: 结构化日志
    - **Trace ID 注入**：使用中间件为每个请求生成唯一 UUID，并绑定到协程上下文。
    - **结构化日志配置**：配置 structlog 处理器，包括日志级别、时间戳、上下文变量合并和 JSON/彩色输出。
    - **全链路追踪**：通过 bind_contextvars 实现日志中的 Trace ID 自动注入，确保请求链路可追踪。
    - **响应头返回**：在 HTTP 响应头中添加 X-Trace-ID，便于前端和外部系统调试。
- [x] **Day 24**: 性能 Profiling
    - **cProfile 集成**：使用 cProfile 对异步代码进行性能分析，识别 CPU 密集型任务的阻塞瓶颈。
    - **异步服务分析**：通过 FastAPI 端点模拟重负载场景，分析函数调用时间和资源消耗。
    - **性能优化洞察**：识别 slow_function 和 heavy_computation 等耗时操作，为后续优化提供数据支持。
- [x] **Day 25**: 异步单元测试
    - **Pytest-asyncio 实践**：编写异步测试脚本，使用 @pytest.mark.asyncio 装饰器处理协程测试。
    - **Mocking 技术**：利用 AsyncMock 模拟数据库操作，避免测试时的外部依赖。
    - **测试覆盖**：实现对 welcome_user 函数的逻辑验证，确保异步代码的正确性和可靠性。
- [x] **Day 26**: 数据清洗方案
    - **Pydantic v2 校验**：使用 BaseModel 和 Field 实现工业传感数据的严苛校验，包括类型和范围验证。
    - **错误捕获与分析**：通过 ValidationError 捕获并分析数据错误，提供详细的错误信息。
    - **数据质量保障**：确保传感器数据（如 id 和 val）的有效性，防止无效数据进入系统。
- [x] **Day 27**: 实现了基于多阶段构建的 Docker 环境优化，将镜像体积从约 800MB 缩减至 85MB，初步掌握工业级部署规范。
- [x] **Day 28**: 环境隔离与多环境配置体系
    - **Pydantic Settings 架构**：构建了基于 pydantic-settings 的中央配置大脑，实现了配置与逻辑的完全解耦，符合 12-Factor App 工业标准。
     - **动态注入与优先级管理**：实现了从 .env 文件到系统环境变量的动态注入，并掌握了“系统变量 > .env 文件 > 默认值”的优先级控制逻辑，确保系统在不同环境下的灵活性。
    - **工程标准化实践**：建立了 .env.example 模板机制，规范了敏感数据（Postgres, Redis, DeepSeek API）的管理流，并结合 .gitignore 强化了工程安全性，杜绝密钥泄露风险。
- [x] **Day 29**: 车辆健康诊断 API 核心架构实现
     - **智能诊断引擎设计**：基于 FastAPI 构建了车辆状态监控核心接口，实现了针对 VehicleStatus 传感器数据的实时校验逻辑，确保诊断流水线的输入质量。
     - **工程化日志链路（初步）**：引入了 structlog 异步日志框架，初步设计了 JSON 格式的结构化日志输出，为 AI 模型的后续训练提供了标准化的数据"黑匣子"。
     - **数据模型保障**：利用 Pydantic 的类型约束机制，建立了严格的传感器数据过滤层，通过代码层面的"物理隔离"防止了脏数据对诊断逻辑的干扰。
- [x] **Day 30**: 工业级容器化部署与日志链路闭环
     - **日志系统深度调优**：攻克了 structlog 与 pytest 运行环境下的日志冲突，通过底层 root_logger 的重构与"手动接线"，确保了诊断轨迹在复杂测试环境下的 100% 可追踪性。
     - **极简依赖管理实践**：弃用传统的 pip freeze 方案，采用 pipreqs 实现基于代码扫描的按需依赖注入。这一举措不仅剔除了历史残留的冗余库，更显著降低了 Docker 镜像的潜在攻击面和启动时延。
     - **权限与持久化方案**：利用 chmod 666 解决了容器内外文件系统的权限壁垒，结合 RUN touch 指令确保了系统在无状态容器环境下的文件写入稳定性。
     - **卷挂载（Volume）实时监控**：通过 docker run -v 技术实现了宿主机与容器内部日志文件的实时同步挂载，构建了"生产环境运行、开发环境监控"的工程闭环。
- [x] Day 31: 全栈 AI 架构转型与 Next.js 15 混合渲染实战
    - **双轴并行开发环境构建**：在保持原有 Python 后端生态的同时，基于 Conda 构建了独立的 Node.js 20 运行环境，实现了 AI 模型逻辑与前端展现层的“物理隔离与逻辑共生”。
    - **前端工程化目录规范**：建立了 frontend/backend 的分层目录体系。通过基于文件夹的路由协议（File-based Routing）构建了多页面应用骨架，并利用 <Link> 组件实现了无刷新的单页应用（SPA）交互体验。



    
---

# 🚀 Tesla AI Engineer 365-Day Challenge: Phase 1

### 🟢 Month 1: 后端核心与高性能架构 (Deep Dive)

#### Week 2: 数据库深度优化与数据一致性
| 天数 | 主题 | 核心任务 (Tesla Standard) | 技术关键词 |
| :--- | :--- | :--- | :--- |
| ~~**Day 09**~~ | ~~索引深度优化~~ | ~~实现百万级对话记录的 EXPLAIN ANALYZE 性能瓶颈分析~~ | ~~PostgreSQL, GIN Index~~ |
| ~~**Day 10**~~ | ~~并发锁机制~~ | ~~使用 `SELECT FOR UPDATE` 实现 Agent 状态更新的原子性~~ | ~~Row-level Locking~~ |
| ~~**Day 11**~~ | ~~连接池调优~~ | ~~针对高并发 I/O 调优 SQLAlchemy 的异步连接池配置~~ | ~~Connection Pooling~~ |
| ~~**Day 12**~~ | ~~数据库迁移~~ | ~~使用 Alembic 模拟生产环境的 Schema 不停机变更~~ | ~~Alembic, Migrations~~ |
| ~~**Day 13**~~ | ~~热点缓存策略~~ | ~~接入 Redis 缓存 System Prompt 与 Session~~ | ~~Redis (Cache Aside)~~ |
| ~~**Day 14**~~ | ~~分布式锁实战~~ | ~~实现 Redlock 算法，确保多实例环境下 AI 任务分配唯一性~~ | ~~Distributed Lock~~ |
| ~~**Day 15**~~ | ~~**Week 2 Project**~~ | ~~**构建“高并发诊断日志引擎”**：TPS > 500，查询延迟 < 50ms~~ | ~~System Design~~ |

#### Week 3: 工业协议转换与系统韧性
| 天数 | 主题 | 核心任务 (Tesla Standard) | 技术关键词 |
| :--- | :--- | :--- | :--- |
| ~~**Day 16**~~ | ~~gRPC 定义~~ | ~~编写 `.proto` 文件定义工厂设备状态上报接口~~ | ~~Protobuf 3~~ |
| ~~**Day 17**~~ | ~~协议性能测试~~ | ~~Benchmark 对比 gRPC (Protobuf) 与 REST (JSON) 吞吐量~~ | ~~gRPC-python~~ |
| ~~**Day 18**~~ | ~~MQTT 边缘采集~~ | ~~模拟 1000 个设备通过 MQTT 异步推送传感器数据~~ | ~~Mosquitto, Paho~~ |
| ~~**Day 19**~~ | ~~WS 状态机~~ | ~~完善 WebSocket 重连机制、心跳检测与前端同步逻辑~~ | ~~WebSockets~~ |
| ~~**Day 20**~~ | ~~弹性架构设计~~ | ~~为 API 调用实现指数退避 (Exponential Backoff) 重试机制~~ | ~~Tenacity, Resilience~~ |
| ~~**Day 21**~~ | ~~流量治理~~ | ~~基于 Redis 令牌桶算法实现设备级/用户级的分布式限流~~ | ~~Rate Limiting~~ |
| ~~**Day 22**~~ | ~~**Week 3 Project**~~ | ~~**构建“异构协议网关”**：实现 MQTT -> FastAPI -> WS 全链路~~ | ~~Protocol Gateway~~ |

#### Week 4: 工程标准化与可观测性
| 天数 | 主题 | 核心任务 (Tesla Standard) | 技术关键词 |
| :--- | :--- | :--- | :--- |
| ~~**Day 23**~~ | ~~结构化日志~~ | ~~接入 `structlog`，实现包含 Trace ID 的全链路日志追踪~~ | ~~Structured Logging~~ |
| ~~**Day 24**~~ | ~~性能 Profiling~~ | ~~使用 `cProfile` 识别异步代码中的阻塞瓶颈~~ | ~~Profiling~~ |
| ~~**Day 25**~~ | ~~异步单元测试~~ | ~~编写 Pytest-asyncio 脚本，使用 Mocking 进行异步单元测试~~ | ~~TDD, Mocking~~ |
| ~~**Day 26**~~ | ~~数据清洗方案~~ | ~~利用 Pydantic v2 实现工业传感数据的严苛校验~~ | ~~Data Validation~~ |
| ~~**Day 27**~~ | ~~镜像体积优化~~ | ~~采用 Multi-stage Build 将 Docker 镜像体积缩减 80%~~ | ~~Dockerfile Opt~~ |
| ~~**Day 28**~~ | ~~环境隔离体系~~ | ~~构建基于 `pydantic-settings` 的多环境配置动态注入~~ | ~~Config Management~~ |
| ~~**Day 29**~~ | ~~API 标准化~~ | ~~生成完全符合 OpenAPI 标准的文档，自动生成前端 SDK~~ | ~~Swagger/OpenAPI~~ |
| ~~**Day 30**~~ | ~~**Month 1 Milestone**~~ | ~~**发布 TS-79 诊断专家 v1.0 生产级镜像**~~ | ~~Release Engineering~~ |

---

## 🛠️ 技术栈 (Tech Stack)
* **Backend:** FastAPI (Async), SQLAlchemy 2.0, Pydantic v2
* **Database:** PostgreSQL (Partitioning), Redis (Redlock)
* **Protocols:** gRPC, MQTT, WebSocket, SSE
* **DevOps:** Docker (Multi-stage), CI/CD (GitHub Actions)
* **AI:** DeepSeek-V3 API, RAG (Upcoming)

---

### 🟡 Month 2: 前端交互与 AI 视觉化 (Responsive & Streaming)
**目标：** 构建高性能实时监控面板，攻克大模型流式渲染与工业级状态管理。

#### Week 5: 现代前端基石与响应式系统 (The Shell)
| 天数 | 主题 | 核心任务 (Tesla Standard) | 技术关键词 |
| :--- | :--- | :--- | :--- |
| ~~**Day 31**~~ | ~~Next.js 核心架构~~ | ~~掌握 App Router, Server Components 与 Client Components 混合使用~~ | ~~Next.js 15+~~ |
| **Day 32** | Tailwind CSS 布局 | 构建“赛博朋克”风格 Grid 布局，支持工厂多节点监控卡片流 | Flexbox/Grid |
| **Day 33** | 响应式深度适配 | 适配移动端与超宽屏（Ultrawide），确保监控数据不溢出、不重叠 | Breakpoints |
| **Day 34** | 组件化开发 | 抽象出可复用的 AI Chat Bubble 和 Device Status Card 基础组件 | Atomic Design |
| **Day 35** | 动态交互进阶 | 引入 Framer Motion 实现极致流畅的组件进入与状态切换动画 | Framer Motion |
| **Day 36** | 图标与视觉语义 | 针对设备运行、故障、待机状态设计视觉反馈系统 | Lucide React |
| **Day 37** | **Week 5 Project** | **构建“工厂资产管理面板”**：实现全响应式的静态设备可视化看板 | UI Prototype |

#### Week 6: 状态管理与复杂数据流 (The Nervous System)
| 天数 | 主题 | 核心任务 (Tesla Standard) | 技术关键词 |
| :--- | :--- | :--- | :--- |
| **Day 38** | Zustand 状态管理 | 使用轻量级 Zustand 管理全局用户偏好与设备实时状态 | Store Design |
| **Day 39** | TanStack Query | 实现异步数据获取、自动缓存回补（SWR）与预取逻辑 | Server State |
| **Day 40** | 高级表单处理 | 构建 AI Agent 配置表单，集成 Zod 进行严苛的前端 Schema 校验 | React Hook Form |
| **Day 41** | Context API 妙用 | 在局部组件树中管理特定的 AI 诊断会话上下文（Session Context） | React Context |
| **Day 42** | 前端持久化 | 实现页面刷新后，当前会话 ID 和 UI 布局偏好自动恢复 | LocalStorage/Persist |
| **Day 43** | 错误边界处理 | 实现 Error Boundary，确保单个组件崩溃不影响全局面板运行 | Fault Tolerance |
| **Day 44** | **Week 6 Project** | **构建“多角色切换系统”**：实现 Agent、Admin、Maintainer 视图平滑切换 | State Sync |

#### Week 7: 打字机流与实时视觉化 (The Pulse)
| 天数 | 主题 | 核心任务 (Tesla Standard) | 技术关键词 |
| :--- | :--- | :--- | :--- |
| **Day 45** | SSE 流式解析 | 手写前端 Parser，处理后端传来的 Chunked Markdown 片段流 | SSE / Streams |
| **Day 46** | 打字机效果优化 | 解决流式输出时的页面抖动（Jank）与自动触底滚动逻辑 | UX Optimization |
| **Day 47** | Markdown 实时渲染 | 集成代码高亮、数学公式（LaTeX）与工业表格渲染 | React Markdown |
| **Day 48** | ECharts 实时图表 | 接入动态折线图，展示传感器上报的实时频率（60FPS 渲染） | Canvas / SVG | 研究 Canvas 渲染优化 |
| **Day 49** | WebSocket 联调 | 实现前端与后端的全双工心跳检测，确保连接断开自动重连 | WS Protocol |
| **Day 50** | 多模态资源加载 | 处理 AI 返回的图片/视频流，实现渐进式加载（Progressive Load） | Media Assets |
| **Day 51** | **Week 7 Project** | **构建“实时 AI 诊断终端”**：支持流式对话与实时动态传感器图谱 | Full-duplex UI |

#### Week 8: 前端工程化与性能极致优化 (The Precision)
| 天数 | 主题 | 核心任务 (Tesla Standard) | 技术关键词 |
| :--- | :--- | :--- | :--- |
| **Day 52** | Virtual List 虚拟列表 | 处理上万条历史日志时，通过虚拟滚动技术保持页面不卡顿 | react-window |
| **Day 53** | 图像/资源优化 | 深度使用 Next.js Image 处理设备快照的极致压缩与懒加载 | WebP / Avif |
| **Day 54** | Bundle Analysis | 使用分析工具剔除冗余依赖，极致缩减首屏加载时间 (FCP) | Turbopack |
| **Day 55** | SEO 与 Metadata | 针对管理平台进行 Meta 信息优化，提升内网搜索索引效率 | Metadata API |
| **Day 56** | Middleware 鉴权 | 在 Edge Runtime 实现路由拦截与基于 JWT 的身份校验 | Edge Functions |
| **Day 57** | E2E 自动化测试 | 使用 Playwright 模拟用户操作 AI 聊天框的完整交互路径 | Playwright |
| **Day 58** | 前端压力测试 | 模拟 50+ 实时数据流同时刷新，排查浏览器内存泄漏 (Leak) | Chrome DevTools |
| **Day 59** | CI/CD 部署自动化 | 配置 GitHub Actions 实现前端项目的自动构建与多环境发布 | Deployment |
| **Day 60** | **Month 2 Milestone** | **发布“赛博工厂 AI 交互系统 v2.0”**：全链路流式响应、毫秒级渲染 | Final Release |

---

### 💡 核心原则 (UI/UX Principles)
* **实时性高于一切**：监控数据延迟超过 500ms 即视为失效。
* **信息密度平衡**：通过分层设计展示核心 AI 预警，避免“数据坟墓”。
* **防御性渲染**：前端必须对后端可能返回的任何脏数据进行优雅降级处理。

---
### 🟠 Month 3: 综合实战 —— 工业级 AI 监控系统 (Industrial Integration)
**目标：** 打通“传感器 -> 协议网关 -> AI 诊断 -> 实时看板”全链路，交付具备 Tesla 特色的工厂大脑原型。

#### Week 9: 工业协议接入与网关转换 (The Bridge)
| 天数 | 主题 | 核心任务 (Tesla Standard) | 技术关键词 |
| :--- | :--- | :--- | :--- |
| **Day 61** | MQTT Broker 部署 | 部署 Mosquitto 并配置基于 JWT 的安全认证与 Topic 隔离 | Mosquitto, Security |
| **Day 62** | 异步设备模拟器 | 编写 Python 脚本模拟 500+ 工业机器人并发产生状态数据流 | asyncio, Pytest |
| **Day 63** | MQTT-to-FastAPI | 实现异步消费者，将传感器二进制数据转化为结构化 JSON | Paho-MQTT |
| **Day 64** | gRPC 控制指令集 | 定义 gRPC 服务，模拟向机器人下发“紧急制动”等高优先级指令 | gRPC, Protobuf |
| **Day 65** | 协议网关性能调优 | 测试并优化网关在每秒 10k 消息下的 CPU 与内存占用 | Performance Tuning |
| **Day 66** | 消息持久化策略 | 采用 TimescaleDB 处理海量时序数据，优化写入吞吐量 | Time-series Data | 明确数据生命周期管理 (TTL) |
| **Day 67** | **Week 9 Project** | **构建“工业协议转换器”**：实现不同协议间的亚毫秒级转发 | Protocol Bridge |

#### Week 10: AI 实时诊断与逻辑注入 (The Intelligence)
| 天数 | 主题 | 核心任务 (Tesla Standard) | 技术关键词 |
| :--- | :--- | :--- | :--- |
| **Day 68** | 异常检测逻辑设计 | 编写基础算法，根据传感器阈值触发 AI 诊断请求 | Rule Engine |
| **Day 69** | AI Agent 自动触发 | 实现任务队列，当设备异常时自动唤醒 DeepSeek 进行原因分析 | Task Queue |
| **Day 70** | 实时上下文组装 | 动态拉取故障发生前 1 分钟的所有传感器快照作为 AI 输入 | Data Context |
| **Day 71** | 流式预警推送 | AI 诊断结果通过 WebSocket 分频道流式推送到前端指定监控位 | Pub/Sub |
| **Day 72** | 闭环指令确认 | 实现“AI 建议 -> 人工确认 -> gRPC 指令执行”的闭环流程 | Human-in-the-loop |
| **Day 73** | 推理成本监控 | 记录每次 AI 诊断的 Token 消耗，并在管理后台实时看板展示 | Token Metrics |
| **Day 74** | **Week 10 Project** | **构建“自动诊断中枢”**：异常发生到 AI 介入延迟控制在 2s 内 | AI Logic |

#### Week 11: 高性能全栈联调与压测 (The Stress Test)
| 天数 | 主题 | 核心任务 (Tesla Standard) | 技术关键词 |
| :--- | :--- | :--- | :--- |
| **Day 75** | 全链路数据追踪 | 接入 OpenTelemetry 实现从传感器到前端展示的全链路 Trace | Distributed Tracing |
| **Day 76** | 前端压力测试 | 模拟 100 个监控卡片同时接收高频数据流，解决渲染卡顿 | Profiling |
| **Day 77** | 后端并发极限测试 | 使用 Locust 模拟 5000+ 并发设备上报，找出系统崩溃点 | Load Testing |
| **Day 78** | 缓存穿透与雪崩 | 模拟 Redis 宕机，测试系统的降级逻辑与数据保护机制 | Chaos Engineering |
| **Day 79** | 数据库查询优化 | 对历史告警记录进行分区查询优化，确保百万级数据秒开 | Partitioning |
| **Day 80** | 网络异常容错 | 测试 3G/4G 弱网环境下 WebSocket 的断线重连与数据补发 | Resilience |
| **Day 81** | **Week 11 Project** | **系统压力白皮书**：输出系统承载极限与 QPS 报告 | QA Analysis |

#### Week 12: 工业级部署与项目结项 (The Giga-Release)
| 天数 | 主题 | 核心任务 (Tesla Standard, 增加 mTLS (双向 TLS) 的了解) | 技术关键词 |
| :--- | :--- | :--- | :--- |
| **Day 82** | Docker Compose 集成 | 编写一键启动脚本，包含 DB, Redis, MQTT, AI-API 及前端 | Containerization |
| **Day 83** | Prometheus 指标监控 | 暴露 `/metrics` 接口，监控 API 成功率与响应时间 | Prometheus |
| **Day 84** | Grafana 看板配置 | 搭建可视化运维大屏，实时监控系统健康度与算力消耗 | Grafana |
| **Day 85** | 安全性扫描 | 检查 API 越权漏洞、SQL 注入及环境变量泄露风险 | Security Audit |
| **Day 86** | 自动标注预研究 | 尝试将 AI 诊断结果保存为数据集，为第二阶段模型训练做准备 | Data Engine |
| **Day 87** | 项目文档与 API 文档 | 完善所有的架构图 (Mermaid) 与接口调用手册 | Documentation |
| **Day 88** | 部署至本地服务器 | 在独立硬件上完成部署，模拟真实的边缘侧运行环境 | On-premise |
| **Day 89** | 演示录屏与复盘 | 制作 3 分钟 Demo 视频，展示全栈全链路闭环能力 | Portfolio |
| **Day 90** | **Phase 1 Milestone** | **第一阶段结项考试**：从 0 到 1 快速恢复生产环境全栈系统 | Disaster Recovery |

---

### 💡 结项考核标准 (Definition of Done)
1. **延迟稳定性**：传感器数据从上报到前端显示的端到端延迟 < 200ms。
2. **并发能力**：单台服务器（8C16G）支持 2000 个设备长连接且 CPU 占用 < 60%。
3. **AI 集成度**：AI 不仅能聊天，更通过 RAG 接入了工厂手册，能准确识别设备型号。
4. **代码质量**：所有核心模块均有单元测试覆盖，且通过生产级 Dockerfile 交付。
---





> **“代码是手，逻辑是心，AI 是大脑。”**
> 本项目记录了我通往资深全栈 AI 工程师的 365 天进阶历程，涵盖从底层的工程筑基到顶层的系统架构设计。

---

## 🗺️ 365 天学习路线图 (Roadmap)

### 🟢 第一阶段：工程筑基 —— 打造工业级“手脚” (Day 1 - 90)
**目标：** 构建稳健的 AI 运行系统架构，打通全栈链路。

* **Day 1-30: 后端核心与高性能架构**
    * 精通 FastAPI 异步编程、PostgreSQL 数据库建模与持久化记忆。
* **Day 31-60: 前端交互与 AI 视觉化**
    * Tailwind CSS 响应式布局、React/Next.js 状态管理、打字机流式渲染 (Streaming)。
* **Day 61-90: 综合实战**
    * 构建“工厂设备实时监控系统”，完成前后端全链路联调。

**深度建议补充**: 增加“确定性”与“并发控制”
    * 缺失项：实时通信协议 (Protocols)。 特斯拉的工厂监控不是简单的 HTTP 请求。
    * 建议： 在 Day 61-90 加入 gRPC 和 MQTT。在工业场景下，低延迟的二进制协议比 JSON 更重要。
    * Senior 视角： 研究分布式锁和 Redis 缓存一致性。当 1000 个传感器同时上报数据时，你的“记忆持久化”会不会死锁？

**阶段项目：** 🏗️ **智能工厂监控助手 (AI-Driven Factory Monitor)**
*重点：练好“手脚”，掌握流式对话、数据库记忆和基础全栈联调。*

---

### 🟡 第二阶段：AI Infra 与云原生 —— 掌控算力 (Day 91 - 180)
**目标：** 对齐 Tesla 核心岗位需求，掌握 GPU 算力调度与生产级部署。

* **Day 91-120: 容器化基础设施**
    * Docker & Docker Compose 多容器协同，实现环境隔离与快速迁移。
* **Day 121-150: 云原生编排 (K8s 专项)**
    * Kubernetes 基础架构、GPU Operator 实战（容器内显卡资源调用）。
* **Day 151-180: 自动化与可观测性**
    * CI/CD 流水线 (GitHub Actions)、Prometheus & Grafana 监控体系。

**深度建议补充**: 从“会用 K8s”到“理解硬件”
    * 缺失项：CUDA 与显存管理。
    * 建议： 在 Day 121-150 深入一下 NVIDIA Triton Inference Server。特斯拉非常看重模型在生产环境中的 Throughput (吞吐量)。
    * Senior 视角： 搞清楚什么是 NVIDIA MPS (Multi-Process Service)。在 Tesla 的集群里，如何让多个小模型共享一块显卡而不互相干扰？这是省钱（算力成本）的关键。

**阶段项目：** 🚀 **高可用 AI 推理平台 (High-Availability AI Serving)**
*重点：练好“骨架”，攻克 K8s、Docker 和 GPU 监控，对齐 MLOps 岗位需求。*

---

### 🟠 第三阶段：感知与大脑 —— 理解物理世界 (Day 181 - 270)
**目标：** 实现从文字 AI 到多模态视觉 AI 的跨越。
    * 到了 Day 180 之后： 我会开始定期给你投喂“论文简报”，让你具备岗位 3 要求的科学家视野。

* **Day 181-210: 视觉与多模态感知**
    * 集成 YOLO/SAM 视觉模型，实现工业级摄像头实时识别。
* **Day 211-240: RAG 与向量数据库**
    * 使用 Milvus/Pinecone 构建企业级知识库，优化检索准确率。
* **Day 241-270: 推理加速与边缘部署**
    * 实战 vLLM / TensorRT-LLM，探索低延迟推理的极限优化。

**深度建议补充**: 从“模型集成”到“感知底层”
    * 缺失项：数据闭环 (Data Engine)。 这是马斯克反复强调的。
    * 建议： 在 Day 211-240 加入 “自动标注 (Auto-labeling)” 的逻辑研究。不要只学怎么用 YOLO，要学如何利用大模型来辅助标注小模型的数据。
    * Senior 视角： 关注 TensorRT 的量化 (INT8/FP8)。在边缘设备上，每一毫秒的延迟都关乎生产安全。

**阶段项目：** 👁️ **视觉质检 Agent (Visual QC Inspector)**
*重点：练好“眼睛”，实战 YOLO、SAM 视觉模型和 RAG，向岗位核心能力发起冲击。*

---

### 🔴 第四阶段：智能体与系统设计 —— AI Native 架构师 (Day 271 - 365)
**目标：** 提升复杂问题解决维度，冲刺 Tesla 级系统架构面试。

* **Day 271-300: AI Agent 深度设计**
    * 研究工具调用 (Tool Calling)、自我纠错、任务拆解等 Agentic Workflow。
* **Day 301-330: 大规模系统设计 (System Design)**
    * 针对高并发、高可用分布式架构进行设计，模拟 Tesla 级别数据量。
* **Day 331-365: 面试突击与终极项目**
    * 复盘 Tesla 面试真题，打通“超级工厂智能大脑原型”。

**深度建议补充**: 系统设计的“第一性原理”
    * 缺失项：分布式文件系统与数据湖。
    * 建议： 加入对 MinIO 或 Apache Iceberg 的了解。Tesla 每天产生海量的视频数据，如何高效存储和检索这些“非结构化数据”是面试大杀器。
    * Senior 视角： 模拟面试时，不仅要说“怎么做”，还要能计算“成本”和“带宽限制”。

**终极项目：** 🧠 **超级工厂智能大脑原型 (Tesla Gigafactory Brain)**
*重点：练好“大脑”，集成全栈 AI 技术，解决端到端的复杂工业场景问题。*

---

## 🛠 代码提交规范 (Commit Convention)

为了保持项目演进历史的专业性，本项目严格遵循以下 Git 提交规范：

| 标识 (Type) | 含义 | 典型应用场景 |
| :--- | :--- | :--- |
| **feat** | **新功能** | 完成了 Day 4 的记忆功能、增加新 API 接口 |
| **fix** | **修复** | 修复连接中断、解决逻辑 Bug |
| **docs** | **文档** | 修改 README、完善代码注释、补充设计文档 |
| **style** | **格式** | 清理缓存、代码缩进调整（不影响业务逻辑） |
| **refactor** | **重构** | 优化代码结构、解耦模块、移除冗余代码 |
| **chore** | **杂务** | 更新 .gitignore、修改依赖配置 |

**示例：**
`feat: 增加用户 Session 持久化存储逻辑`

---

## 项目结构变更说明

为避免数据库刷写导致前端出错，已将项目做简单的动静分离：

- `backend/`：后端 FastAPI 示例与服务脚本（含 db 服务，数据库文件移到 `db/`）
- `static/`：所有静态前端页面（HTML/JS/CSS）放在此目录，便于做动静分离
- `db/`：数据库文件存放目录（例如 `my_ai_db.db`）

快速启动示例：

```bash
source venv/bin/activate
uvicorn backend.day5_db_server:app --reload
```

本地预览静态页面：

```bash
python -m http.server 5500 --directory static
# 打开 http://127.0.0.1:5500/index.html
```

---

> **坚持每天提交代码到 GitHub，记录从 0 到 1 的质变。**