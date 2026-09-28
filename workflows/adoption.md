# 评估、纳入与维护

项目启用不要求正式纳入资产库。若用户要为资产库确立长期维护承诺，再讨论保留原版、特化、纳入或暂缓；已有使用记录可以参考，但不是决定的前置条件。

用户已明确保留决定权。获得本次实际决定后，在 `decisions/` 写 JSON 记录：assets（ID 列表）、state、decided_by: user、user_statement（用户真实表述）、conversation_reference、reason、evidence。不要替用户填肯定意见。

然后运行 `python3 scripts/assets.py decide decisions/<file>.json`，再运行 check。工具更新登记，library 的正式视图随之改变。暂缓/退役也记录同样的依据；无需删除源文件。

需要个人特化时，新资产引用原来源版本并记录修改理由；保持原版可以继续对照。更新外部版本时先接入新的固定候选，检查变更和依赖，再有选择地更新项目副本；现有项目安装不静默更新。
