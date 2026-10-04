# 学习系统接轨调研（Round 1）— 2026-10-04

> 临时归档。当前尚未建立独立 Learning System 仓库，本文件先放在公开日记仓库中，待正式立项后整体迁移。
>
> 本轮目标不是“挑一个最酷的学习 App”，而是识别：哪些现成项目可以直接作为基座、哪些适合作为模块、哪些只借鉴方法论/Schema/Skill 设计，最终服务于个人长期学习闭环。

## 1. 当前真实需求

需要统一承载：

- 大学课程：录音、自动转写、AI 纪要、人工笔记、PPT/PDF/DOCX、教材。
- 题库：选择、判断、填空、简答、计算、论述、匹配、排序等；支持 CSV/XLSX/JSON/GIFT/QTI/Moodle/XML 等多种来源。
- 错题与作答记录：题目、回答、正确率、耗时、置信度、错误类型。
- 长期知识：金融工程、量化、编程、科研、英语、考研、职业知识、生活技能等。
- 记忆：墨墨记忆卡作为主要“每日记忆执行器”。
- 掌握度：区分“老师讲没讲”与“我会不会”，不能把 coverage 和 mastery 混成一个状态。
- 可视化：课程进度、章节覆盖、知识掌握、错题复发、遗忘风险、考试大纲覆盖、预计完成时间。
- 自动化：现有“录音 → 自动转写”之后，继续自动进入 Web AI/Agent 分析，而不是手工上传。
- 可追溯：任何知识点、题目、卡片都能回指原始材料、时间戳、页码、图片及证据等级。

## 2. 核心设计原则

1. **墨墨不是总数据库。**  
   墨墨负责间隔记忆与每日复习；Learning Core 保存 Source / Knowledge Unit / Question / Attempt / Mastery / Plan。

2. **原始证据不丢。**  
   Transcript、PPT、截图、AI 纪要、人工笔记全部保留 provenance。自动总结只是二手材料。

3. **同时输出两份结果。**
   - 人可读：`lesson_report.md`，延续目前课程处理风格。
   - 机可读：`lesson_state.json`，供墨墨、题库、Dashboard、Planner 调用。

4. **Coverage 与 Mastery 分离。**
   - coverage: `not_taught / introduced / taught / advanced`
   - mastery: `untested / weak / partial / mastered / decaying`

5. **只有真实作答驱动掌握度。**  
   “AI 给出解释”不等于“已掌握”；必须经过练习/回忆/应用证据。

6. **外部项目优先做 Adapter，不轻易整仓重写。**

7. **高风险写操作有 Gate。**  
   墨墨删除、批量覆盖、题库大规模改写默认只 proposal / dry-run；先备份、后回读验证。

## 3. 当前候选技术栈

### P0：优先做 Spike / 可能直接成为平台基座

#### HKUDS/DeepTutor
Repo: https://github.com/HKUDS/DeepTutor

当前已具备相当完整的学习工作区：Knowledge Base、Reading、Question Bank、Quiz、Mastery Path、Daily Practice、Course Study、Books、Memory、任务板、多种解析器、MCP/Skills/CLI Apps、Codex 等 Agent 接入。

**本轮最重要的新判断：不要默认从零开发学习 Web App。先验证 DeepTutor 能否承担主平台。**

必须验证：
- 是否能监控/同步本地课程文件夹；
- 是否能保留逐字稿时间戳、页码、图片与自定义 evidence taxonomy；
- Question Bank / Practice / mistake tracking 的数据能否导出；
- Mastery Path 的 mastery 模型是否足够透明、可扩展；
- 是否能通过 Skill / MCP / CLI 增加 Markji Adapter；
- 是否能让外部 Agent 自动提交 lesson handoff，而不是只在 UI 中操作；
- 是否能接入自定义题库 Schema 和外部题库；
- 是否能把课程分析结果回写成结构化可复用状态。

**决策 Gate：**
如果以上关键项大多数 PASS，则优先“DeepTutor + 我们自己的 Learning Policy/Adapters”；否则再抽它的模块，避免自己重复造完整 UI/KB/Question Bank。

#### firecrawl/anydoc
Repo: https://github.com/firecrawl/anydoc

角色：混合 Office/文档格式的本地标准化入口。  
适合把 DOC/DOCX/PPT/PPTX/XLS/XLSX/ODT/ODS/RTF/EPUB/PDF/CSV 等统一转成结构化 Markdown/文档模型。

建议位置：

```text
raw file
  ↓
anydoc format detection + local conversion
  ↓
normalized doc + assets
```

#### firecrawl/pdf-inspector
Repo: https://github.com/firecrawl/pdf-inspector

角色：PDF 分类与路由。优先判断 text/scanned/image/mixed，再决定是否需要 OCR/视觉解析。  
目标是避免“所有 PDF 都直接上昂贵 OCR”。

建议：

```text
PDF
 ↓
pdf-inspector
 ├─ text → local extraction
 ├─ mixed → page/region selective OCR
 └─ scanned/image → MinerU/Docling/OCR fallback
```

### P0/P1：学习闭环与数据模型参考

#### quicklearn
Repo: https://github.com/artbyjazi/quicklearn

重点借鉴：
- lecture/audio/video/PDF/DOCX/PPTX/image/YouTube/article 等多源摄入；
- notes / flashcards / quizzes；
- FSRS；
- 每个产物保留 source segment IDs。

**尤其值得借鉴 provenance 设计。**

#### LearningOS
Repo: https://github.com/markmcnair/learningos

重点借鉴：
- FSRS-6 + BKT；
- prerequisite graph；
- mastery dashboard；
- “今天学什么”的最小工作面。

如果 DeepTutor 的 mastery 不满足要求，这里是优先的替代算法/数据模型来源。

#### StudyForge
Repo: https://github.com/Akhilvallala1/studyforge

重点借鉴：
- concept-level mastery；
- prerequisite；
- remedial practice；
- 不因“看过解释”就重置遗忘/失败历史。

#### OpenTutor
Repo: https://github.com/zijinz456/OpenTutor

重点借鉴：
- adaptive quiz；
- FSRS；
- knowledge graph；
- planner / analytics。

优先级低于 DeepTutor，但仍可作为结构/实现对照组。

#### AI_Study_Platform
Repo: https://github.com/ttang1024/AI_Study_Platform

重点借鉴：
- Exam Planner；
- Today/Smart Session；
- mistake notebook；
- mock exam；
- exam-oriented workload planning。

### P1：Agent 控制、长期自动化与治理

#### LoopX
候选 Repo: https://github.com/loopx-project/loopx

角色：长周期 Agent control plane / durable workspace。  
适合承载：

```text
watch transcript folder
→ create ingestion task
→ call Web AI / Agent
→ validate structured output
→ generate quiz/cards
→ Markji dry-run
→ human/policy gate
→ sync + receipt
```

最终是否直接采用，要与已有 UACP / Provider Control Plane / DeepSeek Harness 的能力重叠度对比。

#### SmartMoney-Cub / Harness pattern
候选 Repo: https://github.com/myc0576/hermes-smartmoney-cub

不把它当学习 App；借它的“证据包 / 决策记录 / replay / promotion gate”思想。

可迁移为：

```text
lesson evidence pack
→ processing plan
→ generated artifacts
→ attempt outcomes
→ mastery evaluation
→ candidate changes
→ gated promotion
```

目标：未来 AI 调整卡片、题库、知识状态时可追溯、可复现、可回滚。

#### Agent Reach
候选 Repo: https://github.com/Panniantong/Agent-Reach

角色：外部学习材料/社媒/视频/网页资源获取层。  
不是系统主数据库，只作为可选 source acquisition adapter。

### P1：Skill / 教育工作流设计

#### Hytidel AI 辅助教育工具箱
Repo: https://github.com/HytidelLegend/htd-ai-augmented-education

值得借鉴：
- Agent Skill 路由；
- `SOURCE_OF_TRUTH.md`；
- runtime / outputs / logs 分离；
- format-conversion-master；
- STT/TTS Skills；
- 敏感信息/提交前检查。

许可证 CC BY-NC 4.0：未来如果项目有商业化可能，优先借设计/调用方式，不直接复制受限内容。

#### Supervisor-Skills
Repo: https://github.com/HKUSTDial/Supervisor-Skills

研究模块参考：
- idea evaluator；
- deep research；
- paper writing/polish；
- figure reconstruction；
- research advisor workflow。

许可证含 NC/SA 约束，直接复制前必须审许可证兼容性。

#### 南京大学 Research Starter Kit
Repo: https://github.com/LAMDA-NeSy/Research-Starter-Kit

定位：科研课程/方法论内容包，不是软件基座。  
可转成未来“科研训练”Learning Pack：找论文、读论文、想 Idea、汇报、meeting、写作、rebuttal 等。

#### 倪海厦 Skill
候选 Repo: https://github.com/coinweth/nihaixia-skill

主要价值不是医学内容，而是“把一大块领域知识组织成可调用 Skill Pack”的方法：
- source/reference
- distilled cases
- modules
- style / reasoning contract

可迁移到：
- 计量经济学 Skill
- 金融工程 Skill
- 期货市场 Skill
- 考研科目 Skill
- 英语 Skill

医学内容本身如用于真实健康决策必须另行验证，不作为本项目可信知识源默认接入。

## 4. 内容库 / 外部学习资源

### ChinaTextbook
Repo: https://github.com/TapXWorld/ChinaTextbook

