# 标准人工检查清单

首版不提供自动验证器。修改本标准后人工检查：

- [ ] `standard.yaml` 中引用的模板路径全部存在。
- [ ] `standard.yaml` 中的 Agent entrypoint 和 required reads 全部存在。
- [ ] Profile 必需产物与模板目录一致。
- [ ] README、guide、reference 与模板之间的链接有效。
- [ ] Profile 选择结果在 README 与 `choose-profile.md` 中一致。
- [ ] Execution Intent 在 README、reference、guide 与模板中的语义一致，并与 Profile 保持正交。
- [ ] Agent 流程在写项目文件前要求人类确认 Profile、Persistence 和 Modules。
- [ ] Agent 推荐会列出最小产物、条件产物和明确不创建项。
- [ ] 模板没有要求为未触发的条件产物创建空文件。
- [ ] 新 change 模板包含 execution intent、required evidence、unavailable verification 和 acceptable residual risks。
- [ ] 验证模板分别记录 Implementation 与 Goal/verification 状态；Probe 可以记录三态假设结果。
- [ ] 示例来自可追溯的真实采用，包含 `sdd/adoption.md`，并能演示一次完整状态流转。
- [ ] 普通兼容修改未错误升级标准版本。
- [ ] 不兼容的名称、字段或生命周期变化已升级整数版本并提供一份迁移说明。
