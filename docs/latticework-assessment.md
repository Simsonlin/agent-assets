# latticework 候选来源评估

更新：用户同意接入后，四项已保存为 [latticework 暂存选集](../staging/latticework/README.md)，状态 staged；尚未安装或完成行为试用。以下保留来源比较和试用建议。检查版本：`dbfdca4dd1a0d0348a390732591b2b6f0abf5d70`。读取了四项 Skill 正文；从固定 checkout 接入四项完整目录，没有收录整个来源。

## 现有来源

当前 `staging/structured/upstream/` 的 8 个 Skill 全部来自 [radarist/structured-analytic-skills](https://github.com/radarist/structured-analytic-skills/tree/d503ff5b164a6bed567a9c48214fd0517cad64dd)，详见 [本地来源记录](../staging/structured/SOURCE.md)。l4ci/latticework 已作为独立来源登记，与 structured 分开。

upstream 表示固定版本的作者原版文件副本；本地管理文档位于它的上一层。它不是作者名、自动更新机制或成熟度级别。

## 补充价值与建议

以下是依据正文与当前选集用途作出的判断，尚未用真实任务验证效果。

| 候选 | 相对当前选集的补充价值 | 建议 |
|---|---|---|
| [scqa-pyramid](https://github.com/l4ci/skills/blob/dbfdca4dd1a0d0348a390732591b2b6f0abf5d70/plugins/latticework/skills/scqa-pyramid/SKILL.md) | 把已有发现组织为面向读者的结论、论据与报告结构；当前 8 项侧重问题拆分和证据判断，没有专门的表达路线 | 有真实研究汇报任务时优先试；不能以表达结构代替缺失证据 |
| [strategy-kernel](https://github.com/l4ci/skills/blob/dbfdca4dd1a0d0348a390732591b2b6f0abf5d70/plugins/latticework/skills/strategy-kernel/SKILL.md) | 围绕诊断、指导方针、连贯行动审查战略，补充“证据分析后如何形成取舍与行动”的用途 | 有具体战略障碍或现有策略文本时试，避免仅为套框架而使用 |
| [tosca-problem-definition](https://github.com/l4ci/skills/blob/dbfdca4dd1a0d0348a390732591b2b6f0abf5d70/plugins/latticework/skills/tosca-problem-definition/SKILL.md) | 同时明确问题、决策者、成功条件、约束和参与者；比单纯拆研究问题更重视谁能采取行动 | 可选；与现有访谈和研究问题拆分存在交集，不必优先增加重复入口 |
| [key-assumptions-check](https://github.com/l4ci/skills/blob/dbfdca4dd1a0d0348a390732591b2b6f0abf5d70/plugins/latticework/skills/key-assumptions-check/SKILL.md) | 与现有 KAC 目标相近，但强调多视角提出假设、并行逐项测试和批评者复核 | 适合作为原版对照，先观察现有 KAC 的实际不足再决定是否试第二个版本 |

这些建议跨项目适用，不把银行研究或开发试点的事实写入通用资产。

## 试用需要明确的差异

- 四项原版都明确要求子 Agent：TOSCA 有三个并行批评者；SCQA 有三个候选视角和两个检查者；strategy-kernel 有四个并行诊断者；KAC 有多轮提出、逐项测试和批评。相较当前结构化 KAC 没有硬性多 Agent 编排的流程，调度和模型调用需求更高；实际成本需测量。
- 仅阅读它们作为候选数据，不会触发这些编排。正式试用前需核对宿主能力和任务授权；若以串行或单 Agent 方式运行，必须记录偏离，不能当成原版编排已验证。
- TOSCA、SCQA、strategy-kernel 要求读取各自 references，接入必须保留完整目录。相邻 Skill 链接不一概视为必须安装的依赖；按所选路线逐项检查。
- 来源目录为 `plugins/latticework/skills/<name>`。当前自动 intake 支持 `skills/<name>`，本次已保留来源布局手工登记；后续需要扩展选集时沿用此方式，或有实际需要时扩展接入器，不能当作“自动支持任意插件来源”的证据。
- 已登记四项 staged 资产；未增加 Profile 或安装配置。有具体任务时按稳定 ID 选择一项，再按统一流程试用。
