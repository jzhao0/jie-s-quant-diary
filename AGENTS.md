# AGENTS.md — 简洁开发和研究

- 直接遵循已有的 [AI 辅助开发不过度工程化原则](docs/ai-assisted-development-principles-2026-10-16.md)，不要再复制成新的规则系统。
- 普通笔记、文本、图表、界面改动：直接修改并查看输出，不新增测试矩阵、夹具、探针、冒烟和状态治理文档。
- 金融研究、回测与交易复盘必须诚实保留数据来源、时间顺序和风险。不得触发真实交易、连接账户、修改其他量化仓库或虚构盈利。
- 有代码逻辑变更时用现有定向测试；仅在真实回归风险下新增测试。更新必要事实即可，勿反复重跑无关工具。

## Parallel development and CI discipline

- Feature development can proceed alongside independent code/performance review. Before incorporating a fix, inspect current branch/HEAD, local modifications and open PRs; a remote commit or Draft PR is not automatically present in a local checkout. Preserve other work: no unrequested reset, force-push, overwrite or automatic merge.
- Prefer focused local tests and run GitHub-hosted Actions only when meaningful for the change and current billing/runner conditions. A skipped or unrun workflow is never PASS; temporary manual CI is not a permanent ban.
- Keep this public repository's own licensing, privacy, security, publication and product requirements authoritative. Never import private cross-repository audit files or private user data into this repository. Do not add an orchestration or CI framework for routine changes.
