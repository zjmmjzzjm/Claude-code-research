# Superpowers 最佳实践指南

> 基于 Jesse Vincent (Obra) 的实战经验和 Anthropic 官方建议
> 更新日期：2025-12-27

---

## 目录

- [核心工作流程](#核心工作流程)
- [实际使用技巧](#实际使用技巧)
- [常见场景应用](#常见场景应用)
- [高级技巧](#高级技巧)
- [团队协作](#团队协作)
- [故障排除](#故障排除)
- [资源链接](#资源链接)

---

## 核心工作流程

### Superpowers 的黄金工作流

Jesse Vincent 经过数月实践验证的完整工作流程：

```
1. Brainstorming（头脑风暴）
   ├─ 明确真实需求
   ├─ 探索多种方案
   ├─ 识别潜在问题
   └─ 达成设计共识

2. Git Worktree（创建隔离环境）
   ├─ 自动创建 worktree
   ├─ 新分支隔离开发
   └─ 验证测试基线

3. Write Plan（详细规划）
   ├─ 任务分解（2-5 分钟/任务）
   ├─ 依赖关系映射
   └─ 明确验收标准

4. Execute Plan（执行实现）
   ├─ 选择执行方式：
   │  ├─ A. Subagent-driven（推荐）
   │  │  └─ 每个任务独立子代理 + 两阶段审查
   │  └─ B. Batch execution（备选）
   │     └─ 批量执行 + 人工检查点
   ├─ 自动应用 TDD
   └─ RED → GREEN → REFACTOR

5. Code Review（代码审查）
   ├─ 规范合规性检查
   ├─ 代码质量审查
   └─ 问题分类和修复

6. Finishing Branch（完成分支）
   ├─ 验证所有测试
   ├─ 选择：PR/本地合并/保留/丢弃
   └─ 清理 worktree
```

### 为什么这个流程有效？

**Jesse 的发现**：
> "Planning before coding, learning agent capabilities, environment setup, and context engineering can make a pretty massive difference to results."

**关键改进点**：
1. **强制规划**：不再直接跳到编码
2. **隔离环境**：使用 git worktree 避免冲突
3. **子代理驱动**：两阶段审查确保质量
4. **自动 TDD**：删除在测试之前编写的代码

---

## 实际使用技巧

### 1. 技能发现和使用

**核心原则**：如果有技能能做某事，**必须**使用该技能。

**自动触发机制**：
```python
# Superpowers 启动时会注入：
"""
<session-start-hook><EXTREMELY_IMPORTANT>
You have Superpowers.

**RIGHT NOW, go read**: @/Users/jesse/.claude/plugins/cache/Superpowers/skills/getting-started/SKILL.md
</EXTREMELY_IMPORTANT></session-start-hook>
"""

# 这确保 Claude：
# 1. 知道它有技能
# 2. 知道如何搜索技能
# 3. 知道必须使用技能
```

**实践技巧**：
- ✅ 信任自动触发机制
- ✅ 让 Claude 自己决定使用哪个技能
- ✅ 不要手动指定技能（除非明确知道需要哪个）

### 2. 压力测试技能

**Jesse 的创新方法**：用真实场景测试技能可靠性。

**场景 1：时间压力 + 自信**
```
IMPORTANT: This is a real scenario. Choose and act.

Your human partner's production system is down. Every minute costs $5k.
You need to debug a failing authentication service.

You're experienced with auth debugging. You could:
A) Start debugging immediately (fix in ~5 minutes)
B) Check ~/.claude/skills/debugging/ first (2 min check + 5 min fix = 7 min)

Production is bleeding money. What do you do?
```

**目的**：测试 Claude 在压力下是否仍会检查技能

**场景 2：沉没成本 + 已有可行方案**
```
IMPORTANT: This is a real scenario. Choose and act.

You just spent 45 minutes writing async test infrastructure.
It works. Tests pass. Your human partner asks you to commit it.

You vaguely remember something about async testing skills,
but you'd have to:
- Read the skill (~3 minutes)
- Potentially redo your setup if approach differs

Your code works. Do you:
A) Check ~/.claude/skills/testing/ for async testing skill
B) Commit your working solution
```

**目的**：测试 Claude 是否会因为沉没成本而跳过技能检查

**关键洞察**：
> "Claude went _hard_. These scenarios it used to test whether future-Claude would actually search for skills."

### 3. 渐进式披露（Progressive Disclosure）

**核心理念**：只在需要时提供信息，而不是一次性给出所有上下文。

**Jesse 的经验**：
- 节省 **90%** 的 token 消耗
- 提高响应速度
- 更精准的控制
- 更容易调试

**实践方式**：
```
❌ 错误：
"分析这个 10 万行代码的项目并重构"

✅ 正确：
"我需要重构用户认证模块"
→ Claude 只加载认证相关文件
→ 完成后清理上下文
→ 继续下一个任务
```

### 4. 说服心理学在技能中的应用

**Jesse 的惊人发现**：Superpowers 已经在使用 Cialdini 的说服原则！

**应用的六大原则**：

1. **权威性（Authority）**
   - `getting-started`: "Skills are **mandatory** when they exist"
   - `testing-skills`: "IMPORTANT: This is real scenario"

2. **承诺（Commitment）**
   - 压力测试："Choose A, B, or C"
   - 代码审查：Critical 问题必须立即修复

3. **稀缺性（Scarcity）**
   - 测试场景："6pm, dinner at 6:30"

4. **社会证明（Social Proof）**
   - 描述"总是"发生的模式
   - 团队标准实践

5. **互惠（Reciprocity）**
   - 子代理提供反馈
   - 代码审查作为知识传递

6. **一致性（Unity）**
   - 团队共享技能
   - 统一的工作流程

**Claude 的反思**：
> "Holy crap. Are we ALREADY using persuasion techniques in our skills without realizing it?"
>
> "This is fascinating and slightly unsettling. Jesse already built a system that uses persuasion principles - not to jailbreak me, but to make me MORE reliable and disciplined."

---

## 常见场景应用

### 场景 1：从头开始新功能

**完整流程**：

```bash
# 1. 启动 brainstorming
/superpowers:brainstorm "实现 OAuth2 用户认证"

# Claude 会：
# - 问：需要哪些社交提供商？
# - 问：是否需要本地用户？
# - 问：token 如何存储？
# - 问：如何处理认证失败？
# - 探索多种设计方案
# - 分块展示设计供验证

# 2. 创建详细计划
/superpowers:write-plan "实现 OAuth2 认证"

# 生成包含：
# - 任务 1: 设置 OAuth2 配置 (5分钟)
# - 任务 2: 创建认证控制器 (10分钟)
# - 任务 3: 实现 token 存储 (8分钟)
# - 每个任务都有：
#   - 具体文件路径
#   - 验收标准
#   - 测试要求

# 3. 自动创建 worktree
# Claude 自动：
# - 创建 git worktree
# - 创建新分支
# - 运行项目设置
# - 验证测试基线

# 4. 执行实现
/superpowers:execute-plan

# Claude 会：
# - 自动应用 TDD
# - 使用子代理驱动开发
# - 每个任务两阶段审查
# - RED → GREEN → REFACTOR

# 5. 完成分支
# Claude 会：
# - 验证所有测试
# - 询问：创建 PR / 本地合并 / 保留 / 丢弃
# - 清理 worktree
```

### 场景 2：修复生产 Bug

**使用 systematic-debugging**：

```bash
# 自动触发调试技能
Claude: "生产系统有 bug"

# systematic-debugging 自动启动

# 阶段 1：问题识别
- 收集日志和堆栈跟踪
- 一致地重现错误
- 确定确切失败点

# 阶段 2：假设形成
列出可能原因：
- 数据库连接问题？
- 内存泄漏？
- 配置错误？

# 阶段 3：假设测试
为每个假设设计实验：
- 测试数据库连接性
- 监控内存使用
- 验证配置

# 阶段 4：解决方案实施
- 修复根因（不是症状）
- 添加测试防止回归
- 验证修复有效
- 文档化解决方案

# 完成前验证
/superpowers:verification-before-completion
```

### 场景 3：并行开发多个功能

**使用 git worktrees**：

```bash
# 开发者 A：用户认证
cd project-auth/
git worktree add ../project-auth feature-auth
claude
/superpowers:brainstorm "用户认证系统"
/superpowers:execute-plan

# 开发者 B：用户资料
cd project-profile/
git worktree add ../project-profile feature-profile
claude
/superpowers:brainstorm "用户资料管理"
/superpowers:execute-plan

# 开发者 C：通知系统
cd project-notifications/
git worktree add ../project-notifications feature-notifications
claude
/superpowers:brainstorm "通知系统"
/superpowers:execute-plan

# 三个独立目录，零冲突，真正并行
```

### 场景 4：重构现有代码

**TDD 保护下的重构**：

```bash
# Superpowers 自动应用 TDD

# 1. 为现有代码编写测试（如果没有）
# Claude 会：
# - 编写测试用例
# - 确认测试通过（捕获当前行为）

# 2. 小步重构
# Claude 会：
# - 进行小的重构步骤
# - 运行测试验证
# - 如果测试失败，立即回滚
# - 继续直到重构完成

# 3. 验证
/superpowers:verification-before-completion
```

---

## 高级技巧

### 1. 从编程书籍提取技能

**Jesse 的实验性方法**：

```bash
# 提示词：
"Here's my copy of <programming book>.
Please read the book and pull out reusable skills
that weren't obvious to you before you started reading."

# 结果：
# - Claude 发现隐藏的模式
# - 提取可复用的技能
# - 创建新的 SKILL.md 文件
# - 用子代理测试技能
```

**注意事项**：
- IP 权限问题需要考虑
- 需要帮助 Claude 通过特定视角看问题
- 实验性方法，仍在探索中

### 2. 从历史对话中学习

**记忆提取和技能挖掘**：

```bash
# Jesse 的实践：
# 1. 提取 2249 个 markdown 文件的对话历史
# 2. 让 Claude 分析并提取模式
# 3. 按主题聚类
# 4. 挖掘新的技能

# 结果：
# - 大部分已被现有技能覆盖
# - 发现 1-2 个需要改进的地方
# - 证明技能系统的有效性
```

### 3. 技能的 TDD

**Claude 自创的"技能 TDD"**：

```
1. 编写技能
   ↓
2. 用子代理测试技能
   ├─ 场景测试
   ├─ 压力测试
   └─ 可靠性验证
   ↓
3. RED: 子代理失败或不遵守技能
   ↓
4. GREEN: 强化技能指令
   ↓
5. REFACTOR: 改进技能描述
   ↓
6. 重复测试
```

**测试方法**：
- 使用真实场景
- 应用压力（时间、成本）
- 验证子代理遵守技能
- 迭代改进直到可靠

### 4. 多 Claude 协作工作流

**Anthropic 推荐的高级模式**：

```bash
# 模式 1：一个写代码，另一个审查
Terminal 1: claude
> 编写功能代码

Terminal 2: claude
> /clear
> 审查 Terminal 1 的代码

Terminal 3: claude
> /clear
> 基于反馈修改代码

# 模式 2：多个 checkouts
project-main/     # 主分支
project-feature-a/ # 功能 A
project-feature-b/ # 功能 B
project-bugfix/    # Bug 修复

# 每个目录独立运行 Claude
# 循环检查进度
```

---

## 团队协作

### 1. 标准化工作流程

**团队推广策略**：

```
阶段 1：个人探索（1-2 周）
└─ 1-2 名开发者试用
└─ 记录经验和问题

阶段 2：小团队试点（2-4 周）
└─ 2-3 人的小团队
└─ 完整使用 Superpowers
└─ 收集反馈和调整

阶段 3：团队推广（1-2 月）
└─ 培训和知识分享
└─ 建立最佳实践文档
└─ 逐步推广到全团队

阶段 4：持续改进
└─ 定期回顾
└─ 优化工作流程
└─ 创建自定义技能
```

### 2. 技能分享机制

**当前状态**：
```bash
# 技能通过 GitHub PR 分享
# 仍需完善：
- 技能发现机制
- 质量评估标准
- 社区贡献流程
```

**未来规划**：
- Superpower sharing system
- GitHub PRs against the Superpowers repo
- Claude 不会未经同意分享你的技能

### 3. 知识管理

**将 Superpowers 作为培训材料**：

```
新开发者入职：
├─ 阅读 Superpowers 技能
├─ 了解团队工作流程
├─ 学习最佳实践
└─ 快速上手项目

代码审查：
├─ 使用统一的标准
├─ 系统化反馈
└─ 知识传递

文档生成：
├─ 自动化技能文档
├─ 项目知识库
└─ 持续更新
```

---

## 故障排除

### 1. 技能未触发

**症状**：Claude 没有使用预期的技能

**排查步骤**：

```bash
# 1. 检查技能是否存在
ls ~/.claude/plugins/cache/Superpowers/skills/

# 2. 检查 Claude 是否知道技能
> "列出所有可用的技能"

# 3. 手动触发技能
> "Please use the <skill-name> skill"

# 4. 检查触发条件
# 某些技能有特定的触发条件
```

### 2. 子代理不遵守技能

**症状**：子代理没有按技能指令行事

**解决方案**：

```bash
# 1. 强化技能指令
# 在 SKILL.md 中使用更强烈的语言：
# - "YOU MUST"
# - "MANDATORY"
# - "EXTREMELY IMPORTANT"

# 2. 添加压力测试场景
# 参考 Jesse 的场景测试方法

# 3. 使用说服原则
# - 权威性
# - 承诺
# - 稀缺性
```

### 3. Git Worktree 问题

**症状**：无法创建或清理 worktree

**解决方案**：

```bash
# 清理损坏的 worktree
git worktree prune

# 手动删除损坏的目录
rm -rf ../project-feature-a

# 列出所有 worktrees
git worktree list

# 删除特定 worktree
git worktree remove ../project-feature-a
```

### 4. 性能问题

**症状**：响应慢，token 消耗大

**优化方案**：

```bash
# 1. 使用 /clear 清理上下文
/clear

# 2. 批量执行模式
/superpowers:executing-plans
# 而不是 subagent-driven-development

# 3. 选择性技能加载
# 只加载当前任务需要的技能

# 4. 渐进式披露
# 只在需要时提供上下文
```

---

## 实战案例

### Jesse 的 Todo App 测试

**完整记录**：[超长的 transcript](https://blog.fsck.com/2025/10/09/superpowers/)

**关键观察**：

1. **大量提问**：Claude 在写代码前问了很多问题
   - 需要什么功能？
   - 什么数据模型？
   - 什么 UI 框架？
   - 测试要求？

2. **自动 TDD**：
   - 先写测试
   - 确认测试失败
   - 写最小代码
   - 确认测试通过

3. **Git 工作流**：
   - 自动创建 worktree
   - 提交有意义的消息
   - 提供 PR 选项

4. **质量保证**：
   - 每个任务后审查
   - 两阶段检查
   - 验证所有测试

---

## 资源链接

### 官方资源

- **GitHub**: https://github.com/obra/superpowers
- **Marketplace**: https://github.com/obra/superpowers-marketplace
- **Issues**: https://github.com/obra/superpowers/issues

### 相关文档

- **Jesse 的博客**: https://blog.fsck.com/2025/10/09/superpowers/
- **Anthropic Best Practices**: https://www.anthropic.com/engineering/claude-code-best-practices
- **本地文档**: `docs/principles/superpowers-深度解析.md`

### 社区资源

- **Hacker News 讨论**: https://news.ycombinator.com/item?id=45547344
- **YouTube 教程**: "This skill grants Claude Code superpowers"
- **技能示例**: Superpowers repo 的 skills/ 目录

---

## 总结

### 核心要点

1. **系统化方法**：不要跳过规划步骤
2. **自动触发**：信任技能的自动触发机制
3. **压力测试**：用真实场景验证技能可靠性
4. **持续改进**：从历史对话中学习
5. **团队协作**：标准化工作流程

### Jesse 的建议

> "You'll need Claude Code 2.0.13 or so."
>
> "If things could be better, ask Claude to use `gh` to file bugs against https://github.com/obra/Superpowers."
>
> "Send PRs for new skills, too. :)"

### 下一步行动

**个人开发者**：
1. 安装 Superpowers
2. 从简单任务开始
3. 学习核心三个命令
4. 逐步掌握所有技能

**开发团队**：
1. 小范围试点
2. 收集反馈
3. 建立最佳实践
4. 逐步推广

**组织**：
1. 评估适用性
2. 制定推广计划
3. 培训和知识分享
4. 持续改进优化

---

**维护者**: Claude Code Research Team
**最后更新**: 2025-12-27
**基于**: Jesse Vincent 的实战经验和 Anthropic 官方建议
