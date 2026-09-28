# DeepSeek Harness 项目技能

`enable --harness dsh` 将选中的完整 Skill 与必需依赖放到目标项目 `.dsh/skills/<source>-<name>/`。项目可用 Git 跟踪副本；不要覆盖已有不同内容。实际调用前检查当前 DSH 版本的技能发现和显式调用能力，保留原有调用策略。

[DSH 官方源码文档](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md)说明目录发现和调用方式。本仓库尚未验证该宿主的原生调用。
