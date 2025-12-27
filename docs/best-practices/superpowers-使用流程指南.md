# Superpowers 使用流程指南

> 快速上手指南 | 从安装到实战
> 更新日期：2025-12-27

---

## 快速开始（5 分钟）

### 第一步：安装 Superpowers

```bash
# 1. 注册市场
/plugin marketplace add obra/superpowers-marketplace

# 2. 安装插件
/plugin install superpowers@superpowers-marketplace

# 3. 退出并重启 Claude
# 退出后重新启动 claude
```

**重启后你会看到**：
```
<session-start-hook><EXTREMELY_IMPORTANT>
You have Superpowers.

**RIGHT NOW, go read**: @/Users/YOUR_NAME/.claude/plugins/cache/Superpowers/skills/getting-started/SKILL.md
</EXTREMELY_IMPORTANT></session-start-hook>
```

### 第二步：验证安装

```bash
# 检查可用命令
# 你应该看到：
/superpowers:brainstorm - 交互式设计优化
/superpowers:write-plan - 创建实现计划
/superpowers:execute-plan - 执行计划（带审查检查点）
```

### 第三步：开始使用

```bash
# 尝试第一个任务
/superpowers:brainstorm "我想实现一个 todo list 应用"
```

就这样！Superpowers 会自动引导你完成整个流程。

---

## 完整使用流程

### 流程概览图

```
┌─────────────────────────────────────────────────────┐
│           1. Brainstorming（头脑风暴）              │
│         明确需求，探索方案，达成共识                │
└─────────────────┬───────────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────────┐
│      2. Git Worktree（自动创建隔离环境）           │
│         新分支，独立目录，避免冲突                  │
└─────────────────┬───────────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────────┐
│         3. Write Plan（详细规划）                  │
│      任务分解，依赖映射，验收标准                  │
└─────────────────┬───────────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────────┐
│       4. Execute Plan（执行实现）                   │
│    选择执行方式：子代理驱动 OR 批量执行             │
└─────────────────┬───────────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────────┐
│        5. Auto TDD（自动测试驱动开发）              │
│        RED → GREEN → REFACTOR                       │
└─────────────────┬───────────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────────┐
│       6. Code Review（代码审查）                    │
│      规范检查，质量审查，问题修复                   │
└─────────────────┬───────────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────────┐
│     7. Finishing Branch（完成分支）                 │
│    验证测试，创建 PR/合并，清理环境                 │
└─────────────────────────────────────────────────────┘
```

---

## 详细步骤说明

### 步骤 1：Brainstorming（头脑风暴）

**何时使用**：你想实现任何新功能时

**如何使用**：

```bash
# 方式 1：明确命令
/superpowers:brainstorm "实现用户认证系统"

# 方式 2：自然对话
Claude: "我想添加 OAuth2 登录"
# Superpowers 会自动触发 brainstorming
```

**Claude 会做什么**：

```bash
# 1. 问澄清性问题
Claude: "需要哪些社交登录提供商？"
You: "Google, GitHub, Microsoft"

Claude: "是否需要本地用户账户？"
You: "需要"

Claude: "token 如何存储和刷新？"
You: "使用 JWT，存储在 httpOnly cookie"

Claude: "如何处理认证失败？"
You: "返回清晰的错误消息"

# 2. 探索多种方案
Claude: "我发现有几种实现方式：
  A. 使用 Passport.js
  B. 使用 Auth0
  C. 自定义实现

  推荐方案 A，因为..."

# 3. 识别潜在问题
Claude: "需要注意的问题：
  - CSRF 攻击防护
  - Token 安全存储
  - 会话管理"

# 4. 分块展示设计
Claude: "设计分为以下部分：
  ## 数据模型
  ...

  ## API 端点
  ...

  ## 安全考虑
  ..."

# 5. 等待你的确认
Claude: "这个设计看起来可以吗？
  需要调整哪些部分？"
```

