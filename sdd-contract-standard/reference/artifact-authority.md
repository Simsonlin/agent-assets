# 产物权威边界

| 位置 | 回答的问题 | 默认权威内容 |
|---|---|---|
| `specs/` | 系统当前做什么？ | 当前可观察行为与能力边界 |
| `changes/` | 接下来准备改变什么？ | proposal、delta、任务和进行中证据 |
| `decisions/` | 为什么选择这个方向？ | 方案、取舍、后果与 supersession |
| `contracts/` | 消费者能依赖什么机器边界？ | schema、IDL、类型、协议和兼容规则 |
| `src/` | 如何实现？ | 实现细节 |
| `tests/`、`verification/` | 如何证明？ | 自动或人工证据 |
| `gate/` | 发布前必须有哪些证据和授权？ | required evidence 与 release decision |

## 避免重复

- Spec 可以引用 Contract，不复制字段、枚举和协议正文。
- Contract 不记录技术选型理由；理由进入 ADR 或 proposal/design。
- Acceptance Criteria 定义本次 change 如何判定完成，不替代当前 capability spec。
- Verification 记录观察结果，不重新定义预期行为。
- 状态字段不表达测试结果；状态和证据分别记录。

Governed change 中，proposal 定义目标和初始证据边界；verification plan 引用它并将证据展开为可执行检查；release decision 只汇总实际结果、偏差和批准例外。发布门禁以 `gate/` 中适用的 required evidence 和 release decision 为权威，不在三个产物中重复改写同一要求。

## Executable authority 例外

测试默认只是证据。只有同时满足以下条件，才可将人类可读的可执行产物声明为行为 Contract 或 Spec：

- 项目明确登记其权威角色；
- 人可以直接理解它表达的行为；
- 实现和其他验证引用它，而不是复制同一事实；
- 变更与归档遵循相应 Spec 或 Contract 生命周期。
