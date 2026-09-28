# Agent Assets

个人 Agent 能力资产库：保存固定来源，按项目选择并启用需要的 Skill。当前支持 Codex 和 DeepSeek Harness。

## 从哪里开始

- **让 Agent 操作**：给它本仓库路径或可访问的仓库地址，让它从 [AGENTS.md](AGENTS.md) 开始，并说明要接入的来源或目标项目需要的 Skill。
- **查看当前方式**：[项目启用流程](workflows/project-skills.md) · [资产登记](docs/catalog.md)。
- **查看资产**：[登记说明](docs/catalog.md) · [catalog.json](catalog.json)；`python3 scripts/assets.py list` 可按状态和领域过滤。
- **给项目启用 Skill**：[项目启用流程](workflows/project-skills.md)；工具命令见 [scripts/README.md](scripts/README.md)。

## 可以直接交给 Agent 的请求

> 阅读这个 agent-assets 仓库的 AGENTS.md。从我提供的外部仓库接入指定 Skill，固定版本并完成依赖检查，放到暂存区。

> 阅读这个 agent-assets 仓库的 AGENTS.md。为当前项目启用 `matt/implement` 及必需依赖，先预览再复制完整目录；列出来源版本、安装名称和目标路径。不要覆盖项目中已有的不同内容。

> 列出这个项目已启用的技能和来源；若要更换技能，先比较项目副本与新来源，不静默覆盖。

## 现有资产与维护入口

| 内容 | 位置 | 当前定位 |
|---|---|---|
| Matt 固定副本，17 个 Skill | [Matt 选集](staging/matt/README.md) | 按项目选用，源文件保持原版 |
| 4 个个人 Skill | [个人 Skill](docs/catalog.md#个人资产) | 已有使用，成熟度分别记录 |
| Adaptive SDD | [标准与模板](adaptive-sdd-standard/README.md) | 独立标准资产 |
| latticework 固定副本，4 个 Skill | [latticework 选集](staging/latticework/README.md) | 问题定义、策略与表达，按项目选用 |
| 新外部候选 | [暂存区](staging/README.md) | 固定来源、完整资源、按需选用 |
| 正式纳入视图 | [library](library/README.md) | 仅含用户决定纳入的资产 |
| 用途组合 | [profiles](profiles/README.md) | 资产选择，按需解析依赖 |

仓库中的源码不是全局安装目录。项目知识、启用副本和实际产物保留在项目中；资产库维护来源与可复用组合。资产正文按任务读取，不一次性加载所有 Skill。