定位：教材资源候选，不是架构。  
注意版权与再分发边界；个人合法取得/有权使用的材料可作为 Source，不默认打包进我们自己的仓库。

### lilinji/English
定位：英语词汇/教材/词表/Anki 构建思路等资源候选。  
需进一步定位准确仓库并审查版权与数据来源。

### The Craft of Self-Teaching
Repo: https://github.com/xiaolai/the-craft-of-selfteaching

定位：元学习/自学方法论内容包，可做“Learning How to Learn”模块。

### 高性价比人生指南
候选：Giaoogle/howtolivebetter 等同类项目。

定位：生活技能/通识知识包的示例。  
说明系统不只服务学校课程：任何值得长期掌握的结构化知识都可以进入同一 Learning Core。

### knowledgefxg / Lorebeam / Oxford/OUP 资源
定位：外部英语材料发现与课程来源。  
不整体镜像，按需要选择内容进入 Source Library。

## 5. 英语专项：不应只做“背单词”

从用户提供的两条 X 帖子与 Parroto 等资源中，抽象出的英语闭环：

```text
选取可理解材料
→ 第一次盲听：主题 + 3 个要点
→ 第二次盲听：因果/态度/细节
→ 对照原文，标记“没听清 / 没听懂”
→ shadowing
→ retell
→ 场景迁移/商务表达
→ 评分与错误标签
→ 错误回流下一轮
→ 必要时生成墨墨卡（词块/表达/易错听辨）
```

参考：
- momoai_daily X 帖：听力 + ChatGPT + Obsidian 的闭环方法；
- AomyYing X 帖：商务英语场景化输出；
- parroto.app：dictation / shadowing / pronunciation / vocab SRS / mock test / progress；
- lilinji English：结构化词表/教材/卡片来源；
- knowledgefxg、Lorebeam/OUP：外部材料与分级测试。

### VibeVoice
候选 Repo: https://github.com/vibevoice-community/VibeVoice

TTS，不是 STT。  
P2 用途：
- 生成课程音频复盘；
- 英语 shadowing / 多角色对话；
- 长文 podcast 化。

录音转文字已有现成自动化，不需要用它替代 STT。

## 6. 可选高级模块

### MiroFish
Repo: https://github.com/666ghj/MiroFish

定位：多 Agent 场景推演/群体模拟。  
不是学习系统核心，但未来可以用于：
- 金融/政策 case simulation；
- 商务谈判；
- 决策与博弈；
- 历史/社会情景推演。

复杂度、成本和许可证都决定它只能是 P3 Optional。

### exercises-dataset
当前搜索结果主要是健身动作数据集，而非学术题库。

价值：作为“强 Schema 的外部领域数据集”例子；不作为当前题库基座。

## 7. 题库统一 Schema（暂定）

任何来源最终先归一化：

```text
Question
├─ id
├─ course
├─ chapter
├─ knowledge_unit_ids[]
├─ source_refs[]
├─ type
│  ├─ single_choice
│  ├─ multiple_choice
│  ├─ true_false
│  ├─ fill_blank
│  ├─ short_answer
│  ├─ calculation
│  ├─ matching
│  ├─ ordering
│  └─ essay
├─ stem
├─ options
├─ correct_answer
├─ explanation
├─ difficulty
├─ exam_source
├─ year
├─ tags
└─ misconception_targets[]
```

外部格式由 Adapter 负责：
CSV / XLSX / JSON / DOCX / GIFT / Moodle XML / QTI / Anki TSV 等。

## 8. Markji / 墨墨定位与 Adapter

墨墨 = **Memory Executor**，不是总数据库。

在用户开通会员/API 之前先完成 OFFLINE/MOCK：

- official Open API client skeleton；
- list decks / chapters / cards；
- create / update / move；
- delete 默认禁用或仅 propose；
- file upload；
- Markji syntax renderer + validator；
- TXT fallback；
- idempotency；
- backup；
- dry-run；
- write → read-back verification。

正式拿到 API key 后只做 TEST deck 验收，全部 PASS 后再接真实课程库。

## 9. 推荐的第一版整体架构

```text
                       Source Layer
  transcript / PPT / PDF / DOCX / book / question bank / web / notes
                             │
                             ▼
                     Ingestion Router
                anydoc + pdf-inspector
                 + OCR/parser fallback
                             │
                             ▼
                    Evidence / Provenance
                             │
                             ▼
                   Lesson / Knowledge Core
          Knowledge Unit / Relation / Misconception
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
          Question Bank    Markji Adapter   Dashboard
              │              │              │
              ▼              ▼              │
           Attempts       Daily Memory       │
              │                             │
              ▼                             │
            Mastery ────────────────────────┘
              │
              ▼
            Planner
              │
              ▼
        next lesson / quiz / review
```

平台层优先验证 DeepTutor 是否可以直接承担大部分 UI / KB / Question Bank / Daily Practice / Skills / MCP 功能。

## 10. DeepTutor Spike 验收表

正式开发前先做一个隔离测试工作区，用一节真实课程作为 benchmark。

必须测试：

- [ ] 放入“第一小节/第二小节”的 transcript + AI纪要 + note 能否稳定摄入
- [ ] 文档中的课堂 PPT 图片能否保留/被 vision 使用
- [ ] 时间戳、页码、source span 能否保留
- [ ] 能否实现 [A]/[B]/[C]/[D] evidence policy
- [ ] 能否输出当前风格的长 Lesson Report
- [ ] 同时输出 machine-readable Lesson State
- [ ] Question Bank 是否支持我们需要的题型和解释
- [ ] 实际作答能否保存 attempt / mistake
- [ ] mastery 是否可导出、可解释、可扩展
- [ ] daily practice 是否能按知识点薄弱程度重排
- [ ] 自定义 Skill / MCP / CLI 能否调用 Markji mock adapter
- [ ] 外部 Agent 能否自动提交 ingestion job
- [ ] 数据是否可备份/迁移，而不被某个 UI 锁死

若关键项 PASS：优先基于 DeepTutor 扩展。  
若关键项 FAIL：只抽组件，保留我们自己的 Learning Core。

## 11. 当前分类结论

### 直接优先试
- DeepTutor
- anydoc
- pdf-inspector

### 高价值抽象/模块参考
- quicklearn
- LearningOS
- StudyForge
- OpenTutor
- AI_Study_Platform
- LoopX
- SmartMoney-Cub pattern

### 外部 source / acquisition
- Agent Reach
- ChinaTextbook
- lilinji English
- knowledgefxg / Lorebeam / Oxford resources

### Skill / Curriculum Packs
- Hytidel AI Augmented Education
- Supervisor-Skills
- Nanjing Research Starter Kit
- The Craft of Self-Teaching
- 倪海厦 Skill（主要借 Skill Pack 结构）

### 可选增强
- VibeVoice
- Parroto
- MiroFish

## 12. 仍未完全定位/待补链接

以下名称目前不应凭猜测写死：

- AllnfraGuide（可能与 AI Infra / MLSys 指南有关，需要原链接）
- lorebeam.com/15532（本轮未可靠解析）
- lilinji.English 的准确仓库地址（需再次确认）
- smartmoney-cub-harness 的准确上游命名/仓库关系
- 用户后续补充的其他 GitHub / X / 网站

## 13. 下一步

1. 继续收集用户下一批候选链接。
2. 建 Candidate Matrix：功能、许可证、活跃度、接口、数据可迁移性、二开成本、和当前真实课堂 workflow 的匹配度。
3. 重点做 DeepTutor 技术 Spike，不先建自己的前端。
4. 同时把 Markji Adapter 在 mock/offline 模式下设计完整。
5. 选定独立仓库后，将本文件与后续调研从日记仓迁入正式 Learning System repo。


---

# Round 2 — 用户补充上游确认 + DeepTutor 代码级 Gate（2026-10-04）

## 14. 三个此前未锁定项目：现已确认

### 14.1 AIInfraGuide
Repo: https://github.com/caomaolufei/AIInfraGuide

**准确定位：AI Infra 系统学习内容库，不是学习平台。**

仓库目标是“从零开始深入理解 AI Infra 全栈”，当前明确覆盖：

- AI Infra 学习路线与知识图谱；
- Python/C++/数学/Transformer/PyTorch/GPU/NCCL 等前置；
- CUDA 与算子优化；
- 分布式训练；
- LLM 推理优化；
- Nsight / profiling；
- 180+ 场、60+ 家公司的面试真题。

**对 Learning System 的价值：**

将它作为未来 `AI-Infra Learning Pack`，导入：
- source hierarchy；
- prerequisite graph；
- interview question bank；
- practice / mastery / Markji candidate generation。

不是把仓库改造成我们的平台。

**许可证注意：** README 显示 MIT badge，但本轮通过 GitHub connector 未找到仓库根目录 `LICENSE` 文件。正式复制代码/内容前需要再次核验许可证文件与各文章/题目来源，不仅依赖 badge。

---

### 14.2 lilinji/English
Repo: https://github.com/lilinji/English

**准确定位：大规模结构化英语词表 / 课程资料资源库。**

README 当前描述约 960+ books，分层包括：

- 中小学教材；
- 中考 / 高考；
- 大学英语；
- CET-4 / CET-6；
- 专四 / 专八；
- **考研约 190 books**；
- 研究生 / 考博；
- IELTS / TOEFL / GRE / GMAT / SAT；
- BEC；
- 新概念英语；
- IT / 软件工程英语。

数据主要为 `.xlsx` / `.txt`，常见字段：
- Word
- Phonetic
- Definition
- Sentence（可选）