**关键点**：
- ✅ 不要急，回答所有问题
- ✅ 讨论权衡和选择
- ✅ 确保你理解并同意设计
- ⚠️ 没有你的确认，不会进入下一步

### 步骤 2：Git Worktree（自动创建）

**何时触发**：Brainstorming 完成后，如果在 git 仓库中

**自动执行**：

```bash
# Claude 会自动：
1. 创建 git worktree
   $ git worktree add ../project-auth-feature auth-feature

2. 创建新分支
   $ git checkout -b feature/oauth-authentication

3. 进入新目录
   $ cd ../project-auth-feature

4. 运行项目设置
   $ npm install
   $ npm run setup

5. 验证测试基线
   $ npm test
   # 确保所有测试通过
```

**为什么这样做**：
- ✅ 主目录保持干净
- ✅ 可以同时开发多个功能
- ✅ 不会影响其他工作
- ✅ 容易丢弃和清理

### 步骤 3：Write Plan（编写计划）

**何时使用**：设计确认后

**如何使用**：

```bash
/superpowers:write-plan "实现与 Google、GitHub、Microsoft 的 OAuth2"
```

**生成的计划**：

```markdown
# OAuth2 认证实现计划

## 概述
实现 OAuth2 认证系统，支持三个社交登录提供商。

## 任务分解

### 任务 1: 设置 OAuth2 配置（5分钟）
**文件**: `src/config/oauth.js`
**内容**:
- 定义 provider 配置
- 设置环境变量
- 配置回调 URL

**验收标准**:
- [ ] 配置文件创建
- [ ] 环境变量文档更新
- [ ] 配置验证测试通过

### 任务 2: 创建认证控制器（10分钟）
**文件**: `src/controllers/authController.js`
**内容**:
- 实现登录端点
- 实现回调端点
- 实现登出端点

**验收标准**:
- [ ] 所有端点创建
- [ ] 输入验证完成
- [ ] 单元测试通过

### 任务 3: 实现 Token 存储（8分钟）
**文件**: `src/services/tokenService.js`
**内容**:
- JWT 生成逻辑
- Token 验证逻辑
- Token 刷新逻辑

**验收标准**:
- [ ] JWT 正确生成
- [ ] Token 验证可靠
- [ ] 刷新机制工作

### 任务 4: 添加错误处理（7分钟）
**文件**: `src/middleware/authErrorHandler.js`
**内容**:
- OAuth 错误捕获
- 用户友好的错误消息
- 日志记录

**验收标准**:
- [ ] 所有错误处理
- [ ] 清晰的错误消息
- [ ] 错误日志记录

### 任务 5: 编写集成测试（12分钟）
**文件**: `tests/integration/oauth.test.js`
**内容**:
- 完整登录流程测试
- 错误场景测试
- Token 刷新测试

**验收标准**:
- [ ] 主流程测试通过
- [ ] 边缘情况覆盖
- [ ] 测试覆盖率 > 80%

## 总时间估计
约 42 分钟

## 依赖关系
任务 1 → 任务 2 → 任务 3
                ↓
             任务 4
                ↓
             任务 5

## 风险和注意事项
- 需要 OAuth 应用凭据
- 回调 URL 必须正确配置
- 测试需要 mock OAuth 提供商
```

**关键点**：
- ✅ 每个任务 2-5 分钟可完成
- ✅ 明确的文件路径
- ✅ 清晰的验收标准
- ✅ 依赖关系可视化

### 步骤 4：Execute Plan（执行计划）

**执行方式选择**：

```bash
# Claude 会问你：
Claude: "执行方式：

A. Subagent-driven Development（推荐）
   - 每个任务独立子代理
   - 两阶段审查
   - 自主工作，速度快
   - 适合大多数场景

B. Batch Execution
   - 批量执行任务
   - 人工检查点
   - 更多控制
   - 适合需要监督的场景

选择 A 或 B："
```

#### 方式 A：Subagent-driven Development（推荐）

