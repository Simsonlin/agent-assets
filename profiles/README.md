# 用途组合

Profile 只选择资产，不定义项目事实，也不表示自动执行全部 Skill。文件名与 id 相同，assets 列出稳定 ID；prepare 按依赖图补全资源。

- engineering-exploration：Matt 模块设计方法，适合范围明确的设计检查。
- engineering-matt：Matt 主线与底层依赖，供完整体系试用。
- research-assumptions：结构化分析中的关键假设检查，适合已有明确结论的材料。
- research-analysis：问题分解、信息质量、竞争假设、关键假设的候选组合，按任务选用。

使用时指定 `--profile <id>`；也可用多个 `--asset <id>` 只试当前需要的能力。资产库 Profile 与 Adaptive SDD 的交付 Profile、DSH 的启动 Profile 是不同概念。
