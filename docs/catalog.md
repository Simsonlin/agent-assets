# 资产登记与分类

`catalog.json` 使用 Python 标准库即可处理。运行 `python3 scripts/assets.py check` 检查路径、名称、依赖图、来源校验和、Profile 引用以及需要人工决定的状态。

## 字段

每个资产有稳定的 `source/name` ID；`kind` 表示 skill、standard、workflow、template 或 tool；`domains` 是可以扩展的领域标签。`path` 与 `entrypoint` 指向唯一源位置。`source` 连接 URL/commit 或个人工作区来源。

资产库状态：`available` 表示已登记、可按依赖检查结果选择；`adopted` 表示用户决定长期维护；`deferred` 表示暂缓；`retired` 表示退役。项目启用不改变资产库状态，不需要先完成试验。后三种状态必须关联用户决定记录。

`dependencies` 只登记所选运行路线必须准备的其他资产。`dependency_review` 必须为 reviewed 才能在项目启用。可选相邻技能、尚未收录入口、条件分支在来源指南说明；不将全文出现的每个技能都当依赖。

`sources[].checksums` 对整个选集固定副本进行校验。个人源码使用工作区版本；项目 Git 记录启用副本。校验和发生变化时，先判断来源更新还是个人特化，不重算旧基线来抹掉差异。

## 与学习主题的关系

[学习主题](../learning/README.md) 用稳定资产 ID、源码入口和用途建立关联，不另行登记资产身份、当前版本或状态。实践记录保留当时实际使用的版本，供回查；它不替代 catalog 的当前登记。一个主题可以引用多个资产，同一资产可以被多个主题引用。

主题本身不作为资产登记；提炼出可复用工具或方法后，才按资产规则登记其唯一源码位置。资产正文和 catalog 不反向维护具体主题列表，项目启用也不需要复制主题材料。

## 个人资产

- [explain-for-understanding](../skills/explain-for-understanding/SKILL.md)：跨领域讲解、材料澄清与工作结果核查；首版待目标项目实践。
- [grilling](../skills/grilling/SKILL.md)
- [grill-me](../skills/grill-me/SKILL.md)
- [wait-what](../skills/wait-what/SKILL.md)
- [spec-execution](../skills/spec-execution/SKILL.md)

后四项已有个人使用，但没有据此自动变成 adopted。自写 Skill 的完整源码放在 `skills/`，登记为 available 即可按需选用；目录位置不代表成熟度或正式纳入。设计依据与实践反馈可由相关学习主题记录，资产仍可独立运行。

Adaptive SDD 作为 standard 登记，按其采用指南使用，不能当成 Skill 目录安装。

## 正式纳入与物理目录

纳入先改变登记和维护承诺，不强制搬目录。完整外部套件可继续保留原路径，只将选中的稳定 ID 放进常用组合；形成个人特化时为它登记新 ID、来源与差异，不复制项目事实。