```bash
/superpowers:execute-plan

# Claude 会：
1. 启动第一个任务
   > [Subagent 1] 执行任务 1: 设置 OAuth2 配置

2. 第一阶段审查
   > [Reviewer] 检查：是否符合计划要求？
   > ✓ 通过

3. 第二阶段审查
   > [Reviewer] 检查：代码质量如何？
   > ✓ 通过

4. 继续下一个任务
   > [Subagent 2] 执行任务 2: 创建认证控制器

5. ... 循环直到所有任务完成
```

**优势**：
- ✅ 可以自主工作数小时
- ✅ 双重质量保证
- ✅ 并行处理能力
- ✅ 不需要持续监督

#### 方式 B：Batch Execution

```bash
/superpowers:execute-plan

# Claude 会：
1. 执行任务 1
   > 完成任务 1：设置 OAuth2 配置

2. 暂停检查点
   Claude: "任务 1 完成。继续下一个任务吗？"
   You: "继续"

3. 执行任务 2
   > 完成任务 2：创建认证控制器

4. 暂停检查点
   Claude: "任务 2 完成。继续下一个任务吗？"
   You: "让我检查一下..."
   You: "继续"

5. ... 循环直到所有任务完成
```

**优势**：
- ✅ 更多人工控制
- ✅ 可以随时调整方向
- ✅ 适合学习流程

### 步骤 5：Auto TDD（自动测试驱动开发）

**自动应用**：执行过程中，Superpowers 会强制使用 TDD。

**TDD 流程**：

```bash
# 任务：创建认证控制器

# RED 阶段
Claude: "编写失败的测试"

# 1. 先写测试
```javascript
// src/controllers/authController.test.js
describe('AuthController', () => {
  it('should redirect to OAuth provider', () => {
    const result = authController.login('google');
    expect(result.url).toContain('accounts.google.com');
  });
});
```

# 2. 确认测试失败
Claude: "运行测试..."
> $ npm test
> FAIL  authController.test.js
> ✗ AuthController › should redirect to OAuth provider
>   ReferenceError: authController is not defined
Claude: "✓ 测试失败（RED）"

# GREEN 阶段
Claude: "编写最小代码使测试通过"

# 3. 写最简单的代码
```javascript
// src/controllers/authController.js
const authController = {
  login: (provider) => ({
    url: `https://${provider}.com/oauth`
  })
};

module.exports = authController;
```

# 4. 确认测试通过
Claude: "运行测试..."
> $ npm test
> PASS  authController.test.js
> ✓ AuthController › should redirect to OAuth provider
Claude: "✓ 测试通过（GREEN）"

# REFACTOR 阶段
Claude: "改进代码结构"

# 5. 在测试保护下重构
```javascript
// src/controllers/authController.js
const oauthConfig = require('../config/oauth');

const authController = {
  login: (provider) => {
    const config = oauthConfig.getProvider(provider);
    return {
      url: config.authUrl,
      state: generateState()
    };
  }
};

function generateState() {
  return Math.random().toString(36);
}

module.exports = authController;
```

# 6. 确认测试仍然通过
Claude: "运行测试..."
> $ npm test
> PASS  authController.test.js
> ✓ AuthController › should redirect to OAuth provider
Claude: "✓ 测试仍然通过"

# 7. 提交
Claude: "提交代码..."
> $ git add .
> $ git commit -m "feat: implement OAuth login redirect"
```

**关键规则**：
- ⚠️ **如果在测试之前写了代码，Superpowers 会删除它！**
- ⚠️ **必须先写测试，确认失败**
- ⚠️ **然后写最小代码，确认通过**
- ⚠️ **最后重构，保持测试通过**

### 步骤 6：Code Review（代码审查）

**何时触发**：每个任务完成后

**两阶段审查**：

