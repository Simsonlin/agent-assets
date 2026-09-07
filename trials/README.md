# 试用记录

每次试用使用独立 run ID。`trials/<run>/record.json` 记录实际使用/尝试的资产、逐文件源摘要、宿主、结果与证据；手写观察和产物引用放在同目录。

`.local/trials/<run>/manifest.json` 保存本机安装路径、转换、文件摘要和清理状态，不提交。record 不保存凭据、完整对话或隐藏推理；方法与目标项目效果分别评估。

结果可为 useful、limited、inconclusive、blocked。native_discovery 和 native_invocation 分别记录 verified/unverified；主 Agent 直接阅读后执行时标记 manual-guided 并保持 native 字段 unverified。

纳入建议与用户实际决定分开保存。首版可以没有 adopted 资产，不能为了完成演练伪造决定。

本轮入口：[首轮建议](recommendations-2026-09-07.md) · [Codex 试用](20260907-design-codex/observations.md) · [DSH 待续测](20260907-research-dsh/observations.md) · [观察模板](TEMPLATE.md)。
