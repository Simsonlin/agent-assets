# 资产工具

在资产仓库运行，依赖 Python 3.10+ 标准库。也可从其他项目用脚本绝对路径调用；--root 只用于指定另一份资产库或测试夹具。

```sh
python3 scripts/assets.py list
python3 scripts/assets.py list --domain research
python3 scripts/assets.py show matt/codebase-design
python3 scripts/assets.py check
python3 scripts/assets.py prepare --project /absolute/project --harness codex --profile engineering-exploration --task '检查一个明确的模块设计问题'
```

prepare 默认预览。确定后增加 --apply 执行；可用 --run 固定一个唯一 run ID，重复运行不会覆盖。可用重复 --asset 参数替代或补充 Profile。

```sh
python3 scripts/assets.py verify <run-id>
python3 scripts/assets.py record <run-id> --used matt/codebase-design --outcome limited --note '实际观察与限制' --evidence trials/<run-id>/observations.md
python3 scripts/assets.py cleanup <run-id>
```

只有真实发现和调用证据充分时才为 record 增加 --discovery verified、--invocation verified。useful 需要已验证调用及存在的证据文件；准备检查可记 inconclusive。record 不覆盖历史条目。

试用副本用独立名称，Markdown/YAML/JSON 中所选技能标识符会转换；外部 URL 与非文本资源保留。完整上游目录及调用策略不丢失，清单保存原始/安装后摘要与替换数量。命名转换是试用适配，记录时应说明；不能将“转换后可用”当成所有原版宿主组合都已验证。

verify/cleanup 遇到不一致返回码 2；输入或登记错误返回码 1。cleanup 保护有后续编辑、新增资源、符号链接或不完整写入的目录，并输出待人工检查项。修正为清单原状后可以重试；不要绕过工具批量删除项目技能。

接入与纳入命令见 [intake](../workflows/intake.md)、[adoption](../workflows/adoption.md)。

验证脚本：`python3 -m unittest discover -s tests -v`。测试在临时目录验证文件保护和生命周期，不调用模型或外部服务。
