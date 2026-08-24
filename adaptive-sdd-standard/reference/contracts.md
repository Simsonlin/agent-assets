# Contract 指南

## Contract 解决什么

Contract 描述消费者可以依赖的机器边界，例如 API schema、消息协议、持久化格式、事件、CLI envelope 或稳定中间模型。它不替代 Capability Spec，也不承载设计理由。

命中以下任一条件后，Contract-First 模块为强制：独立消费者、跨运行边界、持久化格式、兼容承诺。

## 载体

按接口选择 JSON Schema、OpenAPI、Protocol Buffers、TypeScript 类型、其他 IDL，或被明确提升为 executable contract 的行为测试。不要为了形式重复维护多个等价定义。

## Contract 与 change

每个 proposal 都声明：

```yaml
specImpact: none | added | modified | removed
contractImpact: none | added | modified | removed
```

Contract 受影响时必须提交 contract delta。Living 项目可以维护当前合同；Governed 项目发布后必须冻结旧版本，新版本新增而非覆盖。

## 合同如何执行

Contract 定义合法边界；Validation 决定何时检查。两者不是同一个问题。

| 情况 | 通常策略 |
|---|---|
| 同一编译单元内的可信数据 | 静态类型通常足够 |
| 跨 iframe、worker、进程或网络 | 建议运行时校验 |
| 外部或不可信输入 | 应运行时校验 |
| 持久化且由未来版本读取 | 应校验并考虑版本 |
| 失败会破坏数据、安全或发布 | 严格校验并 fail closed |

Contract 记录应说明采用静态类型、运行时校验或两者，以及原因。该选择是项目技术策略，不是所有 SDD Profile 的统一硬规则。
