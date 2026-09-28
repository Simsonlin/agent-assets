# 外部 Skill 暂存区

所有已接入的外部候选统一放在这里，按来源分目录。只存放文件不会自动安装或加载到项目。

| 来源 | 已收录 | 从这里进入 |
|---|---|---|
| mattpocock/skills | 17 个 Skill | [Matt 选集与完整入口](matt/README.md) |
| radarist/structured-analytic-skills | 8 个 Skill | [结构化分析选集与完整入口](structured/README.md) |
| l4ci/skills · latticework | 4 个 Skill | [latticework 选集与完整入口](latticework/README.md) |

```text
staging/
├── matt/               # 17 项
├── structured/         # 8 项
└── latticework/        # 4 项
    ├── README.md       # 每个来源均有本地导航
    ├── SOURCE.md       # 来源、固定版本
    ├── GUIDE.md        # 来源使用说明
    ├── SHA256SUMS.json # 原始文件摘要
    └── upstream/      # 作者原始文件，保留原目录关系
```

`upstream` 是“上游来源”的意思。在这里仅表示固定版本的原版文件副本，不会自动跟随远端更新，也不是额外的资产分类。将它与本地指南分开，可以清楚区分作者原文和个人记录，并保留原有相对资源路径。源码实际位置由 catalog 登记，不强制所有来源的内部目录完全相同。

新来源按 [接入流程](../workflows/intake.md) 收录完整 Skill、支持资源和许可；按 [项目启用流程](../workflows/project-skills.md) 选择需要的目录。staging 的物理位置不决定项目是否启用或资产库是否正式纳入。

已接入 4 项 latticework 资产：[来源评估](../docs/latticework-assessment.md)。
