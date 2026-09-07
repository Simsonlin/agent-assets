# 首轮试用后的资产建议

这些是 Agent 建议，尚未构成用户纳入、暂缓或淘汰决定。

| 资产 | 实际证据 | 建议 |
|---|---|---|
| matt/codebase-design | [一次 Codex 原生只读试用](20260907-design-codex/observations.md)，方法使用可见；未运行复现或对照 | 保留原版，继续 testing；下次在真实设计改动中观察接口表达和验证建议能否带来帮助，暂不为此特化 |
| structured/key-assumptions-check | [准备与撤销通过，DSH 按用户要求跳过](20260907-research-dsh/observations.md) | 保留候选；宿主恢复后新建试用，不能把环境受阻当成方法有效或无效 |
| 其他 Matt / structured Skill | 固定来源、完整性和所选路线依赖检查；没有本轮行为证据 | 保持 staged，按任务选择后试用，不因同源资产可用就整套纳入 |
| 个人 Skill、Adaptive SDD | 接入统一登记，既有个人使用；没有本轮新增效果评价 | 保持 testing，未来结合实际使用补轻量记录 |
| 本仓库工作流与资产工具 | 14 项文件系统测试及两次真实项目准备/清理 | 用于后续迭代；仍不替用户作正式纳入决定 |

本轮没有足够依据将两套外部方法合并，也没有必要为两个试点创建专属能力层。先积累不同任务的试用记录；只有出现重复的场景差异，再考虑新建领域特化资产，并引用原版版本和触发差异的证据。

用户选定具体资产与状态后，按 [纳入流程](../workflows/adoption.md) 记录真实表述及证据，再运行 decide。正式视图通过 `python3 scripts/assets.py list --state adopted` 查询。
