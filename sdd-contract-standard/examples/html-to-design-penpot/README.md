# Example: html-to-design-penpot

这是从真实项目 `html-to-design-penpot` 的本地提交 `ca8b897 docs: adopt living spec SDD standard` 提炼的精简示例。它记录实际选择和迁移结果，不把尚未执行的验证或功能描述成已完成。

## 项目事实

- 项目长期演进，需要持续描述静态 HTML → Penpot 的当前能力和已知边界；
- UI iframe 与 Penpot plugin sandbox 通过消息传递 `ConvertMessage`、`ParsedNode` 和返回消息；
- TypeScript 类型已被两端共同引用；
- 项目存在需要长期保留理由的范围和 fidelity 取舍；
- 没有公共兼容承诺、正式发布门禁或多版本合同需求；
- 最终视觉验收由项目负责人执行，Agent 不代替给出通过结论。

## 推荐与人类确认

| 选择 | 结果 | 项目事实 |
|---|---|---|
| Profile | Living Spec | 需要长期维护当前 capability spec |
| Persistence | spec-anchored | change 完成后把 delta 合并到当前 Spec |
| Contract-First | enabled | 消息跨 UI iframe 与 plugin sandbox 运行边界 |
| ADR | enabled | 范围、合同载体和 fidelity 方案需要长期理由 |
| Governed Delivery | not selected | 没有公共兼容、正式发布或审计门禁 |

人类确认后才执行迁移；确认没有授权修改插件运行逻辑、增加运行时消息校验或 push。

## 最小采用结果

```text
sdd/adoption.md
specs/static-html-to-penpot/spec.md
contracts/ui-plugin-messages/contract.md
decisions/ADR-0001-...
decisions/ADR-0002-...
decisions/ADR-0003-...
changes/20260821-stabilize-text-import/
changes/archive/2026/20260823-adopt-sdd-standard/
```

- capability spec 成为当前 WHAT 的权威；
- Contract 只登记机器边界，字段仍以既有 `src/lib/types/index.ts` 为唯一权威，没有复制 JSON Schema；
- ADR 保留 WHY；
- 尚未实施的文本稳定性方案保留为 active change，没有创建空 verification；
- 旧 Level 模型、混合型能力基线和 fork foundation 文档被当前 Spec、ADR、Contract 与 change 取代。

采用记录的精简快照见 [`sdd/adoption.md`](./sdd/adoption.md)。

## 一次完整状态流转

真实提交保存的是 completed 后的归档快照，没有为每个中间状态分别创建 Git commit；归档的 proposal、tasks 和 verification 共同体现了以下完整生命周期检查点：

```text
proposed → approved → in-progress → verifying → completed → archived
```

它声明 `specImpact: added`、`contractImpact: added`，记录了实施授权、迁移任务和验证结果，因此创建 spec delta、contract delta 与 verification；目录调整不需要独立设计，因此没有创建 design。完成时 delta 已合并到当前 Spec/Contract，change 归档。

文本稳定性 change 仍是 `proposed`：它有 design 和 ADR，但尚未实施，所以没有 verification record，也没有把目标行为合并进当前 capability spec。这展示了“决策已记录”“允许实施”“验证通过”和“视觉验收通过”是不同状态。

## 从真实采用得到的规则

- 识别到真实机器边界时，不应因为项目规模小而延迟登记 Contract；
- Contract 可以复用已有 TypeScript 类型，不需要为了形式新增 schema；
- 迁移旧文档应按权威职责提炼，不机械复制历史文件；
- Agent 的文档检查通过不等于项目负责人的视觉验收通过；
- 未实施 change 不创建空 verification，也不污染当前 Spec。
