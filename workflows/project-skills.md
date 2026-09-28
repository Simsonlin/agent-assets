# 在项目中启用 Skill

从 catalog 选择项目需要的资产 ID；Profile 只是可选的选择起点，不要求整套安装。先阅读目标项目的 `AGENTS.md` 和选中技能的完整目录，确认用途、依赖和宿主。

使用 `python3 scripts/assets.py enable --project <项目绝对路径> --harness codex --asset matt/implement` 预览。重复 `--asset` 可选择多项，也可改用 `--profile <id>`。核对依赖闭包、来源版本、稳定名称和目标路径后加 `--apply` 写入。工具不会覆盖内容不同的现有技能或许可文件。

Codex 的目标位置为项目 `.agents/skills/`，DSH 为 `.dsh/skills/`。完整技能目录、所选内部引用和选择器显示名随来源前缀调整；上游固定副本不变。安装后由项目 Git 决定哪些副本随项目保存，并在项目 `AGENTS.md` 中写明工作场景。启用不改变 catalog 状态，不要求运行任务、记录效果或事后清理。

更新或移除项目副本时，先看项目 Git 差异和来源版本，再作显式项目变更。当前工具不自动覆盖、升级或删除项目文件；以后有具体需要再增加对应操作。
