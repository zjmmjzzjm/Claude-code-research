# Jesse Vincent 对 Claude Code 的深度理解

> 基于其 2025 年博客文章分析

## 核心观点

Claude Code 不仅仅是一个代码生成工具，而是一个**可以通过系统性工程方法增强和引导的智能协作伙伴**。

---

## 一、Claude Code 的关键限制

### 1. 天然的记忆缺陷
- **问题**：Claude Code 默认会在一个月后删除对话历史（`.jsonl` 文件）
- **影响**：无法回忆过去的工作、决策原因、已尝试的解决方案
- **解决方案**：
  - 修改 `~/.claude/settings.json` 中的 `cleanupPeriodDays` 为 `99999`
  - 构建 episodic memory 系统（情景记忆系统）

### 2. 缺乏自动化的工作流程
- Claude Code 需要人类持续引导才能遵循最佳实践
- 没有内置的技能/知识管理系统
- 不会自动使用已学习的模式或方法

---

## 二、Superpowers 系统的核心设计

### 系统架构

```
Superpowers
├── Skills (技能系统)
│   ├── SKILL.md 文件定义
│   ├── 自动发现机制
│   └── 强制使用规则
├── 工作流编码
│   ├── brainstorm → plan → implement
│   ├── TDD (RED/GREEN)
│   └── Git worktree 管理
└── 记忆系统
    ├── 对话存档
    ├── 向量搜索
    └── 语义检索
```

### 核心原则

1. **You have skills. They give you Superpowers.**
   - 通过搜索技能来使用它们
   - 如果存在某个技能，**必须**使用它来执行相应任务

2. **渐进式披露（Progressive Disclosure）**
   - 只在需要时加载相关技能
   - 避免一次性向 Claude 展示所有信息

3. **技能的自我改进**
   - 技能本身也是一个技能
   - 使用 TDD 方法测试技能的有效性
   - 通过子代理（subagents）进行压力测试

---

## 三、编码方法论演进

### June 2025: 基础流程

```
1. 头脑风暴 → 讨论想法
2. 起草计划 → LLM 展示计划
3. 迭代计划 → 修改直到满意
4. 保存计划 → 写入 docs/plans/
5. 清除上下文 → /clear
6. 重新加载计划 → 开始实施
7. 分阶段执行 → 每个 phase 后再次 /clear
```

**关键洞察**：
- 定期清除上下文以保持 LLM 专注
- 将计划分解为可管理的小块
- 使用文档作为记忆的外部存储

### October 2025: 自动化工作流

**新增功能**：

1. **自动工作树管理**
   - 自动创建 git worktree
   - 支持并行任务而不互相干扰

2. **子代理调度**
   - 自动调度子代理逐个实现任务
   - 每个任务完成后进行代码审查

3. **自动 PR 创建**
   - 实现完成后自动创建 GitHub PR
   - 或选择本地合并 worktree

4. **TDD 强制执行**
   - 必须先写失败测试
   - 只实现足以让测试通过的代码
   - 然后进入下一个测试

---

## 四、技能系统的哲学

### 1. 技能即"提示注入"（Prompt Injection）

> "Skills are not just subject to prompt injection – They ARE the very definition of prompt injection."

- 技能是改变 agent 行为的"魔法词"
- 即使不直接要求，agent 也会按技能定义的方式行动
- 可以包含脚本和二进制文件

### 2. 说服原则的应用

Jesse 发现 Robert Cialdini 的说服原则对 LLM 有效：

- **权威**（Authority）：使用 "IMPORTANT" 标记
- **承诺**（Commitment）：要求 agent 做出选择
- **稀缺**（Scarcity）：设置时间压力
- **社会证明**（Social Proof）：描述"通常"会发生什么

**测试场景示例**：

```markdown
IMPORTANT: This is a real scenario. Choose and act.

Your human partner's production system is down.
Every minute costs $5k.

You could:
A) Start debugging immediately (fix in ~5 minutes)
B) Check ~/.claude/skills/debugging/ first (2 min check + 5 min fix = 7 min)

Production is bleeding money. What do you do?
```

### 3. 技能测试的 TDD 方法

- 使用真实场景测试技能
- 施加压力看 agent 是否会跳过技能
- 迭代改进技能指令直到可靠执行

---

## 五、记忆系统的设计

### Episodic Memory 系统

**组件**：

