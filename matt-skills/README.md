# Matt skills 试用副本

先体验 Matt 的原始研发流程，再根据实际任务决定是否微调。本目录保存 **17 个 skill、完整的各自支持文件和对应上游说明**；目前没有修改上游文件，也没有安装 skill。

固定版本：[`3cca18b368ae95cdbdebbff572ccafa662551015`](https://github.com/mattpocock/skills/commit/3cca18b368ae95cdbdebbff572ccafa662551015)，整理日期：2026-09-06。

## 从这里开始

1. 阅读 [使用指南](GUIDE.md)，先看安装准备和场景选择。
2. 需要后续安装时，按下表选择完整目录；先解决已有同名 skill，再复制。
3. 在实际产品项目中运行 setup，开始一个小任务。这里是资产仓库，不是默认试验产品。
4. 用 [试用模板](trials/TEMPLATE.md) 记录少量有用观察。

[来源和更新方法](SOURCE.md) · [本地差异](LOCAL-CHANGES.md) · [上游 README](upstream/README.md) · [许可](upstream/LICENSE)

## 已保存与建议安装的范围

下面每个链接都指向一个完整 skill 目录的入口。安装单位是整个目录，包括 `agents/`、模板、脚本和参考文件，不能只复制 `SKILL.md`。

| 建议批次 | Skill | 用途 |
|---|---|---|
| 首次：主线 | [setup-matt-pocock-skills](upstream/skills/engineering/setup-matt-pocock-skills/SKILL.md) | 配置项目的 tracker 和领域文档 |
| 首次：主线 | [ask-matt](upstream/skills/engineering/ask-matt/SKILL.md) | 根据情况推荐下一步 |
| 首次：主线 | [grill-with-docs](upstream/skills/engineering/grill-with-docs/SKILL.md) | 澄清目标并维护领域语言 |
| 首次：主线 | [to-spec](upstream/skills/engineering/to-spec/SKILL.md) | 将已讨论内容固化为本次工作规格 |
| 首次：主线 | [to-tickets](upstream/skills/engineering/to-tickets/SKILL.md) | 拆成带依赖的可验证切片 |
| 首次：主线 | [implement](upstream/skills/engineering/implement/SKILL.md) | 按规格或 ticket 实现 |
| 首次：依赖 | [grilling](upstream/skills/productivity/grilling/SKILL.md) | 访谈方法 |
| 首次：依赖 | [domain-modeling](upstream/skills/engineering/domain-modeling/SKILL.md) | 领域词汇和重要决策 |
| 首次：依赖 | [codebase-design](upstream/skills/engineering/codebase-design/SKILL.md) | 模块、接口与 seam 的设计方法 |
| 首次：依赖 | [tdd](upstream/skills/engineering/tdd/SKILL.md) | 约定接口上的 red → green 循环 |
| 首次：依赖 | [code-review](upstream/skills/engineering/code-review/SKILL.md) | 分别审查 Standards 与 Spec |
| 首次：探索与交接 | [research](upstream/skills/engineering/research/SKILL.md) | 查一手来源并留下引用 |
| 首次：探索与交接 | [prototype](upstream/skills/engineering/prototype/SKILL.md) | 用可丢弃原型回答一个问题 |
| 首次：探索与交接 | [handoff](upstream/skills/productivity/handoff/SKILL.md) | 跨会话、目录或工具交接 |
| 后续按需 | [diagnosing-bugs](upstream/skills/engineering/diagnosing-bugs/SKILL.md) | 难 bug 的复现、诊断和回归验证 |
| 后续按需 | [wayfinder](upstream/skills/engineering/wayfinder/SKILL.md) | 跨会话的大型决策规划 |
| 后续按需 | [improve-codebase-architecture](upstream/skills/engineering/improve-codebase-architecture/SKILL.md) | 找到值得改善的模块边界 |

建议首次安装前 14 个，先使用主线入口；其余 3 个已保存，遇到对应任务再安装。安装完整集合也不意味着每次调用全部技能。

主要依赖关系：`grill-with-docs → grilling + domain-modeling`；`implement → tdd + code-review`；`tdd → codebase-design`（需要设计接口时）；`wayfinder → research / prototype / grilling + domain-modeling`；架构扫描使用 `codebase-design + grilling + domain-modeling`。`ask-matt` 是更大上游集合的路由，其中的其他推荐不是这些主线路径的强制依赖。

## 没有收录的入口

`triage`、`wizard`、`resolving-merge-conflicts`、`grill-me`、`wait-what`、`to-questionnaire`、`teach`、`writing-for-agents` 暂未收录。可从 [固定版本的上游目录](https://github.com/mattpocock/skills/tree/3cca18b368ae95cdbdebbff572ccafa662551015/skills) 查看。前几项分别用于外部反馈分诊、人工配置步骤和已有合并冲突。

`ask-matt` 或上游 README 提到未收录的 skill 时，先确认本次是否需要，再补充同一版本的完整目录。不要让 Agent 猜测缺失 skill 的内容，也不要以本仓库的自研 `spec-execution` 自动替代 `implement`。

## 文档边界

- `upstream/`：作者原文；保持英文、目录关系与调用元数据。
- 本目录的中文文档：本地推荐和使用解释，不是 Matt 的原始规则。
- `trials/`：实际体验；初始仅有模板，没有已完成试点。
- 本集合独立试用，不要求采用 Adaptive SDD，也没有加入自研编排层。
