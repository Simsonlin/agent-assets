# SDD Contract Standard

这是一个可由人或 Agent 读取、讨论并复制到项目中的 SDD 采用 Playbook。它不要求所有项目使用同一套重流程；它帮助项目根据歧义、影响、可逆性和治理要求选择合适的 Profile 与模块。

**本文件是唯一启动入口。** 给 Agent 本仓库地址并让它从 `README.md` 开始即可；无需由用户逐份指定材料。地址可以是 Agent 可访问的本地目录或 Git 仓库 URL。

## 让 Agent 帮你选择并采用

把下面这段话连同本仓库地址交给 Agent：

> 阅读这个 SDD Contract Standard 仓库的 `README.md`，按照其中的 Agent 采用流程检查我的项目并与我讨论推荐的 Profile、Persistence 和 Modules。先给出建议、理由、最小产物集和不创建的产物；在我明确确认方案前不要修改项目。确认后再按标准最小落地。

Agent 会按 [Agent 采用流程](./guide/agent-adoption.md) 执行：

```text
读取标准与项目事实
  → 提出必要问题
  → 推荐 Profile / Persistence / Modules
  → 列出最小产物与不创建项
  → 人类确认
  → 创建 adoption 和必要产物
  → 检查并交付
```

最终选择始终由人类确认。Agent 可以基于条件指出 Contract-First 是强制项，但不能擅自切换 Profile、模块或项目策略。

## 三种 Profile

- **Living Spec（默认）**：长期系统持续维护当前 capability spec。
- **Quick Change**：范围明确、生命周期短，不需要长期当前 Spec。
- **Governed Delivery**：存在正式兼容、多个独立消费者、发布门禁或审计要求。

模块独立判断：真实机器边界命中条件时启用 **Contract-First**；重要、长期且可能被反复追问的取舍启用 **ADR**。

## 手工采用

不使用 Agent 时，先阅读 [选择 Profile](./guide/choose-profile.md)，再按 [采用指南](./guide/adopt-sdd.md) 落地。所有采用方式都必须创建 `sdd/adoption.md`，并且不得为了目录完整而创建空的条件产物。

## 内容导航

| 目录/文件 | 用途 |
|---|---|
| [`standard.yaml`](./standard.yaml) | 标准版本、Agent 入口、Profile、模块和模板路径的最小权威登记 |
| [`guide/`](./guide/) | Agent/人工选择、采用、调整与检查流程 |
| [`reference/`](./reference/) | 核心原则、权威边界、Profile、生命周期与 Contract 规则 |
| [`templates/`](./templates/) | 按 Profile 和模块复制的模板 |
| [`examples/`](./examples/) | 从真实项目采用结果提炼的精简示例 |
| [`explanation/`](./explanation/) | 标准来源、权衡与演进理由 |

## 标准边界

当前版本支持 Agent 引导、人工确认和模板复制，不提供 CLI、模板生成器、自动升级或复杂验证器，也不要求安装专用 Skill。标准使用整数版本；只有不兼容的产物名称、字段或生命周期变化才升级版本。
