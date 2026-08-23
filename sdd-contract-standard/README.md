# SDD Contract Standard

一套可按项目风险选择、复制即用的 SDD 参考、指南与模板。它不是要求所有项目采用同一套重流程，而是帮助你在约 15 分钟内回答三件事：

1. 当前项目适合哪个 Profile；
2. 必须创建哪些产物，哪些只在条件命中时创建；
3. 下一步从哪份模板开始。

## 快速开始

1. 阅读 [选择 Profile](./guide/choose-profile.md)。
2. 按 [采用指南](./guide/adopt-sdd.md) 复制所需模板。
3. 在项目中创建 `sdd/adoption.md`，记录 Profile、模块、调整项和重新评估条件。
4. 通过一个真实 change 验证流程；不要为了目录完整创建空文件。

默认建议是 **Living Spec**。一次性或低风险改动可用 **Quick Change**；存在正式兼容、发布或审计要求时使用 **Governed Delivery**。

## 内容导航

| 目录/文件 | 用途 |
|---|---|
| [`standard.yaml`](./standard.yaml) | Profile、模块、版本和模板路径的最小权威登记 |
| [`guide/`](./guide/) | 如何选择、采用和调整策略 |
| [`reference/`](./reference/) | 权威边界、Profile、生命周期与核心规则 |
| [`templates/`](./templates/) | 按 Profile 和模块复制的模板 |
| [`explanation/`](./explanation/) | 规范来源、权衡与历史案例 |
| [`sdd-contract-standard.md`](./sdd-contract-standard.md) | 旧入口兼容页 |

## 首版边界

首版采用人工选择和复制，不提供 Skill、CLI、模板生成器、自动升级或复杂验证器。标准自身使用整数版本；只有不兼容的产物名称、字段或生命周期变化才升级版本。