```bash
# 任务完成后自动触发

# 第一阶段：规范合规性
Reviewer: "检查计划符合性..."

检查项：
✓ 是否完成计划要求的所有功能？
✓ 是否遵循了验收标准？
✓ 是否在时间估算内完成？
✓ 依赖关系是否正确？

结果：✓ 通过 / ✗ 不通过

# 第二阶段：代码质量
Reviewer: "检查代码质量..."

检查项：
✓ 代码是否清晰易读？
✓ 是否有充分的测试？
✓ 性能是否可接受？
✓ 是否遵循最佳实践？
✓ 是否有安全问题？

结果：✓ 通过 / ✗ 不通过

# 如果不通过
Reviewer: "发现问题：
- Critical: 缺少输入验证
- Major: 错误处理不完整
- Minor: 变量命名不够清晰

需要修复..."
```

**问题分级**：

| 级别 | 描述 | 处理 |
|------|------|------|
| **Critical** | 阻止发布的问题 | 必须立即修复，不能继续 |
| **Major** | 重要质量问题 | 应该修复，建议修复后继续 |
| **Minor** | 改进建议 | 可以记录，继续进行 |

### 步骤 7：Finishing Branch（完成分支）

**何时触发**：所有任务完成后

**Claude 会问**：

```bash
Claude: "所有任务完成！

验证结果：
✓ 所有测试通过（42/42）
✓ 代码审查完成
✓ 无 Critical 问题
✓ 文档已更新

接下来你想：

A. 创建 Pull Request
   - 推送到远程
   - 在 GitHub 创建 PR
   - 包含详细的变更说明

B. 本地合并
   - 合并回主分支
   - 不创建 PR
   - 适合个人项目

C. 保留分支
   - 暂时不合并
   - 继续工作
   - 稍后决定

D. 丢弃工作
   - 删除 worktree
   - 放弃更改
   - 适合实验性功能

选择 A/B/C/D："
```

**选择 A - 创建 PR**：

```bash
# Claude 会：
1. 推送到远程
   $ git push -u origin feature/oauth-authentication

2. 创建 PR
   $ gh pr create \
     --title "feat: Add OAuth2 authentication" \
     --body "## 概述
实现 OAuth2 认证系统，支持 Google、GitHub、Microsoft。

## 变更
- 添加 OAuth 配置
- 实现认证控制器
- 实现 token 服务
- 添加错误处理
- 编写集成测试

## 测试
- 所有测试通过（42/42）
- 测试覆盖率 85%

## 检查清单
- [x] 代码审查完成
- [x] 文档更新
- [x] 测试通过

Co-Authored-By: Claude <noreply@anthropic.com>"

3. 清理 worktree
   $ cd ..
   $ git worktree remove ../project-auth-feature

4. 返回主目录
   $ cd project-main
```

---

## 实际使用示例

### 示例 1：实现 Todo List 应用

```bash
# 开始
You: 我想实现一个 todo list 应用

# 自动触发 brainstorming
Claude: "我们来明确需求..."

# 提问和讨论...
Claude: "需要哪些功能？"
You: "添加、删除、标记完成"

Claude: "数据存储在哪里？"
You: "使用 localStorage"

Claude: "需要分类吗？"
You: "需要，可以创建多个列表"

# ... 更多问题 ...

# 设计确认
Claude: "这是设计方案... 看起来可以吗？"
You: "可以"

# 自动创建 worktree
Claude: "创建隔离环境..."
> $ git worktree add ../project-todo feature/todo-app

# 编写计划
Claude: "生成实现计划..."
> 共 8 个任务，预计 45 分钟

# 执行
You: /superpowers:execute-plan

Claude: "选择执行方式：
A. Subagent-driven（推荐）
B. Batch execution
"
You: "A"

# 自动执行...
> [Subagent 1] 任务 1：创建 HTML 结构 ✓
> [Reviewer] 第一阶段审查 ✓
> [Reviewer] 第二阶段审查 ✓
> [Subagent 2] 任务 2：实现 CSS 样式 ✓
> ...

# 完成后
Claude: "所有任务完成！
✓ 所有测试通过
✓ 代码审查完成

接下来：A. 创建 PR  B. 本地合并  C. 保留  D. 丢弃"
You: "B"

Claude: "合并到主分支...
> $ git checkout main
> $ git merge feature/todo-app
> $ git worktree remove ../project-todo

完成！"
```