README 还提供 Anki/Quizlet/Eudic 的导入路径，并明确把词表定位为 spaced-repetition-ready 数据。

**对我们的价值：**

不是“安装一个英语 App”，而是把它接成：

```text
lilinji English
   ↓
English Source Adapter
   ↓
canonical Vocabulary / Phrase / Example schema
   ↓
去重 + 难度/考试标签 + 用户已有词汇状态
   ↓
墨墨 / dictation / listening / writing / exam question generation
```

尤其适用于：
- CET-4/6；
- 考研英语；
- 商务英语；
- IT/专业英语；
- 后续 IELTS/TOEFL（如需要）。

**版权/许可证 Gate：**

README 自称 Creative Commons / free & open source，但本轮 connector 未找到仓库根目录 `LICENSE` 文件。并且资源包含大量教材、词书、讲义衍生内容，不能因为仓库公开就默认所有素材都可再分发。

我们的规则：
- 可以作为“外部 Source 候选”研究；
- 用户个人学习场景可按实际授权/来源使用；
- 不默认把整库镜像进我们未来公开仓库；
- 公布/商业化前对具体 dataset 做权利核验；
- 我们自己的 canonical schema / adapter 与第三方内容分离。

---

### 14.3 SmartMoney-Cub / Hermes plugin
Core: https://github.com/myc0576/SmartMoney-Cub  
Hermes plugin: https://github.com/myc0576/hermes-smartmoney-cub

此前命名现已厘清：

- **SmartMoney-Cub** 的 README 标题就是 `smartmoney-cub-harness`，它是核心 harness；
- **hermes-smartmoney-cub** 是一个 Hermes Agent plugin，只封装本地 `smcub` CLI，不重写核心逻辑。

两者均有 MIT LICENSE。

核心设计链：

```text
External Agent / CLI
→ Run Envelope
→ frozen Evidence Pack
→ delayed outcome
→ deterministic replay
→ evaluation
→ challenger rules
→ explicit human promotion gate
```

Hermes wrapper 额外增加：
- `doctor`
- envelope validation
- evidence pack build
- replay
- evaluation
- capability protocol
- path confinement
- explicit read-only boundary

**迁移到学习系统的价值非常高。**

拟借鉴为：

```text
Lesson Run Envelope
→ Source/Evidence Pack
→ structured lesson_state
→ generated questions/cards
→ actual attempts
→ delayed mastery evidence
→ replay / evaluation
→ candidate knowledge/card/rule update
→ promotion gate
```

尤其适合解决：
- AI 后续“为什么改了这张卡？”
- 为什么把某知识点标成 weak/mastered？
- 为什么更新题库答案？
- 新课程是否应覆盖旧知识？
- 如何在模型升级后重新 replay 同一节课检查结果漂移？

**不复制金融逻辑，只复用 harness / audit / replay / governance 思路。**

---

## 15. DeepTutor：代码级初审结论

本轮已从 README 下沉到真实代码，包括：

- `deeptutor/learning/models.py`
- `deeptutor/learning/mastery.py`
- `deeptutor/learning/scheduler.py`
- `deeptutor/learning/assessment.py`
- `deeptutor/services/practice/*`
- `deeptutor/tools/question_bank.py`
- `deeptutor/api/routers/practice.py`
- `deeptutor/api/routers/question_notebook.py`
- `deeptutor/services/workspace/*`
- `deeptutor/reading/ingestion.py`
- `SKILL.md`
- CLI Apps / Skills / MCP 相关实现。

### 15.1 最重要的修正：DeepTutor 当前并不是 BKT/FSRS 学习内核

此前只根据功能描述容易误判。代码确认：

#### Mastery score
`deeptutor/learning/mastery.py` 当前是：

- 最近最多 5 次 attempt；
- 越新的 attempt 权重越大；
- 单次正确 mastery 最高 0.5；
- 两次最高 0.8；
- 3+ 次才允许到 1.0。

即：**recency-weighted accuracy + low-confidence cap**。

源码明确说明：
> intentionally simple and swappable

并且明确写着未来可以替换为 IRT/BKT。

#### Mastery Path retention
`deeptutor/learning/scheduler.py` 是可插拔 retention scheduler，但当前默认是指数遗忘/知识类型先验，**不是 fitted FSRS**。

#### Question Bank Daily Practice
`deeptutor/services/practice/scheduler.py` 明确写：
> SM-2-style cold-start policy, not a fitted FSRS model.

**结论：**
DeepTutor 的优点是“接口很适合换算法”，不是“它已经替我们做好 BKT/FSRS”。

因此仍保留：
- LearningOS / pyBKT 作为 mastery 候选；
- FSRS 官方实现作为 retention 候选。

---

### 15.2 DeepTutor 的真实数据模型比预期强

`Learning models` 已包含：

#### KnowledgePoint
- id
- name
- type: memory / concept / procedure / design
- module_id
- prerequisite_ids[]
- topic_source_ids[]

#### QuizAttempt
- question_id
- knowledge_point_id
- module_id
- is_correct
- user_answer
- error_type
- self_attribution
- mastery_estimate
- timestamp
- voided / void_reason

#### ErrorRecord
- error_type
- self_attribution
- AI confirmation
- retry history
- active / retrying / review / graduated

#### LearningEvidence
已经有我们很关心的：
- source
- assessment_type
- result: correct / incorrect / partial
- quality
- hints_used
- attempt_count
- confidence
- response_time
- session_id
- turn_id

#### ReviewTask
- due_at
- priority
- forgetting_risk
- reason
- evidence_source
- evidence_id

**判断：**
DeepTutor 的 attempt/evidence/mistake 基础结构可以大量复用；没有必要从零设计整套 attempt 日志。

---

### 15.3 Assessment 已经是跨学习 surface 的统一层

`deeptutor/learning/assessment.py` 明确把：

- Mastery Path
- Book Focus-Check
- Immersive Reading

统一写入同一个 assessment adapter。

`AssessmentRecord` 包含：

- origin_type / origin_ref
- question_id
- source
- assessment_type
- result
- question / question_type
- options
- user_answer / correct_answer
- explanation
- difficulty
- material_id / material_title
- section_id / section_title
- mastery_path_id / knowledge_point_id
- attempt_count
- hints_used
- confidence
- response_time
- quality
- attempt_id

并且每次 graded submission 会进入 immutable attempt log。

**这与我们的“题库作答 → 掌握度”主线高度兼容。**

---

### 15.4 Question Bank：核心能力可直接用，但格式还不够

DeepTutor Question Bank 的底层主要是 `notebook_entries`。

已确认能力：
- 回答过的 quiz 自动进入 Question Bank；
- wrong / uncategorized / bookmarked 等筛选；
- category/set；
- mistake tracking；
- explanation；
- difficulty；
- source/material/section；
- mastery_path / knowledge_point linkage；
- answer image；
- bulk organize；
- Practice queue；
- 7/30/90 day analytics。

#### 当前导入格式
代码明确支持：
- CSV
- TSV
- XLSX
- JSON

单次最多 500 题。

#### 当前题型
导入 parser 原生归一到：
- single_choice
- multi_choice
- true_false
- fill_blank
- short_answer

`essay/free_response` 当前也映射为 short_answer。

**缺口：**
我们的 canonical schema 仍应保留：
- calculation
- matching
- ordering
- essay（独立）
- possibly coding / derivation

并继续做：
- GIFT adapter
- Moodle XML adapter
- QTI adapter
- DOCX/PDF question extractor
- Anki TSV adapter

即：**DeepTutor Question Bank 做执行/UI，Canonical Question Schema 做总入口。**

---

### 15.5 Practice / 错题闭环：基本可直接用

Practice 已有：
- total / mistakes / due / overdue / reviewed_today；
- next_due_at；
- due queue；
- objective answer checking；
- again / hard / good / easy 类 rating；
- review history；
- lapse / streak / interval；
- optimistic-concurrency version；
- duplicate request idempotency；
- source analytics；
- mistake auto-capture；
- question 内容变更时 review state version 自动失效。

这比重新开发一个错题本成熟得多。

**但是：**
现有 Practice scheduler 主要是题目级 spaced review，不等于我们的“课程知识点 mastery planner”。

因此：

```text
DeepTutor Practice
= question-level review executor

Our Mastery/Planner policy
= concept-level learning decision layer
```

---

### 15.6 Provenance：已有基础，但不满足我们课堂证据标准

已有：
- KnowledgePoint.topic_source_ids[]
- Assessment material_id / section_id
- Reading source navigation
- PDF/page locator
- YouTube / Bilibili / audio transcript segments with start/end seconds
- source / origin_type / origin_ref

这意味着 DeepTutor 已经不是“无来源 RAG”。

但是我们真实课堂要求更细：

```text
[A] teacher explicitly said
[B] classroom material directly supports
[C] AI explanation
[D] unresolved / ASR conflict
```

并且希望 Knowledge Unit / card / question 能引用：
- source file
- page
- image
- transcript start/end timestamp
- exact source span
- evidence grade
- conflict status

当前 `topic_source_ids` 注释本身也明确说：
> curriculum provenance, not proof of factual correctness

**结论：PARTIAL。**
必须增加我们自己的 `EvidenceRef / SourceSpan` 层，而不是只用 topic_source_ids。

---

### 15.7 本地 Content Workspace：强，但“自动监控新逐字稿”尚不能当作已解决

