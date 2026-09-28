# Codex 项目技能

`enable --harness codex` 将选中的完整 Skill 与必需依赖放到目标项目 `.agents/skills/<source>-<name>/`。项目可用 Git 跟踪这些副本；`AGENTS.md` 说明在什么任务中使用。保留支持文件和 `agents/openai.yaml` 的调用策略，来源版本与稳定名称见预览结果。不同内容的现有目录不会被覆盖。

Codex 会从项目目录发现 Skill；可以按宿主支持的方式显式选择。新文件在现有会话中未出现时，重新打开项目会话。文件在目录中只证明可供发现，不能证明该次任务实际调用了它。

[官方说明](https://learn.chatgpt.com/docs/build-skills)介绍项目和用户发现位置、同名条目及调用元数据。项目副本使用来源前缀，避免同名混淆；用户级技能仍可能同时可用。
