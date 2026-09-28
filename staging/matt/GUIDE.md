# Matt skills 选择与使用指南

项目选用以 [项目启用流程](../../workflows/project-skills.md) 为准，资产登记 ID 为 `matt/<name>`。下文的技能名称用于理解 Matt 方法；项目安装后使用 `<source>-<name>` 名称。

本指南面向本地固定副本。原始行为以 [SOURCE.md](SOURCE.md) 指向的版本为准；本地建议会明确标注。

## 1. 如何选择并启用

### 选择副本与作用范围

安装源是本目录 `upstream/skills/engineering/<name>/` 和 `upstream/skills/productivity/<name>/` 下的完整 skill 文件夹。清单见 [README](README.md)。不要用跟随远端最新版本的安装命令替换这份固定副本。

Codex 的项目级位置是目标产品仓库 `.agents/skills/<name>/`，用户级位置是 `~/.agents/skills/<name>/`。同名 skill 不会自动合并；保留 `agents/openai.yaml` 中的调用策略。可使用 skill 选择器或 `$skill-name` 显式调用。依据：[OpenAI 官方文档](https://learn.chatgpt.com/docs/build-skills)，核对日期 2026-09-06。

**本地建议：按项目需要选择。** `enable` 复制选定的完整目录和登记的必需依赖。上游支持文件夹内的脚本属于 Skill 资源，复制不等于执行；setup 只在项目需要配置时调用。

### 先处理同名版本

现有个人 `grilling` 与本副本有明确差异：前者一次一问，当前 Matt 版按相互独立的问题分轮。项目如果选择 Matt 版本，使用带来源前缀的安装名。

安装前检查项目级、用户级已有条目，比较来源。不要覆盖不明来源的文件，也不要依靠两个同名版本的隐含优先级。工具使用来源前缀；保留个人源码，记录项目最终选择的版本。

其他 Agent 使用它们各自的安装位置和显式调用方式。上游 `/implement` 等表示技能入口，不代表所有宿主都有相同命令；`/clear`、`/compact` 也不是此副本提供的 skill。

例如，项目需要 `implement` 时，先预览：

```sh
python3 scripts/assets.py enable --project /absolute/project --harness codex --asset matt/implement
```

核对四项依赖闭包后加 `--apply`。安装副本可由项目 Git 跟踪。目录存在不代表模型已实际调用技能；上游要求显式调用的入口仍需按其策略使用。

## 2. 在一个真实项目中开始

项目尚未配置 Matt 所需 tracker 和领域文档时，可按需调用：

```text
$matt-setup-matt-pocock-skills
为当前项目配置 Matt 工程技能。请检查已有项目约定；
优先考虑项目已有的 tracker，向我展示配置后再写入。
```

本地 tracker 是一种选择，上游也支持 GitHub、GitLab 等。已有项目 tracker 合适时可直接使用。setup 配置 `docs/agents/` 和项目说明入口；领域词汇与 ADR 按实际需要产生，不需要先填满空目录。来源：[setup 原文](upstream/skills/engineering/setup-matt-pocock-skills/SKILL.md)。

不要先把整个旧项目迁移进一套新文档标准。已经存在的项目约束仍需遵守，但本集合不要求安装或调用本仓库另外两套自研资产。

## 3. 按今天的任务选择入口

这些箭头表示用户选择的阶段，不是自动执行流水线。

| 现在的情况 | 推荐路径 | 可观察的产物 |
|---|---|---|
| 有想法，范围还模糊 | `grill-with-docs` | 共同理解；有新术语时更新 glossary |
| 已想清楚，一次会话可完成 | 同一会话 `implement` | 可验证的行为变化 |
| 实现需要多次会话 | `to-spec → to-tickets → 每次 implement 一个 ticket` | 一份规格、独立 ticket、实现与验证 |
| 外部事实不清楚 | `research`，再回原讨论 | 一份有引用的研究记录 |
| 需要看见或跑起来才知道 | `prototype`，带结论回原讨论 | 能回答问题的原型和观察 |
| bug 原因不清楚 | 按需安装并调用 `diagnosing-bugs` | 可重复反馈、诊断与回归验证 |
| 连关键决策都跨多次讨论 | 按需安装并调用 `wayfinder` | 决策地图；清晰后再进入 spec |
| 想检查架构改善机会 | 按需安装并调用 `improve-codebase-architecture` | 候选报告，选定后再讨论实现 |

来源：[路由](upstream/skills/engineering/ask-matt/SKILL.md)、[实现说明](upstream/docs/engineering/implement.md)。不知道选什么时使用 `$matt-ask-matt`，并说明只考虑 [已保存清单](README.md) 中且实际已安装的技能。

### 澄清一个需求

```text
$matt-grill-with-docs
我想让……，现在的问题是……。
先与我澄清范围、取舍和如何判断结果。请实际加载 grilling 和 domain-modeling。
```

原版 `grilling` 每轮可以问多个没有未决依赖的问题。先体验这个节奏；如果负担太大，可以追加“本次改成一次一问”，并把它记为本次调用偏好，而不是立即改 skill。

`CONTEXT.md` 是术语表，不保存全部需求。多数普通决定仍在对话中；重要取舍只有满足条件才进入 ADR。不要因为没有新增文件就认定 skill 失败，也不要因为有 glossary 就认为决策全部保存。来源：[domain-modeling](upstream/skills/engineering/domain-modeling/SKILL.md)。

### 单会话的小改动

```text
$matt-implement
实现当前对话里已经确认的方案。目标与验收条件是……；测试观察接口是……。
```

原版会在当前分支提交。调用前明确所处分支与本次提交意图；如果你希望先人工检查再提交，在本次请求明确写“先保留改动供我检查，本次不提交”。这属于本地调用覆盖，应记录，不能把它当作原版默认。

### 跨会话的功能

先在原讨论中调用 `$matt-to-spec`。它综合已经确定的内容，不重新访谈需求，但仍要确认 seam：从哪个公开接口观察行为。仔细核对具体数字、负面要求、边界条件和 out-of-scope 是否保留。接着调用 `$matt-to-tickets`，确认每张 ticket 可验证、依赖准确、粒度适合一个新会话。

进入新会话时使用完整 ticket 路径或完整 issue URL：

```text
$matt-implement
实现这张 ticket：<完整路径或 URL>。
开始前读取全文及引用的规格，复述 ticket 标题、目标、验收条件和测试 seam。
```

不要只传“#2”。首次建议按依赖顺序完成，避免把多张 ticket 同时派到共享 checkout。宽范围机械重构是上游允许的切片例外，按 expand–contract 处理；不强行按数据库/API/UI 水平拆分。来源：[to-tickets](upstream/skills/engineering/to-tickets/SKILL.md)。

### 查事实或做原型

```text
$matt-research
请确认……是否支持……。优先查官方文档和源码，保存有引用的结论及未知项。
```

```text
$matt-prototype
这次只回答一个问题：……。
我希望通过……动作观察……，再决定正式实现方案。
```

原版 prototype 有逻辑演示与 UI 变体两条路径。若问题是 Penpot 插件真实 API 行为，应在调用中明确要求最小真实运行实验，说明这改变了原版默认载体；浏览器演示不能证明插件内表现。原版还包含原型分支保存等动作，使用前读 [prototype 原文](upstream/skills/engineering/prototype/SKILL.md)。

### 难 bug

```text
$matt-diagnosing-bugs
预期行为是……，实际行为是……，可用复现样例/入口是……。
先建立能反映这次问题的反馈路径，再定位原因。
```

这个入口要求真实反馈和分阶段诊断，可能需要你参与。不要把无法运行的外部环境替换成没有等价性的 mock 后宣称问题已验证。来源：[诊断原文](upstream/skills/engineering/diagnosing-bugs/SKILL.md)。

## 4. 阶段交接和完成判断

澄清 → spec → tickets 尽量留在同一对话，减少决定在摘要中丢失。若必须换环境、目录或交给另一人，调用 `$matt-handoff`，说明下一会话的目的；它引用现有规格、ticket 和 diff，而不是复制一套。原版将交接文件写入系统临时目录，后续会话使用前确认文件仍可访问。来源：[handoff](upstream/skills/productivity/handoff/SKILL.md)、[阶段边界](upstream/skills/engineering/ask-matt/PHASE-BOUNDARIES.md)。

每张 ticket 收尾时，本地建议核对三件事：实际验收结果、review 发现的处理结果、ticket 状态及后续依赖。没有实际执行的人工验收单独记录责任方与下一步。原版 `implement` 不提供完整的 ticket 收尾闭环，不能以它已经 commit 代替这一步。

## 5. 这个版本需要知道的问题

以下为固定版本的已知行为或上游文档报告，不代表我们已在你的项目复现。

| 问题 | 项目使用时如何处理 | 来源 |
|---|---|---|
| `implement` 先 review 再 commit，但 review 默认只看 `<fixed-point>...HEAD` | 明确被审查的 diff 是否包含本次改动；可以先在已授权任务分支提交，再对明确基点调用 review；若坚持提交前审查，则在调用中明确覆盖未提交与新增文件，记录这一偏离 | [实现说明](upstream/docs/engineering/implement.md)、[审查原文](upstream/skills/engineering/code-review/SKILL.md) |
| review 不自动修复发现，implement 不自动关闭 ticket | 显式要求处理本次有效发现；验收后再更新 ticket 状态 | [实现说明](upstream/docs/engineering/implement.md) |
| `grill-with-docs` 的依赖可能未真正加载 | 检查读取了两个依赖；有新术语时检查 glossary 是否更新 | [澄清说明](upstream/docs/engineering/grill-with-docs.md) |
| 普通决定没有自动持久化 | 在原对话生成 spec，人工核对关键约束；需要交接时保留指针 | [澄清说明](upstream/docs/engineering/grill-with-docs.md) |
| spec 得到 `ready-for-agent` 标签 | 标签不等于批准整个父规格自动执行；若有自动领取机制，明确只领取实现 ticket | [规格说明](upstream/docs/engineering/to-spec.md) |
| 上游源码与讲解可能不同步 | 本快照 `tdd/SKILL.md` 明确使用 red → green，把 refactoring 放在 review 阶段；不要仅按旧教程推测步骤 | [TDD 原文](upstream/skills/engineering/tdd/SKILL.md) |

原版双轴审查是 Standards 与 Spec 两个独立子任务，不等于自研 `spec-execution` 的单一综合审查或 Assurance 复审。宿主无法调用依赖或子代理时记录具体限制，不把另一套执行器悄悄接进来。

## 6. 调整与更新

先用项目调用说明表达项目偏好；确需修改通用 Skill 时，记录相对固定来源的差异与理由，见 [LOCAL-CHANGES.md](LOCAL-CHANGES.md)。上游更新按 [SOURCE.md](SOURCE.md) 操作，项目副本由项目单独比较和更新。
