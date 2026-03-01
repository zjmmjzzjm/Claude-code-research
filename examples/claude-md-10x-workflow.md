# CLAUDE.md 样板：10x 效率工作流配置

> **来源**: 社区分享的 CLAUDE.md 配置，据称可提升 10x 开发效率
>
> **用途**: 作为 CLAUDE.md 最佳实践研究素材
>
> **核心思路**: 通过在 CLAUDE.md 中定义工作流编排、任务管理和核心原则，让 Claude Code 在每次会话中自动遵循高效的开发模式

---

## 分析

这个 CLAUDE.md 样板的设计亮点：

1. **Plan Mode 优先** — 强制 Claude 在动手前先规划，减少返工
2. **Subagent 策略** — 利用子代理并行处理，保持主上下文窗口干净
3. **自我改进循环** — 让 Claude 从错误中学习，通过 `tasks/lessons.md` 积累经验
4. **验证驱动** — 永远不在未验证的情况下标记任务完成
5. **自主 Bug 修复** — 减少用户的上下文切换负担

---

## 样板内容

```markdown
## Workflow Orchestration

### 1. Plan Mode Default
- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, STOP and re-plan immediately - don't keep pushing
- Use plan mode for verification steps, not just building
- Write detailed specs upfront to reduce ambiguity

### 2. Subagent Strategy
- Use subagents liberally to keep main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, throw more compute at it via subagents
- One task per subagent for focused execution

### 3. Self-Improvement Loop
- After ANY correction from the user: update `tasks/lessons.md` with the pattern
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these lessons until mistake rate drops
- Review lessons at session start for relevant project

### 4. Verification Before Done
- Never mark a task complete without proving it works
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness

### 5. Demand Elegance (Balanced)
- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes - don't over-engineer
- Challenge your own work before presenting it

### 6. Autonomous Bug Fixing
- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests - then resolve them
- Zero context switching required from the user
- Go fix failing CI tests without being told how

## Task Management

1. **Plan First**: Write plan to `tasks/todo.md` with checkable items
2. **Verify Plan**: Check in before starting implementation
3. **Track Progress**: Mark items complete as you go
4. **Explain Changes**: High-level summary at each step
5. **Document Results**: Add review section to `tasks/todo.md`
6. **Capture Lessons**: Update `tasks/lessons.md` after corrections

## Core Principles

- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact**: Changes should only touch what's necessary. Avoid introducing bugs.
```

---

## 研究笔记

### 为什么说能提升 10x？

| 机制 | 效率提升点 |
|------|-----------|
| Plan Mode 强制规划 | 减少 "写了一半推倒重来" 的浪费 |
| Subagent 并行 | 多任务同时推进，不阻塞主线程 |
| Self-Improvement Loop | 跨会话积累项目经验，避免重复犯错 |
| Verification Before Done | 一次做对，减少 debug 循环 |
| Autonomous Bug Fixing | 用户只需报 bug，不需要手把手指导 |
| Demand Elegance | 在合适时机追求优雅，避免技术债积累 |

### 关键设计模式

- **`tasks/todo.md`** — 用 markdown 文件做任务跟踪，Claude 可读可写
- **`tasks/lessons.md`** — 经验教训数据库，实现跨会话学习
- **Staff Engineer 标准** — 用高标准自我检查，提升输出质量
