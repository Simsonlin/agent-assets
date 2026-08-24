# Profiles

## Quick Change

- **适用**：范围明确的修复、短期实验、小型变更，没有长期当前 Spec 需求。
- **持久化**：spec-first。完成后归档 change，不要求维护 `specs/`。
- **必需**：`change.md`、`tasks.md`。
- **条件**：ADR、Contract delta。

## Living Spec（默认）

- **适用**：长期系统、能力持续演进、多会话或多人协作。
- **持久化**：spec-anchored。`specs/` 持续代表当前行为。
- **必需**：当前 capability spec；每个 change 的 proposal、spec delta、tasks。
- **条件**：design、verification、ADR、Contract delta。

完成 change 时先把 delta 合并到当前 Spec，再归档 change。当前 Spec 不保留历史态叙述。

## Governed Delivery

- **适用**：正式兼容承诺、多个独立消费者、发布门禁、审计或 fail-closed 要求。
- **持久化**：spec-anchored，并对机器边界使用 contract-as-source。
- **必需**：Living 的核心产物，加 verification plan 和 release decision。
- **条件**：design、ADR、contract delta、migration/rollback。

已发布合同冻结并版本化；版本方式由接口生态决定，不统一强制 SemVer。只有同时维护多个版本且运行时需要选择时，才引入 `CURRENT` 指针或等价 manifest。

## 产物矩阵

| Profile | 每次 change 必需 | 条件触发 |
|---|---|---|
| Quick | change、tasks | ADR、contract delta |
| Living | proposal、spec delta、tasks | design、verification、ADR、contract delta |
| Governed | proposal、spec delta、tasks、verification plan、release decision | design、ADR、contract delta、migration/rollback |

Profile 不决定单次 change 的执行强度。完成 Profile 选择后，按 [Execution Intent](./execution-intent.md) 为 change 选择 Probe、Delivery 或 Assurance。
