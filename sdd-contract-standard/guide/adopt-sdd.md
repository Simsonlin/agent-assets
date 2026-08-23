# 采用 SDD

## 1. 选择并记录

复制 [`templates/adoption.md`](../templates/adoption.md) 到项目的 `sdd/adoption.md`，填写标准版本、Profile、模块、采用理由、调整项和重新评估条件。

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

采用标准不等于必须一次迁移全部历史。先从下一个真实 change 开始，再按需要整理旧内容。
