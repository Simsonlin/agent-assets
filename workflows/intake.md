# 接入外部候选

输入：用户指定的公开来源或本地 checkout、希望试用的技能与用途。

1. 阅读来源说明、许可、选中 Skill 和完整支持文件。判断方法是否适合任务，区分必需依赖与相邻推荐。不运行来源安装脚本或复制来源项目指令。
2. 将来源获取到临时 checkout；固定 commit，并确认 checkout 未修改。已有候选的升级使用新 source ID 先比较，避免覆盖历史。
3. 运行 `python3 scripts/assets.py intake --checkout <checkout> --source <id> --skill <name> --domain <domain>`；多个 Skill/领域可重复参数。
4. 工具保存完整选中目录、许可和第三方声明，生成校验和与 staged 登记。当前自动接入器识别来源 `skills/<name>/SKILL.md`；其他布局由 Agent保留目录关系接入，不猜测路径。
5. 补充 SOURCE.md 和 GUIDE.md：选择理由、固定在线入口、必需与可选依赖、已知限制。核对相对资源后更新 catalog 中的 dependencies 和 dependency_review；未审查状态不能准备试用。
6. 运行 check，给用户可直接使用的资产 ID 与试用请求。不把接入成功说成方法有效。
