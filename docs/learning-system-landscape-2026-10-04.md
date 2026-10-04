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