代码确认：
- CLI 可 `deeptutor workspace set FOLDER`；
- 可以把任意允许目录注册为 content workspace；
- 自定义数据放在 workspace；
- outputs 独立；
- 有 workspace isolation / move / migration；
- KB 有 self-syncing 相关实现与近期 release。

但截至本轮代码搜索：

**尚未确认存在一个通用的 filesystem watcher，能够做到：**

```text
转写目录出现新文件
→ 自动识别这是一节新课
→ 自动创建 ingestion job
→ 自动等待同节课 AI纪要/笔记/PPT 到齐
→ 自动跑 lesson processor
```

因此这个要求仍交给：
- 我们已有 UACP / Provider Control Plane / DSH；
- 或 LoopX；
- 或一个极薄的 folder watcher。

DeepTutor 负责接收和管理结果，不应假设它自己完成课程目录自动编排。

---

### 15.8 外部 Agent 自动化：基础条件 PASS

`SKILL.md` 已确认 CLI 支持：

```bash
deeptutor run <capability> ... --format json
deeptutor kb create <name> --doc ...
deeptutor kb create <name> --docs-dir ...
deeptutor kb add ...
deeptutor chat ...
deeptutor workspace set ...
```

并支持：
- Skills；
- external skill hubs；
- CLI Apps；
- MCP services；
- Codex / provider integrations。

所以我们不必让自动化依赖浏览器点击。

可以设计：

```text
UACP / local watcher
→ deeptutor CLI/API
→ structured receipt
```

这是明显 PASS。

---

### 15.9 Markji Adapter：推荐作为独立 CLI + DeepTutor Skill/CLI-App 接入

比直接写死进 DeepTutor 核心更稳。

建议：

```text
markji-sync core
├─ official Open API
├─ syntax renderer/validator
├─ TXT fallback
├─ backup
├─ dry-run
├─ idempotency
└─ read-back verification

        ↑
DeepTutor CLI App / Skill
        ↑
Chat / Agent / UACP
```

DeepTutor CLI Apps 本身就是“管理员安装、Agent 以结构化 argv 调用”的模型，和 Markji Adapter 很匹配。

这样将来离开 DeepTutor：
- `markji-sync` 仍能被 Codex / DSH / ChatGPT / UACP 单独调用；
- 不产生平台锁定。

---

### 15.10 Mastery Path 的可调整性：PASS

代码里有：
- `mastery_build`
- `mastery_revise`
- outline / study / review modes
- prerequisite graph
- source relations

并且 prompt 明确要求：
**已有学习路线不要整张重建；只对错误知识点做最小 revise。**

这个原则和我们“课程持续增量维护”高度一致。

---

## 16. DeepTutor 第一轮 Gate 评分

| Gate | 当前判断 | 说明 |
|---|---|---|
| 本地工作区 | PASS | 可绑定真实 folder，数据本地持久化 |
| 自动监听新课程文件 | PARTIAL | 未确认通用 watcher / lesson assembly |
| PDF/Office/多媒体摄入 | PASS | 多解析器 + Reading + media ingest |
| 视频/音频 timestamp | PASS | transcript segment 有 start/end |
| 页码/材料导航 | PASS | Reading/source navigation 已有 |
| [A/B/C/D] 课堂证据等级 | FAIL/EXTEND | 需要自定义 EvidenceRef |
| 精确 source span → knowledge/card/question | PARTIAL | 基础 source/section 有，需细化 |
| Question Bank UI | PASS | 已成熟 |
| CSV/XLSX/JSON 题库导入 | PASS | 现成 |
| GIFT/QTI/Moodle/复杂题型 | FAIL/EXTEND | 继续做 Adapter |
| 错题/作答 immutable evidence | PASS | assessment + practice event |
| Question-level spaced review | PASS | SM-2-style |
| Concept mastery | PARTIAL | 当前算法简单，接口可替换 |
| BKT/FSRS | NOT PRESENT | 需要外接/替换 |
| Daily Practice | PASS | queue + analytics |
| 知识薄弱度驱动全局 Planner | PARTIAL | 需我们自己的 policy |
| Skill / CLI / MCP 扩展 | PASS | 架构已支持 |
| Markji 接入可行性 | PASS-IN-ARCH | 需实际做 adapter smoke |
| 外部 Agent 自动执行 | PASS | CLI/API 可作为 machine interface |
| 数据本地/可迁移性 | GOOD | SQLite + workspace；仍需正式 exporter |
| 现有真实课程一键跑通 | NOT TESTED | 下一阶段需要 live spike |

---

## 17. 当前架构判断更新

代码级审查后，不建议：

### A. 完全从零写一个学习平台
重复造轮子过多。

也不建议：

### B. 把 DeepTutor 当成唯一 Source of Truth
因为我们的课堂 evidence taxonomy、精确 provenance、Markji sync、长期 planner 有额外要求。

更合理的候选是：

```text
               DeepTutor
     UI / KB / Reading / Question Bank
     Practice / Chat / Skills / MCP
                    │
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
 Our Learning Extension     markji-sync
 EvidenceRef / LessonState   independent CLI
 Coverage / mastery policy   official API
 Planner adapters            TXT fallback
          │
          ▼
     UACP / local automation
```

是否采用“DeepTutor extension”还是“sidecar Learning Core”，留到真实 Spike 决定。

---

## 18. 下一项实际工作（仍不创建正式 Learning System repo）

### DeepTutor Real-Course Spike

使用已提供的真实 benchmark：
**期货市场｜第2周第1次课**

输入：

```text
第一小节_转写结果.docx
第一小节_AI纪要.docx
第一小节_笔记.docx
第二小节_转写结果.docx
第二小节_AI纪要.docx
第二小节_笔记.docx
+ 当前最终 Lesson Report
```

需要验证：

1. DeepTutor 原生摄入结果；
2. 图片/PPT page 5 是否可定位；
3. transcript timestamp 是否可追踪；
4. 是否能生成与当前人工流程同等级的 Lesson Report；
5. 是否能生成 LessonState JSON；
6. 10 道主动检验是否能进入 Question Bank；
7. 用户作答能否产生 attempt / mistake / practice state；
8. 能否把题目显式绑定到 knowledge point；
9. mastery 输出如何变化；
10. 自定义 EvidenceRef 扩展点在哪里；
11. Markji mock CLI 是否能作为 CLI App / Skill 被调用；
12. 所有结果能否导出并 replay。

在这个 Spike 之前：
**继续不建正式独立仓库，不进行真实 Markji API 写入。**



---

# Round 3 — DeepTutor Real-Course Parser Spike（真实课程，2026-10-04）

## 19. 实验环境

已在 Windows 设备上创建**隔离 spike**，没有改动现有项目：

```text
D:\Projects\_spikes\deeptutor-real-course-20261004
├─ source\        # HKUDS/DeepTutor shallow clone
├─ .venv\         # 独立 Python 3.13 环境
├─ source_audit.py
├─ probe_deeptutor_extract.py
├─ probe_images.py
└─ extract_probe.json
```

DeepTutor 源码安装已成功完成（Python 3.13.2，`uv pip install -e .`）。

真实课程目录：

```text
D:\文件\学校\大三上\期货市场\第二周第一节
├─ 第一小节_AI纪要.docx
├─ 第一小节_笔记.docx
├─ 第一小节_转写结果.docx
├─ 第二小节_AI纪要.docx
├─ 第二小节_笔记.docx
└─ 第二小节_转写结果.docx
```

未对原课程文件做任何写操作。

---

## 20. 真实源文件审计

### 第一小节

| 文件 | 体量 | 时间戳 | 内嵌图 |
|---|---:|---:|---:|
| 第一小节_转写结果.docx | ~9.9k extracted chars | 106 | 0 |
| 第一小节_AI纪要.docx | ~1.9k chars | 0 | 0 |
| 第一小节_笔记.docx | 仅标题 | 0 | 0 |

### 第二小节

| 文件 | 体量 | 时间戳 | 内嵌图 |
|---|---:|---:|---:|
| 第二小节_转写结果.docx | ~9.7k extracted chars | 104 | **1 JPEG** |
| 第二小节_AI纪要.docx | ~1.9k chars | 0 | 0 |
| 第二小节_笔记.docx | 仅标题 | 0 | 0 |

第二小节原始 DOCX 内确实包含：

```text
word/media/image1.jpeg
```

大小约 152,899 bytes。

---

## 21. DeepTutor 原生 DOCX extractor：真实结果

调用：

```python
deeptutor.utils.document_extractor.extract_text_from_path(...)
```

对六份真实文件全部成功，无需 LLM。

### 21.1 时间戳保留：PASS

DeepTutor 原生 text extraction 保留了逐字稿中的时间戳。

例如第二小节提取后仍可看到：

```text
说话人1 06:53
让我们观察中金所的结算制度图……

说话人1 07:09
……

说话人1 07:40
……
[图片 1: image-01.jpg]

说话人1 07:58
……
```

并保留 `08:17` 等后续时间戳。

**结论：**
我们不需要为了“逐字稿 timestamp”重写 DOCX parser。

---

### 21.2 DOCX 内嵌图片：PASS，而且不是只留占位符

DeepTutor 的 `document_images.extract_docx_rich()` 在真实第二小节中输出：

```text
images = 1
image-01.jpg
mime = image/jpeg
bytes = 152899
```

并在正文中保留固定 marker：

```text
[图片 1: image-01.jpg]
```

源码设计明确表明：
- image marker 留在 text reading order；
- raster bytes 单独作为 image attachment；
- vision-capable model 可接收真实图片；
- Reading surface 可将 marker 映射回 section locator。

