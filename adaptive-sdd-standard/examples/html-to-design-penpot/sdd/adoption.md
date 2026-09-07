---
standard: adaptive-sdd-standard
standardVersion: 1
standardSource: agent-assets/adaptive-sdd-standard
standardRevision: 7d21795
profile: living-spec
persistence: spec-anchored
modules:
  - contract-first
  - adr
adoptedAt: 2026-08-23
---

# SDD Adoption

## 采用理由

项目需要持续维护静态 HTML → Penpot 的当前能力，因此采用 Living Spec。UI iframe 与 Penpot plugin sandbox 是真实运行边界，因此启用 Contract-First。范围、合同载体和 fidelity 取舍需要长期保留理由，因此启用 ADR。

## 项目目录映射

使用标准推荐的 `sdd/`、`specs/`、`changes/`、`decisions/` 和 `contracts/`。消息字段的唯一权威载体是项目已有的 `src/lib/types/index.ts`；Contract 记录只引用它。

没有独立验证证据时不创建空 `verification/`；没有发布门禁，不创建 `gate/`。

## Overrides

- change 的少量 verification 与 change 一起保存。
- 当前合同没有公共兼容版本，不创建版本目录或 `CURRENT`。

## Core deviations

none。

## 重新评估触发条件

- 出现第二个 writer、独立消费者、持久化消息或跨仓库接口；
- 开始公共分发、兼容承诺或正式发布门禁；
- 决定为跨 sandbox 消息增加运行时校验；
- 人工视觉验收成本需要自动化。

## Adoption history

| 日期 | Profile/模块变化 | 原因 | 决策链接 |
|---|---|---|---|
| 2026-08-23 | 初始采用 Living Spec + Contract-First + ADR | 持续能力 Spec、真实消息边界和长期决策 | 真实项目 commit `ca8b897` |
