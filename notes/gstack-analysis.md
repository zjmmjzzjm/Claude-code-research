# gstack 分析 — garrytan/gstack

> 仓库地址：https://github.com/garrytan/gstack
> 作者：Garry Tan（Y Combinator CEO）
> 许可证：MIT

## 概述

gstack 是一个开源的 Claude Code 技能框架，目标是将 Claude Code 变成**虚拟工程团队**。提供 28 个斜杠命令技能（slash-command skills），覆盖完整的开发 sprint 周期。Garry Tan 声称用它在 60 天内（兼职）完成了 60 万+ 行生产代码。

## 技术栈

| 组件 | 技术 | 说明 |
|------|------|------|
| 运行时 | Bun >= 1.0.0 | 单文件部署 ~58MB，内置 SQLite，原生 TypeScript |
| 语言 | TypeScript | 主要开发语言 |
| 浏览器 | Playwright ^1.58.2 | 无头 Chromium，可访问性树 API |
| HTTP | Bun.serve() | 轻量内置服务器 |
| AI | Anthropic SDK ^0.78.0 | Claude API 集成 |

## 核心架构

### 1. 浏览器自动化系统（Browse Module）

与传统 MCP 方案不同，采用**持久无头 Chromium 守护进程 + 轻量 CLI 客户端**架构：

```
Claude Code → CLI 客户端 → HTTP 请求 → Bun HTTP 服务器 → Playwright → Chromium
```

性能对比：
- 首次调用 ~3 秒（启动 Chromium），后续 ~100-200ms
- MCP 方案通常首次 ~5s，后续 ~2-5s + 30,000-40,000 tokens 协议开销

**Ref 系统（关键创新）：**
- 使用 Playwright 可访问性树 API（非 DOM 注入）
- 自动为每个元素分配 `@e1`, `@e2` 等引用标签
- 扩展 `@c1`, `@c2` 用于 cursor:pointer 的 div 元素
- 通过 async `count()` 检测 SPA 中的 ref 过时，快速失败而非超时

命令分类（50+ 命令）：
- **READ**（非变异）：text、html、links、forms、js、css、network、console
- **WRITE**（变异）：click、fill、select、upload、dialog-accept
- **META**（元操作）：snapshot、screenshot、tabs、diff、chain

### 2. Skill 系统

每个技能是自包含的 Markdown 文件（SKILL.md），包含 YAML 前置元数据、流程引导和决策树。

28 个主要技能分类：

| 类别 | 技能 | 用途 |
|------|------|------|
| 规划 | office-hours、plan-ceo-review、plan-eng-review、plan-design-review | 产品定义和架构评审 |
| 开发 | review、investigate、design-review | 代码审查和调试 |
| 测试 | qa、qa-only、benchmark、canary | QA 自动化和性能监控 |
| 安全 | cso | OWASP + STRIDE 威胁建模 |
| 发布 | ship、land-and-deploy | PR 创建和部署 |
| 防护 | careful、freeze、guard | 防止危险命令误操作 |
| 工具 | browse、setup-browser-cookies、retro、document-release | 浏览器自动化和文档化 |

### 3. 目录结构

```
gstack/
├── browse/                    # 核心浏览器自动化模块
│   ├── src/
│   │   ├── cli.ts             # CLI 客户端
│   │   ├── server.ts          # Bun HTTP 服务器
│   │   ├── browser-manager.ts # Chromium 生命周期
│   │   ├── snapshot.ts        # 可访问性树 → @ref 映射
│   │   ├── read-commands.ts   # 非变异命令
│   │   ├── write-commands.ts  # 变异命令
│   │   └── meta-commands.ts   # 元操作命令
│   └── dist/browse            # 编译的二进制 (~58MB)
├── review/                    # 代码审查技能
├── plan-ceo-review/           # CEO 产品审查
├── plan-eng-review/           # 工程架构审查
├── qa/                        # QA 自动化测试
├── ship/                      # 发布部署
├── investigate/               # 系统化调试
├── cso/                       # 安全审计
├── careful/ & freeze/         # 安全防护
├── test/                      # 测试套件
├── ARCHITECTURE.md            # 架构文档
├── ETHOS.md                   # 构建哲学
└── BROWSER.md                 # 浏览器命令参考
```

## 使用场景

### 1. 独立开发者当团队用

核心场景：一个人干一个团队的活。通过 skill 把 Claude Code 编排成产品经理、架构师、QA、安全官等多个角色。

### 2. 完整 Sprint 工作流

```
想法 → /office-hours（头脑风暴）
     → /plan-ceo-review（CEO 视角挑战需求）
     → /plan-eng-review（架构评审）
     → 写代码
     → /review（代码审查）
     → /qa https://staging.myapp.com（浏览器 QA）
     → /cso（安全审计）
     → /ship（创建 PR 发布）
     → /retro（回顾复盘）
```

### 3. 浏览器自动化测试

- QA 验收：自动打开站点，点击、填表、截图对比
- 视觉回归：snapshot diff 检测页面变化
- 带登录态测试：导入 Chrome cookie
- 前端调试：console 错误、network 请求检查

### 4. 安全防护

- `/careful`：防止 `rm -rf`、`DROP TABLE`、`git push --force` 等危险操作
- `/freeze src/auth`：锁定目录，防止意外修改关键代码
- `/cso`：OWASP Top 10 + STRIDE 威胁建模审计

### 5. 团队标准化

通过 skill 固化最佳实践为可执行流程，新人跑 `/review` + `/qa` + `/cso` 即可达到老手审查标准。

## 设计哲学

### Boil the Lake（完整性原则）

AI 让边际成本趋近零时，做完整的事：100% 测试覆盖而非 90%，完整特性而非快速原型。

效率压缩比（人工 vs AI 辅助）：
- 样板代码：100x
- 测试编写：50x
- 特性实现：30x
- 错误修复：20x
- 架构设计：5x
- 研究探索：3x

### Search Before Building（先搜索后构建）

三层知识结构：
1. 经验法则层 — 战斗检验的模式
2. 新趋势层 — 当前最佳实践
3. 第一原理层 — 基于具体问题的原始观察

## 安全模型

- 仅本地绑定（127.0.0.1）
- Bearer Token（每会话随机 UUID，文件权限 0o600）
- Cookie 只读（复制到临时文件，从不修改原文件）
- 硬编码路径（防止 shell 注入）
- 无明文日志（Cookie 值仅在内存中解密）
- 30 分钟空闲自动关闭

## 对比分析

| 维度 | gstack | 一般 skill 仓库 |
|------|--------|----------------|
| 定位 | 全流程 sprint 框架 | 日常开发辅助 |
| 特色 | 浏览器自动化 + 角色模拟 | 轻量实用技能 |
| 复杂度 | 重（含编译的 browse 二进制） | 轻（纯 Markdown） |
| 适合 | 独立开发完整产品 | 团队日常提效 |

## 借鉴价值

1. **浏览器自动化**：持久守护进程 + Ref 系统的设计思路，比 MCP 方案更高效
2. **角色模拟**：通过 skill 让 AI 扮演 CEO/CTO/QA/CSO 多角色审查
3. **安全防护**：careful/freeze/guard 的分层防护机制
4. **完整性哲学**：AI 时代追求完整而非最小可行，值得思考
