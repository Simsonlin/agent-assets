# 采用 SDD

本页描述方案已经由人类确认后的落地步骤。使用 Agent 时，必须先完成 [选择与确认流程](./agent-adoption.md)；确认前不修改项目。

## 1. 选择并记录

复制 [`templates/adoption.md`](../templates/adoption.md) 到项目的 `sdd/adoption.md`，填写标准来源地址、revision、版本、Profile、模块、采用理由、调整项和重新评估条件。

推荐统一目录词汇：

```text
sdd/             采用记录
specs/           当前能力行为
changes/         提议中和实施中的变更
decisions/       长期决策
contracts/       机器接口与兼容边界
verification/    验证证据
gate/            发布所需证据与决策
```

Profile 决定哪些目录需要出现。没有内容时不要创建空目录或空文件。

## 2. 复制最小模板

- Quick：为 change 复制 `change.md` 和 `tasks.md`。
- Living：先建立当前 capability spec，再为 change 复制 proposal、spec delta 和 tasks。
- Governed：在 Living 基础上增加 verification plan 和 release decision，并维护已发布合同。

仅在条件命中时复制 design、verification、ADR、contract delta 或 migration/rollback。

新项目不要把计划中的目标能力直接写成已经实现的当前事实。未实现行为进入 proposal/spec delta；capability spec 可以先保持 `draft`，并在 change 完成时合并成为当前行为。

现有项目迁移时先区分：

- 当前可观察行为 → capability spec；
- 正在提议或实施的改变 → active change；
- 有长期价值的理由 → ADR；
- 机器边界 → Contract；
- 检查或事故结果 → verification/change evidence；
- 纯历史且仍有解释价值 → archived change。

不要机械复制旧编号、旧阶段清单或已经被替代的策略。被新 Profile/Module 模型替代的旧策略应退休，避免两套现行规则。

## 3. 使用统一命名

```text
specs/<capability-id>/spec.md
changes/YYYYMMDD-<change-id>/
changes/archive/YYYY/YYYYMMDD-<change-id>/
decisions/ADR-NNNN-<title>.md
contracts/<contract-id>/
verification/<change-id>/
gate/<release-id>/
```

ID 使用小写 kebab-case。ADR 使用递增编号。日期只帮助 change 排序，不代表版本。

## 4. 完成与归档

- Quick：记录验证结果后原样归档。
- Living：先把 spec delta 合并到当前 `specs/`，再归档。
- Governed：先完成合同发布、验证和 release decision，再归档。
- rejected change 也归档并保留拒绝原因。

采用标准不等于必须一次迁移全部历史。只迁移维持当前权威、解释长期决策或继续推进真实 change 所必需的内容。

## 5. 完成检查

- `sdd/adoption.md` 与实际 Profile、模块和目录一致；
- 每个 change 都声明 `specImpact` 和 `contractImpact`；
- 条件产物有真实触发原因，不存在空文件；
- Spec 不复制 Contract 字段，Contract 不复制实现理由；
- 验证证据、实施授权和发布授权分开；
- 旧链接已更新，同一事实没有第二个现行权威来源。
