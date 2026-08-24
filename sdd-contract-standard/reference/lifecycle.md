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
- 完成记录分别保存 Implementation 与 Goal/verification 状态；Probe 另记录假设为 SUPPORTED、REJECTED 或 INCONCLUSIVE。
- 通常只有 `COMPLETE + CONFIRMED` 才进入 `completed`。如果 Acceptance Criteria 明确把人工验证交接或不确定结论定义为合法终态，也可用 `COMPLETE + READY_FOR_HUMAN_VALIDATION`，或 Probe 的 `INCONCLUSIVE` 完成 change，但必须记录未完成验证和后续责任方。
- `INCOMPLETE`、`BLOCKED`，以及仍有必需验证待完成的 `UNCONFIRMED` 不得标为 `completed`；继续处理时保持 `in-progress`/`verifying`，放弃时转 `rejected` 并保留原因。

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
