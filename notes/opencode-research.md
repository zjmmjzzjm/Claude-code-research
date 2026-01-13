# OpenCode & Oh My OpenCode 研究报告

本报告对 OpenCode 生态系统中的两个核心项目进行深入分析：`OpenCode` (核心工具) 和 `Oh My OpenCode` (增强框架)。这两个项目共同构成了一个强大的、开源的 AI 编程助手解决方案，是 Claude Code 的有力竞争者。

## 1. OpenCode (The Core)

**仓库**: [https://github.com/anomalyco/opencode](https://github.com/anomalyco/opencode)
**官网**: [https://opencode.ai](https://opencode.ai)

### 核心定位
OpenCode 是一个开源的 AI 编程 Agent，旨在提供类似于 Claude Code 的体验，但具有以下关键差异化优势：
*   **100% 开源**: 完全透明，社区驱动。
*   **模型中立 (Provider Agnostic)**: 不绑定特定厂商。支持 Claude (Anthropic), OpenAI, Google Gemini，甚至本地模型。
*   **内置 LSP 支持**: 开箱即用的语言服务器协议支持，赋予 Agent 代码补全、跳转定义、查找引用等 IDE 级能力。
*   **TUI 优先**: 专为终端用户设计，由 Neovim 和 terminal.shop 的创作者打造，追求极致的终端体验。
*   **Client/Server 架构**: 允许远程控制（例如通过移动端 App 控制运行在电脑上的 Agent）。

### 架构分析
基于 Monorepo (TurboRepo) 结构，包含多个核心包：
*   **packages/opencode**: 核心 CLI 工具。
*   **packages/desktop**: 桌面端应用封装。
*   **packages/console**: 可能涉及云端控制台或管理界面。
*   **packages/plugin**: 插件系统定义。

### 核心功能
*   **多 Agent 模式**:
    *   `build`: 默认 Agent，全权限，用于开发。
    *   `plan`: 只读 Agent，用于分析和规划，默认禁止文件编辑。
*   **LSP 集成**: 让 AI 能像人类开发者一样使用 IDE 功能，极大提高了代码理解和修改的准确性。
*   **跨平台**: 支持 macOS, Windows, Linux。

---

## 2. Oh My OpenCode (The Framework)

**仓库**: [https://github.com/code-yeongyu/oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode)

### 核心定位
如果说 OpenCode 是 `zsh`，那么 Oh My OpenCode 就是 `oh-my-zsh`。它是一个**Batteries-Included**（开箱即用）的配置框架和插件集，旨在将 OpenCode 的能力推向极限。

### 核心理念：Sisyphus (西西弗斯)
引入了一个名为 **Sisyphus** 的主 Agent（默认基于 Claude Opus 4.5），作为用户的“AI 技术主管”。Sisyphus 不直接干所有的活，而是负责**编排**和**分派**任务给专门的子 Agent：
*   **Oracle** (GPT-5.2): 负责架构设计、调试策略（利用其强大的推理能力）。
*   **Librarian** (GLM-4.7): 负责查阅文档、分析多仓库代码（利用其长上下文和搜索能力）。
*   **Frontend UI/UX** (Gemini 3 Pro): 负责前端界面开发（利用其多模态和生成能力）。
*   **Explore** (Grok/Gemini): 快速代码库探索。

### 关键特性 ("Ultrawork")
*   **Ultrawork 模式**: 通过关键词 `ultrawork` (或 `ulw`) 触发。Agent 会自动分析任务，并行启动后台子 Agent 进行调研、规划，然后持续执行直到完成。
*   **Claude Code 兼容层**: 兼容 Claude Code 的配置、MCP、Hooks 等，方便迁移。
*   **增强工具集**:
    *   **AST-Grep**: 基于 AST 的代码搜索和替换，比正则更精准。
    *   **增强 LSP**: 提供悬停文档、跳转定义等。
    *   **MCP 集成**: 内置 Exa (联网搜索), Context7 (文档), Grep.app (GitHub 代码搜索)。
*   **自我修正机制**:
    *   **Todo Continuation Enforcer**: 强制 Agent 完成所有 TODO，防止半途而废。
    *   **Comment Checker**: 防止 AI 写过多无用的注释。
    *   **Think Mode**: 自动检测复杂任务并开启深度思考模式。

### 为什么强大？
Oh My OpenCode 的核心价值在于**分工明确的模型编排**。它承认不同模型有不同的长处（Claude 适合写代码和编排，GPT 适合逻辑推理，Gemini 适合长文本和前端），并将它们有机结合。这比单一模型的 Agent 更高效、更强大。

---

## 3. 总结与启示

### 对比 Claude Code
*   **OpenCode** 提供了开源的底层引擎和更强的 IDE 集成 (LSP)。
*   **Oh My OpenCode** 展示了如何通过**多模型协作 (Multi-Model Orchestration)** 和 **精细化工具链** 来构建下一代 AI 编程体验。

### 进化方向
对于我们在研究的 `Claude-code-research` 项目，可以借鉴以下几点：
1.  **引入 LSP 能力**: 目前大多数 Agent 还是基于文本读写，引入 LSP 能显著提升修改准确率。
2.  **多模型分工**: 不应只依赖单一模型，应建立“专家团队”模式（架构师、前端、文档员）。
3.  **自动化闭环**: 像 Sisyphus 一样，建立“任务 -> 拆解 -> 并行调研 -> 执行 -> 验证”的全自动工作流。
4.  **配置框架化**: 像 `oh-my-opencode` 一样，提供一套开箱即用的最佳实践配置，降低用户门槛。
