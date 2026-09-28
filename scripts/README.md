# 资产工具

在资产仓库运行，依赖 Python 3.10+ 标准库。`--root` 仅用于另一份资产库或测试夹具。

```sh
python3 scripts/assets.py list
python3 scripts/assets.py show matt/implement
python3 scripts/assets.py check
python3 scripts/assets.py enable --project /absolute/project --harness codex --asset matt/implement
```

`enable` 默认只预览；核对后加 `--apply`，将选中的完整 Skill 和登记的必需依赖复制到项目目录。可重复 `--asset`，或使用 `--profile <id>` 作为选择起点。Codex 写入 `.agents/skills/`，DSH 写入 `.dsh/skills/`。名称稳定地使用 `<source>-<skill>`；所选技能之间的引用和选择器显示名同步调整，来源文件不变。若目录已存在且内容一致，返回 `already-enabled`；不同则停止，不覆盖。来源目录中的许可和第三方声明也会复制到项目技能目录。

项目是否用 Git 跟踪副本由项目决定；本库不自动清理、升级或删除项目文件。启用不会改变 catalog 的成熟状态，也不要求使用记录。项目应在自己的 `AGENTS.md` 说明这些技能适用于哪些任务。

其他命令：`intake` 接入固定来源，`decide` 根据用户决定更新资产库状态。

验证：`python3 -m unittest discover -s tests -v`。测试在临时目录验证来源和文件保护，不调用模型或外部服务。