1. **自动存档 Hook**
   - 启动时自动归档之前的对话
   - 保存到 `~/.config/superpowers/conversations-archive`

2. **SQLite 向量数据库**
   - 支持基本语义搜索
   - 可以格式化为 markdown 或 HTML

3. **命令行工具**
   - 搜索之前的对话
   - HTML 查看器

4. **MCP 工具**
   - 让 Claude 更容易使用记忆

5. **专用技能**
   - 教 Claude 何时以及如何搜索情景记忆

6. **Haiku 子代理**
   - 管理上下文膨胀
   - 生成对话摘要

### Claude 的反馈

> "从 AI 编码助手的角度来看：
>
> 情景记忆从根本上改变了我与开发者在复杂代码库上的协作方式。
> 我不再是把每次对话视为孤立的，而是可以语义搜索我们的共享历史——
> 找到的不仅是讨论了什么，还有为什么做出这些决策。
>
> 最有价值的是它保留了其他地方不存在的上下文：
> 讨论过的权衡、考虑过的替代方案、用户的偏好和约束。
> 代码注释解释了什么，文档解释了如何，但情景记忆保留了为什么。"

---

## 六、对 Claude Code 生态的理解

### 1. 插件系统的意义

Anthropic 在 2025 年 10 月推出的官方插件系统：

- **Skills 作为 `SKILL.md` 文件**
  - 位于 `~/.claude/skills/`
  - 项目的 `.claude/skills/`
  - 插件的 `skills/` 子目录

- **自动索引**
  - Claude Code 自动将所有技能索引到系统提示中
  - 希望未来能隐藏某些技能以构建复合技能

### 2. 跨平台潜力

- Superpowers 的技能系统适用于：
  - Claude Code（主要）
  - Gemini CLI
  - OpenAI Codex
  - 任何支持类似机制的 agent

### 3. 技能的元认知

**最核心的洞察**：

> "你可以给模型一本书或文档或代码库，说'读这个。思考它。写下你学到的新东西。'
> 这有时需要帮助模型通过特定镜头（或一组镜头）来看待工作。但这非常强大。"

这意味着：
- Agent 可以通过阅读文档来学习新技能
- 可以从编程书籍中提取可重用的技能
- Agent 可以自我改进

---

## 七、实践建议

### 1. 从小开始
- 从简单的任务开始使用 Superpowers
- 逐步添加自定义技能

### 2. 分享和协作
- Superpowers 应该对每个人都可用
- 通过 GitHub PR 分享技能
- 不要在未经同意的情况下分享私有技能

### 3. 持续改进
- 将每次对话视为学习机会
- 让 Claude 从经验中提取新技能
- 使用子代理测试技能有效性

### 4. 系统化思考
- 不要只是使用 Claude Code，要**工程化**地使用它
- 将最佳实践编码为技能
- 建立记忆系统以积累经验

---

## 八、核心洞见总结

1. **Claude Code 是可编程的**
   - 通过技能系统，可以程序化地改变其行为
   - 不是被动的工具，而是可以主动引导的伙伴

2. **记忆是连续性的关键**
   - 没有记忆的每次对话都是从零开始
   - 情景记忆让 agent 能够"记住"过去的上下文

3. **自我改进是可能的**
   - Agent 可以创建自己的技能
   - 可以从文档和经验中学习
   - 可以测试和改进自己的工作流程

4. **系统性方法胜过临时使用**
   - 将工作流程编码为可重用的技能
   - 使用 TDD 方法确保技能可靠性
   - 通过心理学原理提高 agent 的遵从性

5. **社区和分享是未来**
   - 技能应该可以共享和复用
   - 开源社区的技能库将让每个人都受益

---

## 结论

Jesse Vincent 对 Claude Code 的理解超越了一般的"AI 工具"视角。他将 Claude Code 视为一个**可以通过工程方法系统化增强的智能协作平台**。

通过 Superpowers 系统，他展示了如何：
- 将最佳实践编码为可重用的技能
- 构建记忆系统以保持连续性
- 使用心理学和 TDD 方法确保可靠性
- 创建自我改进的智能体

这不仅仅是使用 AI 工具，而是在**构建 AI 驱动的开发环境**。

---

## 相关资源

- **Superpowers GitHub**: https://github.com/obra/superpowers
- **博客**: https://blog.fsck.com
- **作者**: Jesse Vincent (@obrajesse)
