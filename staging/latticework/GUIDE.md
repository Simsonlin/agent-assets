# latticework 试用指南

使用 [统一流程](../../workflows/trial.md) 按单项资产准备，完整资源由 catalog 定位。首批 4 项不强制组成流水线，也没有新建默认 Profile。

## 选择与输入

| 资产 | 最小输入 | 原版编排 |
|---|---|---|
| scqa-pyramid | 已有结论和支撑材料、面向的读者；可指定篇幅/形式 | 三个候选视角、两名逻辑检查者 |
| strategy-kernel | 组织或事项、具体战略障碍；可给现有策略 | 四个并行诊断视角，再综合策略 |
| tosca-problem-definition | 需要澄清的问题与能参与回答的人 | 逐项访谈后，三个并行批评者 |
| key-assumptions-check | 结论及支持它的推理；可补充背景和用途 | 多视角列假设、逐项测试、多名批评者 |

原版均要求子 Agent。catalog 的 runtime_requirements 作说明，当前 prepare 不检查或提供宿主调度能力；dependency_review=reviewed 仅表示所选文件路线已审查。实际调用前由 Agent 核对宿主与本次任务边界，环境不支持时记录限制，不能声称串行执行等于原版多 Agent 验证。

## 文件与依赖审查

- 三个有理论参考文件的入口分别完整保留 references/pyramid.md、references/strategy-kernel.md、references/tosca.md；四项均保留作者示例及示例索引。
- 本轮选定独立任务路线没有必须加载的其他 Skill，dependencies 因此为空。相邻链接是选题、前后续方法或替代用途推荐，不自动执行。
- 原文未收录的相邻入口包括 mece-decomposition、storm-research、swot-analysis、porters-five-forces、blue-ocean-strategy、hoshin-kanri、okr、analysis-of-competing-hypotheses、pre-mortem、weighted-decision-matrix。若任务需要转向其中一项，先补齐该固定来源的完整资产；不要按名称编造正文或悄悄换成另一个作者的同名方法。
- 存在于当前选集中但未一起安装的相邻链接，也不能当作该次试用已经调用。按任务明确增加资产后再准备。

## 同名版本与证据

latticework/key-assumptions-check 与 structured/key-assumptions-check 是两个来源、两个原版。当前工具不支持同一 run 选入两个原名相同的 Skill；对照时分别创建 run，以相同材料和评价问题记录差异。

准备预览可用：

```sh
python3 scripts/assets.py prepare --project /absolute/project --harness codex --asset latticework/scqa-pyramid --task '用已有结论与证据整理面向指定读者的汇报结构'
```

DSH 可使用同一资产登记，但原生发现、调用及子 Agent 编排需要在可运行环境中另行验证。模板使用实际读者与任务，不写入某个试点的默认业务假设。

只保存必要结果和运行证据，结束后使用 cleanup。作者示例不是本人的真实试用记录，接入和文件校验不构成方法效果验证。
