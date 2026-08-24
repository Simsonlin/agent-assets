# Execution Intent

Execution Intent 描述一次 change 为什么实施、需要多强的证据，以及哪些残余风险可以接受。它与 Profile 正交：Profile 决定产物持久化和治理，Intent 决定本次执行强度。

## 三种 Intent

| Intent | 目标 | 默认信心目标 | 典型证据 |
|---|---|---|---|
| Probe | 快速验证想法、集成可行性或方向性假设 | directional | 最小真实路径、人工观察、第三方试用结果 |
| Delivery | 交付可用行为并控制实质回归 | reasonable | Acceptance Criteria、现有测试、直接行为检查、必要人工验证 |
| Assurance | 精密实现高风险逻辑、合同、迁移、安全或发布门禁 | high | 可追溯验证、失败路径、兼容/回滚、独立复核 |

Intent 不由代码行数、团队大小或模板数量决定。Quick Change 可以是 Assurance；Governed Delivery 中也可以存在一个用于决策的 Probe，但 Probe 结果不能自动满足发布门禁。

## Change 必需语义

新 change 应声明：

```yaml
executionIntent: probe | delivery | assurance
```

并在正文说明：

- **Required evidence**：为本次目标决策必须获得的证据；
- **Unavailable verification**：Agent 或当前环境不能忠实完成的检查，以及后续责任方；
- **Acceptable residual risks**：在当前 Intent 下明确接受的已知风险；
- **Confidence target**：只有需要覆盖默认值时才填写。

旧 change 缺少 `executionIntent` 时兼容解释为 `delivery`，不要求批量迁移。Agent 可以建议修改 Intent，但未经人类确认不得自行切换。

## 证据原则

- 测试默认是证据，不是行为权威，也不是数量目标。
- 只有能证明 Acceptance Criteria 或实质风险时才新增测试、fixture 或模拟环境。
- fixture 可以验证本地假设，不能冒充真实第三方行为。
- 人工验证是合法证据；不可自动完成时应明确记录，不得制造合成 PASS。
- Probe 允许 `SUPPORTED | REJECTED | INCONCLUSIVE`，其中 Inconclusive 不是失败，也不是通过；非 Probe 序列化为 `NOT_APPLICABLE`。

## 双状态

实施结果与目标验证分别记录：

- Implementation：`COMPLETE | INCOMPLETE | BLOCKED`
- Goal/verification：`CONFIRMED | READY_FOR_HUMAN_VALIDATION | UNCONFIRMED`

以上新字段使用这里给出的全大写值作为规范序列化形式，避免同一状态出现多种拼写。

因此实现可以完成，但因为真实第三方或人工检查尚未执行而保持 `READY_FOR_HUMAN_VALIDATION`。这比把 change 整体标成模糊的 PASS/FAIL 更准确。