**这个结果比 Round 2 的静态判断更好：课堂 PPT 截图并不会在 DeepTutor 中天然丢失。**

---

### 21.3 “图与讲解上下文”可以锚定：PASS（段落级）

真实提取结果中，中金所结算图 marker 位于以下语义区间：

```text
06:53 让我们观察中金所的结算制度图……
07:09 交易结算会员……
07:40 全面结算会员……
[图片 1: image-01.jpg]
07:58 因此……
```

说明我们能够构造：

```text
EvidenceRef
├─ file = 第二小节_转写结果.docx
├─ time_window ≈ 06:53–07:58
├─ embedded_image = image-01.jpg
├─ local paragraph anchor
└─ related concept = 中金所会员分级结算
```

这是实现“老师说图 + 图本身 + 时间戳”三者关联的关键基础。

---

## 22. 一个重要限制：DOCX 的“Page 5”不是原生文档语义

DOCX 本质不是固定分页格式。

DeepTutor 的 text/OOXML extraction 可以稳定保留：
- 段落顺序；
- 图片位置；
- 时间戳；
- 图片 bytes。

但不能仅靠 DOCX XML 稳定声称：

```text
这张图在 Word 第5页
```

DeepTutor 的**paged Office preview**需要系统存在 `soffice` / LibreOffice，把 Office 文档渲染为 PDF 再提供真实 page boundary。

本机本轮检查：

```text
soffice = NOT INSTALLED / NOT ON PATH
libreoffice = NOT INSTALLED / NOT ON PATH
```

所以当前 Spike 已确认的是：

```text
paragraph/timestamp/image provenance = PASS
Word rendered page number = BLOCKED_BY_SOFFICE
```

如果以后确实需要“Page 5”作为 provenance：
1. 可安装 LibreOffice / soffice；
2. 或者我们优先存 paragraph/source span，page 仅作为 presentation locator；
3. 不应把可变 Word pagination 当成唯一 canonical identity。

**推荐 canonical identity：**
`file + paragraph/span + timestamp + image id`  
Page number只做辅助 locator。

---

## 23. DeepTutor 对本节原始输入的保真度判断

| 输入信息 | 实测 |
|---|---|
| 中文正文 | PASS |
| DOCX 标题/段落 | PASS |
| transcript timestamp | PASS |
| AI纪要正文 | PASS |
| 空笔记识别 | PASS |
| embedded JPEG | PASS |
| image marker reading-order anchor | PASS |
| image bytes 可供 vision | PASS |
| Word 固定页码 | 当前 BLOCKED（无 soffice） |
| [A/B/C/D] evidence grade | 尚无，需要扩展 |
| ASR conflict graph | 尚无，需要 Lesson Processor |

因此“先把六个 DOCX 统一转 Markdown 再丢给 DeepTutor”并不是必须步骤。

DeepTutor 自己的 parser 已经能保留我们最关心的：
**text + timestamp + embedded image order**。

anydoc 仍有价值，但定位调整为：
- legacy Office / 更多异构格式；
- normalization fallback；
- 外部批处理；
而不是所有 DOCX 的强制前置层。

---

## 24. Real-Course Spike 当前 Gate 更新

| Gate | Round 2 | Round 3 实测 |
|---|---|---|
| 真实六文件可读取 | NOT TESTED | **PASS** |
| transcript timestamp | 静态 PASS | **PASS (live)** |
| embedded classroom image | 静态推测 | **PASS (live)** |
| image 与正文相对位置 | 未确认 | **PASS** |
| image bytes 可抽取 | 未确认 | **PASS** |
| DOCX page number | 未确认 | **BLOCKED / presentation-only** |
| 原生 Lesson Report 质量 | NOT TESTED | 待模型运行 |
| LessonState JSON | NOT TESTED | 待自定义 schema |
| Question Bank injection | NOT TESTED | 下一步 |
| Attempt/Mistake write | 代码 PASS | 下一步 live |
| Mastery linkage | 代码 PASS | 下一步 live |
| Markji mock CLI App | 未实现 | 后续 |

---

## 25. 下一步已收窄

接下来不再花时间证明“DeepTutor 能不能读这些 Word”。

已经证明能。

下一道真实 Gate 是：

### Gate A — Gold Baseline Lesson Processor

输入六文件，要求输出两份产物：

```text
lesson_report.md
lesson_state.json
```

其中 `lesson_report.md` 必须和现有 GPT Gold Baseline 对比：

- 知识覆盖；
- 老师强调信号；
- ASR 冲突；
- 中金所图；
- 期货交易所五大职能；
- 全员 vs 分级结算；
- 期货公司四类业务；
- 风险管理子公司；
- 课程债务；
- 主动检验题。

`lesson_state.json` 则必须正式引入：

```text
Source
SourceSpan
EvidenceRef
KnowledgeUnit
CoverageStatus
Question
Misconception
UnresolvedConflict
FlashcardCandidate
```

### Gate B — Question Bank live injection

把 Gold Baseline 的主动检验题转换成 DeepTutor 原生：
- CSV/JSON import；
- knowledge point linkage；
- source/material linkage；
- explanation；
- difficulty。

然后真实答题一次，验证：
`Attempt → Mistake → Practice → Mastery evidence`。

### Gate C — Markji mock bridge

先不使用真实 API key。
只验证 DeepTutor Skill/CLI App 能调用独立 `markji-sync --dry-run` 并返回 receipt。

---

## 26. 当前新的架构倾向

Real-Course parser Spike 之后，DeepTutor-based 路线的可行性进一步上升。

目前更倾向：

```text
DeepTutor = 学习工作台 + 原始学习执行层
     │
     ├─ Reading / KB / Files
     ├─ Question Bank
     ├─ Practice / Mistake
     ├─ Chat / Skills / MCP
     └─ basic Mastery Path

Our Extension = 课程严谨性 + 个性化策略层
     │
     ├─ Lesson Processor
     ├─ EvidenceRef / SourceSpan
     ├─ [A]/[B]/[C]/[D]
     ├─ ASR conflict handling
     ├─ Coverage != Mastery
     ├─ richer BKT/FSRS policy
     └─ global Planner

markji-sync = 独立 Memory Adapter

UACP / Web Agent Bridge = 自动化执行层
```

仍然不创建正式项目仓库，直到 Gate A/B 至少跑通。


---

# Round 4 — Question Bank / Practice / Linked Evidence Live Spike（2026-10-04）

## 27. Gold Baseline 10 道主动检验 → DeepTutor 导入：PASS

已把现有 GPT Gold Baseline 中的 10 道主动检验题映射为 DeepTutor 当前原生 Question schema，并生成：

```text
D:\Projects\_spikes\deeptutor-real-course-20261004\w2l1_questions.json
D:\Projects\_spikes\deeptutor-real-course-20261004\w2l1_questions_preview.json
```

调用：

```python
deeptutor.services.practice.importing.preview(...)
```

结果：

```text
questions = 10
errors = 0
```

说明现有这节课的主动检验可以无损落到 DeepTutor 当前支持的：
- true_false
- single_choice
- short_answer

本节暂时没有必须依赖 matching / ordering / calculation 专用题型的 blocker；基差计算目前可作为 short_answer 执行，但长期仍应增加 `calculation` 一等题型。

---

## 28. Question Bank 真实 SQLite 导入：PASS

使用隔离 DB：

```text
D:\Projects\_spikes\deeptutor-real-course-20261004\isolated_question_bank.sqlite
```

执行 DeepTutor 原生：

```python
PracticeStore.stage_import(...)
PracticeStore.commit_import(...)
```

第一次导入：

```json
{
  "created": 10,
  "duplicates": 0,
  "total": 10
}
```

完全相同题目第二次导入：

```json
{
  "created": 0,
  "duplicates": 10,
  "total": 10
}
```

**结论：题库文件重复导入的内容级幂等性真实 PASS。**

Question Bank 统计：

```json
{
  "total": 10,
  "wrong": 0,
  "unresolved": 0,
  "bookmarked": 0,
  "uncategorized": 0
}
```

Tags 自动形成 16 个 categories，例如：
- W2L1
- 中金所
- 会员分级
- 期货市场
- 交易所职能
- 基差
- 风险
- 履约风险
- 期货公司
- 保险+期货
- 风险管理

---

## 29. Practice 真实作答闭环：PASS

在上述真实隔离 Question Bank 中模拟两次实际作答：

### 错题

题：

> 某会员可以交易，也可以给自己的客户结算，但不能给其他交易会员结算。它最可能属于哪类？

正确答案：B（交易结算会员）  
模拟提交：A

DeepTutor 结果：

```json
{
  "correct": false,
  "rating": "again",
  "is_mistake": true,
  "review_count": 1,
  "lapses": 1,
  "streak": 0,
  "interval_days": 0.007,
  "mastered": false
}
```

### 正确题

题：

> 某机构自己不能在交易所做期货交易，但可以替非结算会员结算。它属于哪一类？

正确答案：D（特别结算会员）  
模拟提交：D

DeepTutor 结果：

```json
{
  "correct": true,
  "rating": "good",
  "is_mistake": false,
  "review_count": 1,
  "lapses": 0,
  "streak": 1,
  "interval_days": 3.0,
  "mastered": true
}
```

作答后 Practice summary：

```json
{
  "total": 10,
  "mistakes": 1,
  "due": 8,
  "reviewed_today": 2
}
```

并真实写入 `practice_review_events` 两条事件。

**因此：**
`Question → Answer → correctness → mistake state → next review interval → analytics`
已经可以直接复用 DeepTutor。