### 示例 2：修复生产 Bug

```bash
# 开始
You: 生产环境的登录功能出问题了

# 自动触发 systematic-debugging
Claude: "开始系统化调试...

## 阶段 1：问题识别

收集证据：
- 错误信息：'Invalid token'
- 发生时间：每次登录
- 影响范围：所有用户

确定失败点：token 验证函数

## 阶段 2：假设形成

可能原因：
A. Token 过期时间设置错误
B. Token 验证逻辑有 bug
C. Secret key 配置错误

## 阶段 3：假设测试

测试假设 A：检查 token 过期时间
> $ grep 'EXPIRES_IN' .env
> EXPIRES_IN=1h
> 正常

测试假设 B：检查验证逻辑
> 查看代码...
> 发现 bug：时间比较使用了错误的运算符
> ✓ 找到根因！

## 阶段 4：解决方案实施

修复：将 '<' 改为 '<='
测试：添加单元测试
验证：运行测试套件 ✓
文档：更新 CHANGELOG

完成！根因已修复并验证。"
```

---

## 常见使用场景

### 场景 1：日常功能开发

```bash
/superpowers:brainstorm "功能描述"
  ↓ 回答问题，讨论设计
/superpowers:write-plan "实现目标"
  ↓ 查看计划，调整任务
/superpowers:execute-plan
  ↓ 选择执行方式
  ↓ 等待完成
  ↓ 选择 PR/合并/保留/丢弃
```

### 场景 2：快速 Bug 修复

```bash
You: "有个 bug 需要修复"

# 自动触发 systematic-debugging
# Claude 会自动进行 4 阶段调试

# 完成后自动触发 verification-before-completion
# Claude 会验证修复是否完整
```

### 场景 3：代码重构

```bash
/superpowers:brainstorm "重构用户认证模块"
  ↓ 讨论重构目标和范围
/superpowers:write-plan "重构计划"
  ↓ 重构步骤和测试策略
/superpowers:execute-plan
  ↓ 自动应用 TDD
  ↓ 在测试保护下安全重构
```

### 场景 4：并行开发

```bash
# Terminal 1
$ cd project-auth/
$ git worktree add ../project-auth feature-auth
$ claude
> /superpowers:brainstorm "用户认证"
> /superpowers:execute-plan

# Terminal 2
$ cd project-profile/
$ git worktree add ../project-profile feature-profile
$ claude
> /superpowers:brainstorm "用户资料"
> /superpowers:execute-plan

# Terminal 3
$ cd project-notifications/
$ git worktree add ../project-notifications feature-notifications
$ claude
> /superpowers:brainstorm "通知系统"
> /superpowers:execute-plan

# 三个功能同时开发，零冲突！
```

---

## 技巧和最佳实践

### 1. 信任自动触发

```bash
❌ 不要：
> /superpowers:brainstorm
> /superpowers:systematic-debugging
> /superpowers:test-driven-development

✅ 应该：
# 自然对话，让 Claude 决定使用哪个技能
"我想实现一个功能"
"有个 bug 需要修复"
"需要重构这段代码"
```

### 2. 充分参与 Brainstorming

```bash
✅ 好的做法：
- 回答所有问题
- 讨论不同的方案
- 表达你的偏好
- 确保理解设计
- 不要急于进入下一步

⚠️ 避免的陷阱：
- "随便，看着办"
- "快点开始写代码"
- 跳过讨论阶段
```

### 3. 选择合适的执行方式

