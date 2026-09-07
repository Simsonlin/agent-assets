# v1 实施记录

方案：[Personal Agent Capability Architecture v1](plans/personal-agent-capability-v1.md)。更新：2026-09-07。

| 阶段 | 当前状态 | 证据 |
|---|---|---|
| 1：组织与入口 | 完成 | README / AGENTS 导航、34 项资产、3 个来源、4 个通用用途 Profile；来源、领域和成熟状态分别登记 |
| 2：可撤销试用 | 完成 | 标准库工具完成接入、预览、准备、核对、记录、清理和用户决定登记；14 项本地测试通过 |
| 3：真实试用 | Codex 完成一次；DSH 按用户要求跳过实际运行 | [Codex 观察](../trials/20260907-design-codex/observations.md) · [DSH 状态](../trials/20260907-research-dsh/observations.md) |
| 4：纳入演练 | 流程与建议已交付；正式纳入待用户决定 | [本轮建议](../trials/recommendations-2026-09-07.md)；未自动产生 adopted 资产 |

## 已交付

- 既有 17 个 Matt Skill 已统一迁入 staging/matt；4 个个人 Skill 和 Adaptive SDD 保持原位置，以 catalog 统一登记。未为试点项目改写通用方法。
- 在 staging 固定接入 structured-analytic-skills 的 8 个完整 Skill，保留 MIT 许可、第三方说明、支持资源与摘要。已审查所选路线依赖，可选后续路线见来源 GUIDE。
- 提供接入/试用/纳入三个 Agent 流程，Codex/DSH 两套适配，工程和研究四个 Profile，以及轻量观察模板。
- prepare 默认预览；试用使用独立名称和完整目录，记录每次来源/安装摘要与文本转换；cleanup 保护用户修改、额外文件、已有配置和路径边界。
- record 区分准备、原生发现、实际调用与效果；decide 需要用户真实决定记录。正式库允许暂时为空。

## 实际试用与撤销

**Codex：** 通过用户已授权的限定范围只读任务，确认原生发现、明确调用及精确正文读取，产生两项有源码依据的模块接口观察。结果记为 limited：没有运行构建复现或无 Skill 对照，不能据此认定稳定增益。原始完整事件流未纳入仓库，只保留简短报告和必要执行证据。

**DSH：** 完成研究项目临时副本准备、摘要核对和撤销。用户表示 DSH 无法启动并要求先跳过；没有发送研究材料或执行模型试用。结果记为 blocked，不用于评价资产质量；原生发现、调用及研究效果均未验证。

两个 run 的 cleanup 均为 cleaned，protected 为空。恢复 DSH 或开展下一轮时应创建新 run；已撤销的临时调用名与路径仅保留作历史证据。项目源码、正式研究文档和个人用户级技能目录没有被修改。

## 验证

- `python3 scripts/assets.py check`：34 个资产、4 个 Profile、3 个来源通过。
- `python3 -m unittest discover -s tests -v`：14 项通过；覆盖预览无副作用、完整资源/策略保留、依赖闭包、同名隔离、DSH 安装位置、重复准备保护、修改后撤销保护、符号链接/清理路径保护、固定来源校验、接入同版本扩展与版本漂移拒绝、调用证据及用户决定登记。
- 仓库维护文档的本地链接检查通过；既有 Matt 上游快照摘要保持一致。
- `git diff --check` 通过。design-workflow 清理后 Git 状态干净；研究项目有既有或并行工作的未提交文档，保留原状，未把它们作为本次试用产物或清理对象。两处均无本次临时 Skill 残留。资产库变更留在工作区，未提交或推送。

## 环境基线与后续入口

- 仓库实际路径为 agent-assets，当前任务曾保留旧名 engineering-assets；未把本机绝对路径写进通用 Profile 或工具逻辑。
- Python 3.10.11。npm Codex 缺少平台二进制；桌面随附 CLI 0.153.4 可用。第一次模型请求遇到用量限制，恢复后经用户授权完成本次运行；未更换模型或使用额度重置。
- 本机 DSH 包版本 0.1.2-alpha.2，静态适配依据已核对；用户报告启动问题，本次不修复宿主。
- 下一次直接从 README 的自然语言请求开始。优先继续原版真实试用；有证据后再决定纳入或特化。DSH 恢复后补研究路线的真实调用，不需要重建资产结构。

## 暂存目录统一调整

按用户要求，原根目录 matt-skills 整体迁入 staging/matt，所有外部候选统一位于 staging/<source-id>。同步 catalog、README、Agent 导航、来源指南与方案，并为 structured 增加直接列出 8 项 Skill 的入口。

保留 upstream 作为“固定版本的作者原版副本”一层，与本地说明分开。Matt 69 个原版文件逐字节一致；资产 ID、来源版本、Profile 和生命周期不变。已结束的 .local 试用清单保留当时 source_path 作历史证据，当前路径以 catalog 为准。

latticework 仅作来源评估，未接入或安装，建议与限制见 [评估记录](latticework-assessment.md)。没有修改业务项目或全局技能配置。

本次验证：34 项资产登记通过；14 项测试通过；30 份本地维护文档链接无缺失；迁移后 Matt 准备预览解析到新路径且无安装副作用；原始 SHA256SUMS 的 69 项一致；git diff --check 通过。

## latticework 首批候选接入

用户同意将评估的四项加入待试用候选：scqa-pyramid、strategy-kernel、tosca-problem-definition、key-assumptions-check。从 `dbfdca4dd1a0d0348a390732591b2b6f0abf5d70` 接入 20 个完整原版文件，保留原始插件目录和 MIT 许可，单独登记来源及摘要；四项均为 staged。

理论参考与示例文件完整；未收录的可选相邻路线及子 Agent 环境要求见来源 GUIDE。原始 Skill 正文未修改，没有安装到项目或运行模型。现有 structured 同名资产保持独立；比较时使用不同 run。

当前登记共 38 项资产、4 个来源、4 个 Profile。后续试用和正式采用决定仍分别记录。

接入验证：38 项登记通过；20 个来源文件与固定 checkout 逐字节一致；四项 YAML 元数据解析通过；Codex/DSH 各四项准备预览通过且无安装副作用；必需资源和本地指南链接完整，10 项未收录相邻入口已在 GUIDE 标明；git diff --check 通过。