---

## 30. Cross-surface linked assessment → learning evidence：PASS

另建隔离：
- SQLite assessment DB
- LearningStore

创建真实知识点：

```text
path = futures-w2l1
module = clearing-members
kp = kp-clearing-member-types
name = 中金所结算会员分类与权限
type = concept
```

对同一道题记录：
1. 第一次回答错误；
2. 700 秒后第二次回答正确。

通过 DeepTutor 原生 `record_assessment()`，并显式给出：
- mastery_path_id
- knowledge_point_id

结果：

```text
immutable attempts = 2
learning evidence = 2
repetition_state.review_count = 2
repetition_state.lapse_count = 1
review_queue_count = 1
latest projection = correct
```

两次都返回：

```text
linked_retention_updated
```

并且 Question Notebook 的 latest projection 正确更新为第二次答案，而两次 attempt 均保留在 immutable attempt log。

**这验证了最关键的一条技术链：**

```text
一个题目
→ 显式 knowledge point linkage
→ immutable attempt
→ LearningEvidence
→ retention state
→ review queue
```

这部分不用我们重造。

---

## 31. 发现一个重要接口缺口：generic file import 会丢失 Knowledge linkage

虽然 DeepTutor 内部 `AssessmentRecord` 已支持：

- mastery_path_id
- knowledge_point_id
- material_id
- section_id
- confidence
- response_time
- quality

但是当前 `PracticeStore.commit_import()` 的通用 CSV/XLSX/JSON import 路径只把文件题写成：

```text
origin_type = external_import
origin_ref = practice-import
source = import
material_title = filename
material_id = import:<preview token>
result = ungraded
```

并**没有从导入 schema 接受/写入**：
- mastery_path_id
- knowledge_point_id
- source_refs / EvidenceRef
- canonical material_id / section_id

因此当前普通文件导入虽然能进题库、做题、生成错题，但不会天然更新对应知识点的 retention/mastery。

这是我们必须补的扩展点。

### 推荐方案

不要修改用户手工导入兼容路径的基本行为。

新增一个受控的 Learning Adapter，例如：

```text
CanonicalQuestion
    ↓
deeptutor-learning-import
    ↓
Assessment / Question Notebook
    + mastery_path_id
    + knowledge_point_id
    + material_id
    + section_id
    + EvidenceRef
```

即：

- 普通用户文件 → DeepTutor 原生 importer；
- 我们 Lesson Processor 生成的题 → rich importer / assessment adapter。

这样保留上游兼容性，也能实现完整掌握度闭环。

---

## 32. Windows 运行时发现的小缺口：tzdata 未被默认依赖带入

在 Windows Python 3.13 隔离安装后，首次调用：

```python
practice.overview("Asia/Shanghai")
```

报：

```text
ZoneInfoNotFoundError
No module named 'tzdata'
```

手动在隔离 venv 安装：

```text
tzdata
```

后：
- Asia/Shanghai 正常；
- Practice analytics 正常。

这不是我们的架构 blocker，但如果以后 Windows 本地部署 DeepTutor，需要在安装脚本/环境检查中显式处理。

建议我们的 bootstrap doctor 检查：

```text
ZoneInfo("Asia/Shanghai")
```

不通过则提示/安装 tzdata。

---

## 33. Gate B 当前结论

原 Gate B：

> Question Bank live injection + Attempt → Mistake → Practice → Mastery evidence

现在拆成：

| 子项 | 结果 |
|---|---|
| Gold 10题 → DeepTutor parser | **PASS** |
| 10题真实入 SQLite Question Bank | **PASS** |
| 重复导入幂等 | **PASS** |
| tags/categories | **PASS** |
| 实际正确/错误判定 | **PASS** |
| mistake capture | **PASS** |
| review event | **PASS** |
| adaptive next-review state | **PASS** |
| 真实 immutable assessment attempts | **PASS** |
| explicit KP linkage → LearningEvidence | **PASS** |
| linked evidence → retention/review queue | **PASS** |
| generic JSON import 自动 KP linkage | **FAIL / EXTEND** |
| imported question → concept mastery 自动更新 | **需要 rich importer** |

因此 Gate B 的底层可行性已基本成立，剩下的是我们的 Adapter，而不是 DeepTutor 核心能力缺失。

---

## 34. 当前优先级再次调整

现在不应该先做“自己的题库系统”。

DeepTutor 已经覆盖题库执行面。

我们的下一批开发重点应缩为：

1. `LessonState` canonical schema；
2. `EvidenceRef / SourceSpan`；
3. `CanonicalQuestion -> DeepTutor rich importer`；
4. `Coverage / Mastery policy`；
5. `markji-sync mock`；
6. 最后才是自动 watcher / UACP wiring。

下一道 Gate：**Gold Baseline LessonState fixture + schema**。


---

# Round 5 — Gold LessonState Schema + Rich Import Proof（2026-10-04）

## 35. LessonState v0.1 已建立并通过 JSON Schema

在隔离 spike 中建立：

```text
D:\Projects\_spikes\deeptutor-real-course-20261004\lesson_state_v0.1.schema.json
D:\Projects\_spikes\deeptutor-real-course-20261004\futures_w2l1_gold.lesson_state.json
```

Schema：

```text
learning.lesson-state.v0.1
```

当前核心实体：

```text
Lesson
Source
SourceSpan
EvidenceRef
KnowledgeUnit
Question
FlashcardCandidate
UnresolvedConflict
CourseDebt
```

并正式把两个状态拆开：

```text
coverage_status:
  not_taught / introduced / taught / advanced

mastery_status:
  untested / weak / partial / mastered / decaying
```

真实期货课 Gold fixture 当前包含：

```text
sources               6
evidence              10
knowledge_units       10
questions             10
flashcard_candidates   5
unresolved_conflicts   1
course_debts           3
```

`jsonschema.validate()`：

```text
PASS
```

这意味着我们后续不再让 Lesson Processor 输出任意结构的长 JSON，而是有了第一份可回归测试的机器合同。

---

## 36. EvidenceRef 已经能表达真实课堂需要

当前 v0.1 可以表示：

```text
evidence_id
source_id
grade = A/B/C/D
claim
span:
  start_time
  end_time
  paragraph_anchor
  page_locator
  image_id
notes
```

真实中金所例子已经编码为：

```text
source = 第二小节_转写结果.docx
time ≈ 06:53–08:17
image = image-01.jpg
grade = A
claim = 中金所会员分级图及三类结算会员权限是老师明确强调的重点
```

并另设：

```text
grade = D
ASR conflict
```

表示前段转写冲突。

因此：
**“老师强调 + 原始图 + 时间戳 + ASR冲突”已经可以在一个可验证机器模型里共同存在。**

---

## 37. Gold 10 题已显式绑定 KnowledgeUnit

不再只靠 tag 推测。

例如：

```text
gold-q4
→ ku-cffex-member-types
→ ev-cffex-diagram
```

基差题：

```text
gold-q7
→ ku-basis
→ ev-basis
```

保险+期货：

```text
gold-q10
→ ku-insurance-futures
→ ev-insurance-futures
```

这为：
- Question Bank；
- Attempt；
- Mastery；
- 错题分析；
- 墨墨卡生成；
- Planner

提供同一知识 ID。

---

## 38. DeepTutor 不需要新增后端才能做 Rich Import

进一步检查 DeepTutor 已有：

```text
POST /question-notebook/entries/upsert
```

对应 `UpsertEntryRequest` 原生已经接受：

- origin_type / origin_ref
- question_id
- question / type / options
- correct_answer / explanation / difficulty
- source
- material_id / material_title
- section_id / section_title
- mastery_path_id
- knowledge_point_id
- attempt_count
- hints_used
- confidence
- response_time
- quality

因此 Round 4 里说“需要新增 rich importer”现在可以进一步收窄：

> **不一定需要 fork DeepTutor backend；我们可以先做外部 Adapter，直接调用现有 rich upsert surface。**

---

## 39. Rich pre-population → same Question entry → Assessment → LearningEvidence：LIVE PASS

新建隔离 DB / LearningStore，先把 `gold-q4` 作为：

```text
origin_type = document_analysis
origin_ref = lesson:futures-w2l1:gold-questions
result = ungraded
material_id = futures-w2l1
mastery_path_id = futures-w2l1
knowledge_point_id = ku-cffex-member-types
```

预置到 Question Notebook。

随后对同一题提交错误答案 A。

真实结果：

```json
{
  "pre": {
    "id": 1,
    "result": "ungraded",
    "mastery_path_id": "futures-w2l1",
    "knowledge_point_id": "ku-cffex-member-types"
  },
  "assessment_outcome": {
    "entry_id": 1,
    "upserted": true,
    "attempt_recorded": true,
    "diagnostics": ["linked_retention_updated"]
  },
  "post": {
    "id": 1,
    "result": "incorrect",
    "user_answer": "A"
  },
  "same_entry_id": true,
  "learning_evidence": 1,
  "retention_review_count": 1
}
```

SQLite 直接检查也确认：

```text
assessment_attempts:
  attempt_id = rich-gold-q4-a1
  notebook_entry_id = 1
  origin_type = document_analysis
  question_id = gold-q4
  result = incorrect
  mastery_path_id = futures-w2l1
  knowledge_point_id = ku-cffex-member-types
```

因此完整目标链已经实证：

```text
LessonState
→ CanonicalQuestion
→ DeepTutor Question Notebook（预置、未答）
→ 用户真实回答
→ 同一 entry 更新
→ immutable assessment_attempt
→ LearningEvidence
→ retention state
```

