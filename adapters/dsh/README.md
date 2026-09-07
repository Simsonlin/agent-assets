# DeepSeek Harness 试用适配

首个验证基线为本机 @deepseek-ai/dsh 0.1.2-alpha.2。prepare 将临时完整目录放到目标项目 `.dsh/skills/<trial-name>/`；该版本还支持项目 .agents/skills、用户 .dsh/skills 和用户 .agents/skills。

显式调用形式为 `/<trial-name>`。保留 `disable-model-invocation` 和 `user-invocable`；显式注入与 skill 工具加载是不同路径，不重复加载同一份已注入正文。核对技能目录与实际资源路径。

先检查正在使用的 DSH preset 是否提供 skills 能力，再运行。CLI 的 --profile 是 DSH 启动配置，不是本库 Profile。`dsh --profile headless --help` 在尚无该 profile 时也可能创建用户目录，不能把它当作绝对无写入的检查。

优先使用用户已有的运行环境。若需要临时 headless 环境，放在独立临时 DSH_HOME，避免改用户的 web/desktop profile。不要复制或输出用户凭据；可通过宿主支持的共享凭据入口使用现有授权。缺失模型服务或未完成真实调用时明确记录，目录检查不算模型试用。

[官方源码文档](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md)说明目录优先级、调用策略及动态发现。版本演进较快，实际验收以当前安装代码和可观察运行结果为准。

## 当前验证状态

2026-09-07 已完成文件准备、摘要核对和撤销。用户因 DSH 无法启动而要求先跳过实际运行；原生发现、调用和方法效果均未验证，也没有发送研究材料到 DeepSeek。见 [试用记录](../../trials/20260907-research-dsh/observations.md)。恢复时创建新试用，不复用已清理副本的调用路径。
