# 生命周期

## Change

```text
proposed → approved → in-progress → verifying → completed → archived
    └────────────────→ rejected → archived
```

- `approved` 只代表允许实施，不代表允许发布。
- `completed` 表示验收条件已处理并记录结果。
- Living/Governed 在归档前必须完成 Spec delta 合并。
- 状态不编码 PASS/FAIL；结果进入 verification 或任务记录。

## Decision

```text
proposed → accepted | rejected
accepted → deprecated | superseded
```

已接受决策不回写成另一种历史；方向变化时创建新决策并引用被替代项。

## Capability Spec

```text
draft → active → deprecated → archived
```

当前 Spec 描述当前行为。变更历史由 archived changes 和 decisions 承担。

## 命名与归档

```text
changes/YYYYMMDD-<change-id>/
changes/archive/YYYY/YYYYMMDD-<change-id>/
```

rejected change 也归档，保留拒绝原因。
