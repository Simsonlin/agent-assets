# 来源、收录范围与更新

## 固定来源

| 项目 | 值 |
|---|---|
| 作者 / 仓库 | [Matt Pocock / mattpocock/skills](https://github.com/mattpocock/skills) |
| 获取分支 | `main`；仅用于本次获取，日常使用固定以下 commit |
| Commit | [`3cca18b368ae95cdbdebbff572ccafa662551015`](https://github.com/mattpocock/skills/commit/3cca18b368ae95cdbdebbff572ccafa662551015) |
| Commit 时间 | `2026-09-04T09:43:27+01:00` |
| Commit 标题 | `Merge pull request #1025 from mattpocock/chore/link-skills-exclude-misc` |
| 获取日期 | 2026-09-06，Asia/Shanghai |
| 许可 | [上游 MIT License 原文](upstream/LICENSE)，Copyright (c) 2026 Matt Pocock |
| 打包方式 | 普通文件选集；不是嵌套 Git 仓库、submodule 或已安装插件 |
| 初始本地源码修改 | 无；见 [LOCAL-CHANGES.md](LOCAL-CHANGES.md) |

## 精确收录规则

保留以下 15 个 engineering skill 的完整目录：

```text
ask-matt
code-review
codebase-design
diagnosing-bugs
domain-modeling
grill-with-docs
implement
improve-codebase-architecture
prototype
research
setup-matt-pocock-skills
tdd
to-spec
to-tickets
wayfinder
```

以及 2 个 productivity skill：`grilling`、`handoff`。

每个目录中的全部文件原样复制，包括 `SKILL.md`、`agents/openai.yaml`、Markdown 支持文件和脚本模板。另复制每个 skill 对应的 `docs/<category>/<name>.md`，以及根 `README.md` 和 `LICENSE`。

合计：17 个 skill、17 份对应讲解、69 个上游文件。`upstream/` 下的相对路径与源仓库完全一致；其余上游目录没有收录，包括作者的项目指令、插件配置、构建依赖、未选中的 skill 和实验技能。

[SHA256SUMS](SHA256SUMS) 列出全部上游文件的初始 SHA-256；它不涵盖本地中文指南。当前清单与上游固定提交逐文件一致。

## 选集的导航边界

上游 README 保留完整目录导航，因此其中以下 9 个相对链接目标不在本地选集。它们不是已选 skill 主线路径所需的文件；查看时使用这些固定版本链接：

- [插件分发 ADR](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/.agents/adr/0002-ship-as-a-claude-code-plugin.md)
- [resolving-merge-conflicts](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/resolving-merge-conflicts/SKILL.md)
- [triage](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/triage/SKILL.md)
- [wizard](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/wizard/SKILL.md)
- [grill-me](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/productivity/grill-me/SKILL.md)
- [teach](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/productivity/teach/SKILL.md)
- [to-questionnaire](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/productivity/to-questionnaire/SKILL.md)
- [wait-what](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/productivity/wait-what/SKILL.md)
- [writing-for-agents](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/productivity/writing-for-agents/SKILL.md)

`ask-matt` 也在正文中提到这些未选技能。其推荐范围比本选集大，使用时提供实际安装清单。`CONTEXT-FORMAT.md` 中示例项目路径和 wayfinder 模板中的 `link` 是原始模板占位，不是漏复制文件。上游链接到外部网站的内容仍需联网，不代表整个文档集合可完全离线浏览。

## 本次静态检查

- 69 个上游文件与上述 commit 的 checkout 逐字节一致。
- 所选 17 个 skill 文件夹完整，对应说明存在；内部实际支持文件链接均能解析。
- 用 Ruby 的 YAML 解析器检查 17 份 frontmatter 与 17 份 `agents/openai.yaml`：名称与目录一致，描述非空；显式调用 skill 的 `allow_implicit_invocation: false` 已保留。
- 中文指南的本地文件链接已检查；上述 9 个选集导航遗漏单独登记。
- skill-creator 的 `quick_validate.py` 因可用 Python 缺少 PyYAML 未能运行；没有为此安装依赖。该脚本的字段白名单也不包含上游的 `disable-model-invocation` 和 `argument-hint`。本次采用上述 YAML 与文件完整性检查，不为通过通用校验而删除上游字段。
- 没有安装或调用这些 skill 执行产品任务，没有运行附带的诊断脚本。静态检查不证明它们在当前宿主的实际行为；运行体验留待 [trials](trials/TEMPLATE.md)。

## 后续怎样更新

1. 先阅读现有 [本地差异](LOCAL-CHANGES.md) 和试用记录，确认是否需要更新。
2. 将上游新版本取到另一个临时 checkout，记录候选 commit；不要直接用浮动 `main` 覆盖副本。
3. 按上面的精确清单比较完整目录、对应讲解与调用元数据，检查新增依赖、删除或改名；需要增减选集时同步 README 清单。
4. 对已有本地修改逐项判断保留还是撤销；保持安装源只有一份明确版本。
5. 确定更新后替换选中的上游文件，清理本选集内已经由上游删除的旧文件，保留中文指南并更新其已知问题。不要复制上游 `.git`、项目 AGENTS/CLAUDE 指令或安装配置。
6. 更新本页 commit、日期、收录范围和验证结果；从新上游基线重新生成 SHA256SUMS，再检查文件和引用。
7. 将安装到产品项目作为后续独立操作；仓库更新不会自动更新已安装副本。试用记录保留当时的版本，不批量改写历史。

若仅对当前版本做本地微调，保持 SHA256SUMS 为原始基线，以便看见差异。macOS 下可在 `matt-skills/` 目录执行 `shasum -a 256 -c SHA256SUMS` 检查现有文件是否仍等于基线；新增文件另与清单比较。
