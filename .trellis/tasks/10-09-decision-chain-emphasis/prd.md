# 决策链默认入口与执行及时升级

Owner：本Marketplace源码checkout，目标分支`main`，基线`31c888edf1e72bbdc2b0a9769faee31c8cb34edb`。本有界PRD-only任务明确纳入根`10-09-agents-skills-layering-remediation`修订实施包，与Trellis`10-09-agents-effective-source-owner`互链；当前只创建规划记录。

修改`workflows/native/workflow.md`、`workflows/codex-subnode-channel/workflow.md`和`index.json`对应摘要/现有tests：非研究任务默认先筛选真正的user-owned取舍；先满足依赖，再按影响/阻断优先级逐轮提问，互相影响的问题分轮。树随答案演进，不要求一次穷举；空frontier但证据未完成不得封口。具体方法引用grill，仅维护项目入口、记录与阶段合同。明确研究、事实、局部实现和已定选择不造问题；普通继续复用已闭合链。

执行实质歧义立即报告问题/影响/推荐并暂停依赖；in_progress native replan后阻塞grill提问，planning按重新seal声明新版本。已授权同范围低风险增量守原短路径。维持原生身份/状态/批准/Channel与独立subnode派发门，不新增调度或另一状态机。

源与Trellis bundled合同对齐，更新index digest，运行既有Marketplace tests和依赖/研究/局部选择/执行升级正反例；先在main提交推送，再由Trellis固定gitlink、原生消费者刷新provenance。当前checkout detached，实施时安全转main并保留已有内容，不在旧独立checkout发新行为。

本repo没有task.py，不隐式初始化、伪造task/runtime或复制别的会话身份。按本明确PRD和列明审批包执行精确范围，清理本任务临时产物，返回commit/验证证据；当前不修改工作流产品源。
