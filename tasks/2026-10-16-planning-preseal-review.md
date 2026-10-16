# 规划封口前复核与合并推进确认

落实根任务 planning-preseal-review 已展示并获用户明确批准的 Marketplace 范围：同步 native、codex-subnode-channel、channel-driven-subagent-dispatch、tdd 的最终方案展示、合并授权、原生 seal/approve/start 顺序及重规划提示。保留各变体职责，更新 index 摘要，运行现有检查；先提交推送 origin/main，再由 Trellis 固定 gitlink。验证与完成回执追加本文件。

源码修订与检查已完成：`python3 -m unittest discover -s tests -v` 8 项通过，index 对四个工作流的 SHA-256 均匹配；native 与 Trellis 默认源模板字节一致，`git diff --check` 通过。后续消费者来源与物化验收由根任务记录。