这基本解决了“题库如何和掌握度真正接起来”的核心技术不确定性。

---

# Round 6 — Markji Offline/Mock Gate（2026-10-04）

## 40. 墨墨制卡语法已按当前已验证文档建立保守规则

参考：

- 墨墨开放 API：<https://open.maimemo.com/>
- AI 制卡语法指南：<https://tutuji333.github.io/markji-faq/questions/content/card-syntax-guide/>

当前语法合同采用“只生成已验证语法，不猜标签”的原则。

至少覆盖：

- 真实换行；
- 独占一行的 `---` 答案线；
- `[P#...#...]` 段落；
- `[T#...#...]` 文本；
- `[F#n#...]` 挖空；
- `[E##...]` KaTeX 公式；
- `[Choice##...]` 单选；
- `[Choice#multi#...]` 多选；
- `fixed` 固定选项顺序；
- `[Pic#ID/<file.id>#]`；
- `[Audio#ID/<file.id>#...]`；
- `[Card#ID/<root_id>#...]`；
- link URL 编码规则。

没有验证的标签/嵌套不生成。

---

## 41. Markji syntax validator 原型：SELFTEST PASS

本地 prototype 已实现保守 validator，并做反例测试。

能拦截：

```text
literal \n
HTML tags
unresolved <imageFileId> 等占位符
单选出现多个 *
多选只有一个 *
Choice 未闭合
裸 $...$ / $$...$$ 数学公式
缺少答案线（warning）
```

Self-test：

```text
valid_basic        PASS
literal_newline    detected
html               detected
unresolved_media   detected
bad_single         detected
bad_multi          detected
valid_formula      PASS

SELFTEST_PASS
```

---

## 42. 真实 Gold LessonState → Markji dry-run bundle：PASS

从：

```text
futures_w2l1_gold.lesson_state.json
```

当前生成：
- 5 张基础知识记忆卡；
- 2 张原生选择题卡；

合计：

```text
cards = 7
validation errors = 0
validation warnings = 0
```

每张卡生成：

```text
content_sha256
```

作为第一版 idempotency key。

这还不是最终所有卡片策略；它只是证明：
**LessonState → Markji syntax 可以完全离线验证，不需要先购买会员/API。**

---

## 43. markji-sync 已变成独立可执行 CLI prototype

位置：

```text
D:\Projects\_spikes\deeptutor-real-course-20261004\markji-sync-prototype
```

隔离 venv 中已经成功安装 console script：

```text
markji-sync.exe
```

当前命令：

```text
markji-sync doctor
markji-sync capabilities
markji-sync render-bundle --lesson-state ... --output ...
markji-sync sync --bundle ... --dry-run
```

### doctor

真实返回：

```json
{
  "schema": "markji.sync-doctor.v1",
  "version": "0.0.1",
  "status": "PASS_OFFLINE",
  "transport": "NOT_CONFIGURED",
  "api_called": false,
  "safety": "NO_REAL_WRITE_WITHOUT_EXPLICIT_TRANSPORT_AND_NON_DRY_RUN"
}
```

### capabilities

当前协议：

```text
markji.sync-capabilities.v1
protocol_version = 1
```

明确区分：
- doctor：无网络/无写入；
- render_bundle：仅本地产物；
- sync_dry_run：无远程写入；
- sync_real：网络 + 远程写，目前 disabled。

### dry-run

真实返回：

```json
{
  "schema": "markji.sync-receipt.v1",
  "status": "PASS",
  "mode": "dry-run",
  "api_called": false,
  "remote_writes": 0,
  "cards_planned": 7
}
```

并输出 7 个稳定 SHA-256 idempotency keys。

---

## 44. 为什么现在没有填真实 HTTP endpoint

本轮可以打开官方入口 <https://open.maimemo.com/>，但当前静态 Web 检索环境无法可靠展开其 JS OpenAPI 页面到每一个 method/path。

因此 prototype **刻意没有猜 endpoint**。

真实 transport 保持：

```text
NOT_CONFIGURED
```

这是正确的安全边界。

等用户开通会员拿到 API Key 后：
1. 读取/导出官方 OpenAPI 当前版本；
2. 把真实 method/path/schema 固化；
3. 先 read-only auth/list；
4. TEST deck；
5. create/read/update/delete smoke；
6. 再启用 `sync_real`。

在此之前不需要 API key，也不会造成真实墨墨写入。

---

## 45. 当前总判断

到这一轮为止，三个最核心的不确定性已经大幅降低：

### 课程材料能否自动结构化？
**底层解析 PASS，LessonState schema PASS；LLM Lesson Processor 尚待自动生成质量评测。**

### 题库能否和真实掌握度闭环？
**PASS。已经真实跑通 Question → Attempt → Mistake/Evidence → Retention。**

### 墨墨能否在买 API 前先把我们这一侧做完？
**PASS。Offline renderer / validator / dry-run CLI 已经可以工作。**

下一道最高价值 Gate：

> **用实际 LLM/Agent 从六份原始文件自动生成 LessonState，与 Gold fixture 做结构化差异评测。**

这将决定 Lesson Processor prompt / skill / multi-agent 是否达到当前人工 GPT 流程的质量。


---

# Round 7 — Benchmark 校准：Reference = GPT + 用户提示词（2026-10-04）

## 46. 纠正此前对 Gold Baseline 来源的表述

此前文档中有“人工 GPT 流程 / Gold Baseline”的说法，容易让后续 AI 误解为人工手工整理。

正确来源是：

```text
用户提供课程资料
→ 用户给 GPT 固定/长期使用的课程处理提示词
→ GPT 生成结构化课程结果
```

因此 Reference 的准确名称改为：

```text
GPT Prompted Reference Output
```

而不是“人工整理真值”。

原始课堂资料仍然是事实真值层；GPT 输出只是当前用户已经认可的质量与交互基准。

---

## 47. Benchmark 现在采用四层优先级

```text
1. Raw classroom sources
2. Prompt Contract
3. GPT Prompted Reference Output
4. Candidate pipeline output
```

含义：

- 原始转写 / 图 / 笔记决定“事实是否成立”；
- 用户提示词决定“应该如何组织、标注、提问和维护长期知识状态”；
- GPT Reference 用来衡量当前已认可的输出深度、结构和体验；
- DeepTutor / Lesson Processor 候选输出与前三者比较。

因此：

> 不允许为了“更像 GPT Reference”而复制 GPT Reference 中可能存在的错误。

---

## 48. 已建立 Reference Prompt Contract v1

当前没有找到最初提示词的逐字原文，因此没有伪称恢复原 prompt。

已依据：
- 当前 GPT Reference 的稳定结构；
- 已知长期课程处理要求；
- [A]/[B]/[C]/[D] 证据规则；
- 主动检验；
- 课程债务；
- OBS 摘要；
- 长期知识树；

建立**规范合同**：

```text
Course Processing Reference Prompt Contract v1
```

核心要求包括：

- 原始课堂录音 > 转写+图文 > 用户笔记 > AI纪要；
- 转写不能无条件当老师逐字原话；
- A/B/C/D 证据标签；
- 按真实授课顺序重建；
- 公式、图像、强调、考试信号必须处理；
- 冲突不允许静默合并；
- Coverage != Mastery；
- 主动检验不能只有选择题；
- 维护课程债务；
- 输出 OBS 摘要；
- 更新长期知识树。

注意：

> 这份 Prompt Contract 是“重建的规范”，不是声称逐字恢复用户原始提示词。

如果后续找到原提示词，应直接用原提示词替换该 Contract。

---

## 49. deterministic benchmark 已建立

隔离目录：

```text
D:\Projects\_spikes\deeptutor-real-course-20261004\benchmark
```

Reference GPT Output 已完整保存：

```text
reference_gpt_output.md
1859 lines
```

Benchmark 维度：

```text
15 结构
30 核心知识覆盖
15 证据纪律
15 考试信号 / 冲突 / 课程债务
10 主动检验
 5 OBS + 长期知识树
10 LessonState 机器状态
----------------
100
```

把现有 GPT Prompted Reference 自己跑回 benchmark：

```text
score = 100 / 100
```

用于校准测试器本身。

这不是证明 Reference“事实 100% 正确”，而是证明 benchmark 能识别当前 Reference 所体现的全部规范要求。

---

## 50. 下一步评价标准

候选 Lesson Processor 的输出将不再用模糊的“感觉像不像以前 GPT”。

而是：

```text
>=95  Reference-level structure/source coverage
85-94 strong candidate，人工检查漏项
70-84 有用，但不能替代当前 GPT + prompt 工作流
<70    暂不能接管
```

此外还有独立 factuality gate：

- 每个 A/B 结论必须可回指 Raw Source；
- C 必须明确是补充解释；
- D 不允许被自动“修正掉”；
- 不允许 candidate 因为知道金融知识而覆盖老师课堂口径。

下一步继续跑：

> **同样六份原始文件 → 自动 Lesson Processor → benchmark + raw-source factuality audit。**


---

# Round 8 — Prompt provenance correction + ingestion watcher prototype（2026-10-04）

## 51. 关于“原始期货市场 Prompt”的严格状态

已再次搜索：
- 个人历史上下文；
- 当前会话文件；
- Library。

可以确认历史记录里**确实存在**一份以：

```text
你现在是我的“期货市场”课程专项 AI。
```