```bash
# Subagent-driven（推荐）
✅ 适合：
- 大型功能（10+ 任务）
- 信任 Claude 的判断
- 想要速度和效率
- 可以在完成后审查

# Batch execution
✅ 适合：
- 学习 Superpowers 流程
- 需要更多控制
- 不确定的任务
- 想要逐步审查
```

### 4. 利用 Git Worktree

```bash
# 创建多个 worktree 并行开发
git worktree add ../project-a feature-a
git worktree add ../project-b feature-b
git worktree add ../project-c feature-c

# 在不同终端分别启动 Claude
# 每个独立工作，互不干扰

# 完成后清理
git worktree remove ../project-a
git worktree remove ../project-b
git worktree remove ../project-c
```

### 5. 定期使用 /clear

```bash
# 在不同任务之间清理上下文
/superpowers:execute-plan
# ... 完成第一个功能
/clear
# 清理上下文，准备下一个任务
/superpowers:brainstorm "下一个功能"
```

---

## 故障排除

### 问题 1：技能未触发

**症状**：Claude 直接开始写代码，没有 brainstorming

**解决**：

```bash
# 手动触发
/superpowers:brainstorm "你的任务"

# 或者明确告诉 Claude
"请先使用 brainstorming 技能讨论设计方案"
```

### 问题 2：Worktree 创建失败

**症状**：无法创建 git worktree

**解决**：

```bash
# 清理损坏的 worktree
git worktree prune

# 检查磁盘空间
df -h

# 手动创建
git worktree add ../project-feature feature-branch
```

### 问题 3：子代理失败

**症状**：子代理没有按指令行事

**解决**：

```bash
# 切换到批量执行模式
/superpowers:execute-plan
# 选择 B: Batch execution

# 或者更具体的指令
"请一步步执行，每完成一个任务暂停"
```

### 问题 4：TDD 删除代码

**症状**：在测试之前写的代码被删除了

**说明**：这是正常行为！

```bash
# 正确流程：
# 1. 先写测试
# 2. 确认测试失败
# 3. 写代码
# 4. 确认测试通过

# 不要在测试之前写代码
```

---

## 快速参考卡

```
┌─────────────────────────────────────────┐
│      Superpowers 核心命令              │
├─────────────────────────────────────────┤
│ /superpowers:brainstorm "任务"        │
│   → 头脑风暴，明确需求                 │
│                                         │
│ /superpowers:write-plan "目标"         │
│   → 详细规划，任务分解                 │
│                                         │
│ /superpowers:execute-plan              │
│   → 执行实现，自动 TDD                 │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│      自动触发的技能                     │
├─────────────────────────────────────────┤
│ • systematic-debugging (调试)          │
│ • test-driven-development (TDD)        │
│ • verification-before-completion (验证)│
│ • code-review (代码审查)              │
│ • using-git-worktrees (工作树)        │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│      执行方式选择                       │
├─────────────────────────────────────────┤
│ A. Subagent-driven (推荐)              │
│    → 快速、自主、双重审查              │
│                                         │
│ B. Batch Execution                     │
│    → 控制、逐步、人工检查点            │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│      完成选项                           │
├─────────────────────────────────────────┤
│ A. 创建 PR (团队协作)                  │
│ B. 本地合并 (个人项目)                 │
│ C. 保留分支 (继续工作)                 │
│ D. 丢弃工作 (实验功能)                 │
└─────────────────────────────────────────┘
```

---

## 下一步

1. **从简单任务开始**
   - 先熟悉流程
   - 了解每个阶段
   - 建立信任

2. **逐步提高复杂度**
   - 从 2-3 个任务开始
   - 逐步增加到 10+ 任务
   - 尝试并行开发

3. **创建自定义技能**
   - 识别重复工作
   - 提取可复用流程
   - 编写自己的技能

4. **团队推广**
   - 小范围试点
   - 收集反馈
   - 建立最佳实践
   - 逐步推广

---

**维护者**: Claude Code Research Team
**最后更新**: 2025-12-27
**更多文档**: `docs/best-practices/superpowers-最佳实践指南.md`
