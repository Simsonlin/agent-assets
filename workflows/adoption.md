# 评估、纳入与维护

Agent 根据具体试用记录建议保留原版、继续观察、领域特化或正式纳入。说明适用边界、所需环境和维护成本；一次成功只能证明该任务，不推断跨场景稳定。

用户已明确保留决定权。获得本次实际决定后，在 trials/decisions 写 JSON 记录：assets（ID 列表）、state、decided_by: user、user_statement（用户真实表述）、conversation_reference、reason、evidence。不要替用户填肯定意见。

然后运行 `python3 scripts/assets.py decide trials/decisions/<file>.json`，再运行 check。工具更新登记，library 的正式视图随之改变。暂缓/退役也记录同样的依据；无需删除源文件。

需要个人特化时，新资产引用原来源版本及触发修改的试用记录；保持原版可以继续对照。更新外部版本时先接入新的固定候选，检查变更和依赖，再有选择地替换 Profile 的资产 ID；现存试用安装不静默更新。