开头的原始 prompt，而且历史索引确认它包含：
- 四类课堂文件；
- 资料证据优先级；
- [A]/[B]/[C]/[D]；
- 12部分输出结构；
- 主动检验；
- 课程债务；
- OBS 摘要；
- 长期知识树；
- 后续上传材料处理规则。

但是当前可用检索结果只返回了**索引级摘要**，没有返回该 prompt 的完整逐字正文。

因此，上一轮“已经找到原始完整 Prompt”的表述需要严格修正为：

> 已确认原 Prompt 的存在、开头和结构，但目前没有取得完整逐字正文。

当前 `Prompt Contract v1` 继续作为**可执行规范合同**使用，但不得标注为 verbatim original。

如果以后历史聊天或文件检索返回原文全文，应：
1. 原文全文保存为 immutable reference；
2. Prompt Contract 改成派生规范；
3. benchmark 记录二者 SHA-256 与版本关系。

---

## 52. 六份真实课程源文件已做 deterministic normalization

隔离输出：

```text
D:\Projects\_spikes\deeptutor-real-course-20261004\normalized_sources
```

包含六份 Markdown normalization 和 `manifest.json`。

每份 source 都记录：
- 原始 DOCX SHA-256；
- normalized text SHA-256；
- chars；
- lines。

目的：
- 模型升级后可 replay；
- Parser 改动后可发现 normalization drift；
- 不需要每次重新猜“是不是同一份输入”。

---

## 53. 课程目录 watcher prototype：LIVE PASS

新建：

```text
D:\Projects\_spikes\deeptutor-real-course-20261004\automation\watch_lesson_bundle.py
```

当前针对真实：

```text
D:\文件\学校\大三上\期货市场\第二周第一节
```

自动检查：

```text
第一小节
  转写结果
  AI纪要
  笔记

第二小节
  转写结果
  AI纪要
  笔记
```

六份齐全后生成：

```text
learning.ingestion-job.v1
```

真实第一次运行：

```json
{
  "status": "PASS",
  "action": "JOB_CREATED",
  "lesson_key": "期货市场/第二周第一节",
  "job_id": "job-edec02749d5be164",
  "source_count": 6,
  "next_state": "READY_FOR_AI",
  "remote_writes": 0
}
```

完全相同输入第二次运行：

```json
{
  "status": "PASS",
  "action": "SKIP_UNCHANGED"
}
```

因此 watcher 的第一版幂等性成立。

---

## 54. Ingestion Job 已经把“自动转写之后”那个人工断点正式表示出来

当前 job：

```text
READY_FOR_AI
```

并显式携带：
- course / lesson；
- 六个 source path；
- 每个 source SHA-256；
- lesson fingerprint；
- benchmark path；
- LessonState schema；
- reference output；
- required outputs；
- next_action = external_web_ai_processor。

也就是说现在已经把原来：

```text
自动转写
→ 用户手工上传 GPT
```

改造成了机器可执行边界：

```text
自动转写
→ watcher
→ ingestion job
→ external_web_ai_processor
```

当前没有调用外部 Web AI，也没有远程写入。

---

## 55. 下一步对接点

下一步不再继续扩写 watcher，而是把已有的本地 Web AI / UACP 项目接到：

```text
learning.ingestion-job.v1
```

它只需要完成：

```text
READY_FOR_AI
→ 上传/发送六份 source
→ 使用 Course Prompt Contract
→ 取得 GPT 输出
→ 保存 lesson_report.md
→ 生成 lesson_state.json
→ benchmark
→ factuality audit
→ ACCEPT / REPAIR
```

这样课程自动化项目和 Learning System 不耦合具体浏览器实现。

换 Web GPT / API / 本地模型时，job contract 不变。


---

# Round 9 — 原始 Prompt 正式归档 + Amendment 生效 + Watcher Prompt-aware（2026-10-04）

## 56. 原始「期货市场」Prompt 已取得完整逐字原文

本轮用户直接提供了完整原始 Prompt，因此此前“只确认存在、尚未取得逐字正文”的状态已经解除。

正式本地归档：

```text
D:\Projects\_spikes\deeptutor-real-course-20261004\prompts\futures_market_original_prompt_v1.txt
```

原始 Prompt SHA-256：

```text
9841b07d4ed278d409f7b632fc1f66917e3e27357087e5e2030020747f1ca8d1
```

它现在正式成为期货市场课程处理规则的 Source of Truth。

此前重建的 Prompt Contract v1 仅保留为：
- benchmark 辅助规范；
- 可机器检查的派生合同；

不得再替代原 Prompt 本身。

---

## 57. 后续修正已单独版本化

用户后续明确修正两点：

1. OBS 复盘模块必须给可直接复制的复制块；
2. 文件收齐后直接开始分析，不再等“本节文件上传完毕，开始处理”。

已单独归档：

```text
futures_market_amendment_v2.txt
```

SHA-256：

```text
a0447d82a12483b8d6bd6584c3c95c9afa95b8e78cc2a3f0913a5f185df53759
```

优先级：

```text
amendment_v2 > original_v1
```

该 amendment 只覆盖旧的“等待人工确认”规则，其余证据优先级、课程输出结构、长期维护规则继续有效。

---

## 58. Effective Prompt v2 已冻结

合并：

```text
original_v1 + amendment_v2
```

得到：

```text
futures_market_effective_prompt_v2.txt
```

SHA-256：

```text
b60ff4e1ae80554cae487c754629156076cc0c9909226497a151dd67e128d337
```

并建立：

```text
prompt_manifest.json
schema = learning.prompt-manifest.v1
```

机器规则明确为：

```json
{
  "auto_start_when_expected_bundle_complete": true,
  "wait_for_manual_confirmation": false,
  "obs_summary_copy_block_required": true
}
```

---

## 59. Watcher 现在对 Prompt 版本敏感

此前 lesson fingerprint 只包含课程源文件 hash。

现在改为：

```text
fingerprint =
hash(
  source paths + source SHA-256
  + effective prompt SHA-256
)
```

意义：

如果课程文件完全不变，但课程提示词发生修改：

```text
旧行为：SKIP_UNCHANGED  ❌
新行为：JOB_CREATED      ✅
```

这样 Prompt 变化会自动触发新的处理任务，不会继续复用旧分析结果。

---

## 60. Prompt-aware watcher live test：PASS

使用同一组六份期货市场文件。

由于加入了 Effective Prompt v2，生成新的 job：

```text
job-b56f9c2e30fc4de9
```

Receipt：

```json
{
  "status": "PASS",
  "action": "JOB_CREATED",
  "lesson_key": "期货市场/第二周第一节",
  "source_count": 6,
  "prompt_sha256": "b60ff4e1ae80554cae487c754629156076cc0c9909226497a151dd67e128d337",
  "next_state": "READY_FOR_AI",
  "manual_confirmation_required": false,
  "remote_writes": 0
}
```

第二次运行同一输入：

```text
SKIP_UNCHANGED
```

因此：

- source-sensitive idempotency：PASS
- prompt-sensitive idempotency：PASS
- auto-start semantics：PASS

---

## 61. 现在 Course Ingestion Contract 的正式状态

```text
课堂文件完整
    ↓
Watcher
    ↓
source + prompt fingerprint
    ↓
learning.ingestion-job.v1
    ↓
manual_confirmation_required = false
    ↓
READY_FOR_AI
    ↓
Web GPT / Agent Processor
```

从这一轮开始，后续期货市场自动化不再依赖人工发送启动口令。


---

# Round 10 — UACP/Web-GPT integration gate check（2026-10-04）

## 62. Decision: DEFER Web-GPT auto-upload integration for now

Inspected current local repository:

```text
D:\Projects\universal-agent-control-plane
branch = feat/issue9-dot-opendots-poc-plan-20261003
HEAD   = 9510080064a4dff0f3388dc9985dc496a113202e
```

Current UACP evidence says:

- Browser Bridge fresh-chat text E2E: PASS.
- exact bound ChatGPT tab / exactly-one-send / response archive: PASS.
- Browser Bridge **automatic ChatGPT file attachment**: not accepted as production capability.
- current PROJECT_STATE explicitly says `production attachment: NOT REACHED`.
- historical docs also explicitly deferred automatic file attachment until text transport was proven.
- OpenDots current accepted path is read-only; computer/browser/files/shell are OFF.

A different path, AA/DSH, **does** have real live attachment acceptance:

```text
Windows input bundle
→ Agents Anywhere
→ Mac connector
→ DSH
→ model
= LIVE E2E PASS
```

including multi-provider PaperWB worker/reviewer/controller acceptance.

However, that is not the same requirement as:

```text
local lesson bundle
→ logged-in ChatGPT Web conversation
→ upload DOCX/images
→ run the user's course prompt
→ collect GPT Web output
```

Therefore do **not** wire Learning System ingestion jobs into UACP Browser Bridge yet.

### Current boundary

Keep:

```text
learning.ingestion-job.v1
state = READY_FOR_AI
```

as the stable handoff boundary.

Do not implement a temporary brittle uploader merely for this project.

When UACP later exposes an accepted ChatGPT Web attachment transport, the learning pipeline can attach at this boundary without changing LessonState, DeepTutor, benchmark, or Markji layers.

### What can be reused now

The following UACP patterns are already mature enough to borrow later:
- durable JobStore;
- short-call status/collect;
- attachment manifest + SHA-256 pattern;
- bounded input bundle;
- provider result receipt;
- reviewer/controller gate;
- UTF-8 boundary hardening;
- idempotent/replayable task state.

For now, Learning System proceeds independently of Web-GPT transport.
