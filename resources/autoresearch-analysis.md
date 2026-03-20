# autoresearch 插件分析

> 仓库地址：https://github.com/uditgoenka/autoresearch
> 版本：v1.7.5 | 许可证：MIT

## 项目定位

autoresearch 是一个 **Claude Code 插件**，灵感来自 Andrej Karpathy 的 autoresearch 方法论。它将 Claude Code 变成一个**无人值守的自主迭代改进引擎**，核心公式为：

> **约束 + 可量化指标 + 自主迭代 = 复利式收益**

你设定目标和度量标准，Claude 自动循环执行「修改 → git commit → 验证 → 指标改善则保留 / 否则 git revert → 继续下一轮」的流程，直到达成目标或手动停止。

## 技术栈

**不含传统代码**——全部是 Markdown 文件，本质是一套精心设计的 Prompt Engineering 框架，以 Claude Code Plugin（Skill + Command 体系）形式分发。依赖 Git 作为"记忆系统"，用 TSV 文件记录实验日志。

## 核心命令（8 个）

| 命令 | 功能 |
|------|------|
| `/autoresearch` | 无限自主迭代循环（主命令） |
| `/autoresearch:plan` | 交互式设置向导（目标 → 指标 → 验证方式） |
| `/autoresearch:fix` | 迭代修错，直到零失败 |
| `/autoresearch:debug` | 科学化 Bug 追踪，7 种调查技术 |
| `/autoresearch:security` | 只读安全审计（STRIDE + OWASP 框架） |
| `/autoresearch:ship` | 通用交付工作流，覆盖 9 个领域 |
| `/autoresearch:scenario` | 12 维边缘场景探索 |
| `/autoresearch:predict` | 多角色专家分析（模拟多个专家视角） |

## 核心循环协议（8 个阶段）

每次迭代严格遵循：

1. **Review** — 审查当前状态 + git 历史
2. **Ideate** — 基于已有学习选择下一步修改
3. **Modify** — 做**一个**原子级改动
4. **Commit** — git 提交（验证前）
5. **Verify** — 运行机械化验证（测试/基准测试）
6. **Guard** — 可选的回归保护检查
7. **Decide** — 指标改善则保留，否则 `git revert` 回滚
8. **Log** — 记录结果到 TSV 文件，然后重复

## 应用场景

### 代码类

- **测试覆盖率提升**：设定目标 90%，Claude 自动写测试、跑测试、保留有效的、回滚无效的
- **性能优化**：盯着 p95 延迟 / QPS / 内存占用，自动尝试各种优化手段
- **减小包体积**：以 bundle size (KB) 为指标，自动 tree-shake、拆包、替换依赖
- **Lint 清零**：500 个 lint error → 0，每次修一个，失败就回滚
- **修 CI**：测试红了，自动循环修到全绿

### 非代码类

- **文案打磨**：以可读性评分为指标，反复改进营销文案/文档
- **配置调优**：数据库参数、模型超参数等，以基准测试结果为指标自动搜索

### 最佳适用条件

1. **有机械化验证手段**（能跑脚本得到一个数字）
2. **改进空间大**（需要几十上百次小迭代）
3. **你不想盯着**（睡前启动，醒来收结果）

不适合的场景：需要主观判断的（UI 美不美）、一步就能搞定的、没有量化指标的。

## 仓库结构

```
autoresearch/
├── README.md                          # 主文档
├── guide/                             # 详细使用文档（13 个 .md 文件）
│   ├── getting-started.md
│   ├── autoresearch.md / plan / debug / fix / security / ship / scenario / predict
│   ├── chains-and-combinations.md
│   ├── examples-by-domain.md
│   └── advanced-patterns.md
├── claude-plugin/                     # 可安装的插件包
│   ├── commands/autoresearch/         # 7 个子命令 .md
│   └── skills/autoresearch/           # 核心技能定义
│       ├── SKILL.md                   # 主技能文件
│       └── references/               # 协议文档（10 个 .md）
├── .claude-plugin/                    # 市场清单
├── .claude/                           # 插件元数据
└── scripts/                           # 工具脚本
```

## 关键设计原则

- **机械化验证**：只信任可量化指标（测试通过数、覆盖率%、延迟 ms），拒绝主观判断
- **原子化修改**：每次迭代只做一个修改，确保可追踪、可回滚
- **Git 即记忆**：所有实验都通过 git 提交，失败自动 revert（保留历史）
- **崩溃恢复**：连续 5 次失败后自动切换策略（组合成功方案、尝试相反方向、激进架构变更）
- **Guard 机制**：可选的安全阀，确保优化某个指标时不会导致其他方面退化
