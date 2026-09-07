# Agent Assets

个人 Agent 能力资产库：保存和管理能力，试用外部来源，再依据实际体验逐步纳入。当前支持 Codex 和 DeepSeek Harness。

## 从哪里开始

- **让 Agent 操作**：给它本仓库路径或可访问的仓库地址，让它从 [AGENTS.md](AGENTS.md) 开始，并说明要接入、试用或采用的资产和任务。
- **查看方案与进度**：[v1 方案](docs/plans/personal-agent-capability-v1.md) · [实施记录](docs/IMPLEMENTATION.md)。
- **查看资产**：[登记说明](docs/catalog.md) · [catalog.json](catalog.json)；`python3 scripts/assets.py list` 可按状态和领域过滤。
- **开始一次试用**：[试用流程](workflows/trial.md)；工具命令见 [scripts/README.md](scripts/README.md)。

## 可以直接交给 Agent 的请求

> 阅读这个 agent-assets 仓库的 AGENTS.md。从我提供的外部仓库接入指定 Skill，固定版本并完成依赖检查，放到暂存区。

> 阅读这个 agent-assets 仓库的 AGENTS.md。用我指定的资产在当前项目测试这个任务：……。完成试用准备、按宿主方式调用、记录观察，结束后撤销本次试用配置。

> 根据这些试用记录，建议哪些资产保留原版、特化、正式纳入或暂缓。纳入决定由我作出。

## 现有资产与维护入口

| 内容 | 位置 | 当前定位 |
|---|---|---|
| Matt 固定副本，17 个 Skill | [Matt 暂存选集](staging/matt/README.md) | 独立试用，源文件保持原版 |
| 4 个个人 Skill | [个人 Skill](docs/catalog.md#个人资产) | 已有使用，成熟度分别记录 |
| Adaptive SDD | [标准与模板](adaptive-sdd-standard/README.md) | 独立标准资产 |
| latticework 固定副本，4 个 Skill | [latticework 选集](staging/latticework/README.md) | 问题定义、策略与表达，待试用 |
| 新外部候选 | [暂存区](staging/README.md) | 固定来源、完整资源、待试用 |
| 正式纳入视图 | [library](library/README.md) | 仅含用户决定纳入的资产 |
| 用途组合 | [profiles](profiles/README.md) | 资产选择，按需解析依赖 |
| 试用证据 | [trials](trials/README.md) | 记录效果与环境限制 |

仓库中的源码不是全局安装目录。项目知识和实际产物保留在项目中；资产库维护方法、来源、试用经验和采用决定。资产正文按任务读取，不一次性加载所有 Skill。
