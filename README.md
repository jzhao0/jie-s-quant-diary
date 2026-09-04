# jie's quant diary

个人项目记载

## 📁 项目结构

```
jie's quant diary/
├── data/                  # 数据文件 (.gitignore 忽略)
├── notebooks/             # JupyterLab 学习笔记
│   └── YYYYMMDD_*.ipynb   # 按日期命名
├── scripts/               # 可复用脚本
│   └── finance_utils.py   # 金融工具函数
├── tests/                 # 测试文件
├── docs/                  # 文档
├── .gitignore             # Git 忽略规则
└── README.md              # 项目说明
```

## 🚀 快速开始

### 环境激活
```bash
conda activate quant
```

### 启动 JupyterLab
```bash
jupyter lab
```

## 📝 每日提交规范

1. **Notebook 命名**: `YYYYMMDD_主题.ipynb`
   - 示例: `20260701_pandas金融数据清洗实践.ipynb`

2. **提交信息格式**:
   ```
   [日期] 具体改动 + 业务价值
   示例: "[20260701] 实现月度波动率手算逻辑，修复复权价格计算"
   ```

3. **提交内容**:
   - 学习笔记 (notebooks/)
   - 可复用函数 (scripts/)
   - 测试用例 (tests/)

## 🧭 研究与工程 Idea Bank

- [Research & Patent Idea Bank](docs/research-and-patent-idea-bank.md) — 跨金融、经济、数学、统计、计算机的专利筛选与可开发技术想法库。
- 仓库为公开仓库：尚未申请的专利候选只记录非使能级概要，完整技术方案在申请前不公开。

## 🔧 环境信息

- **设备**: MacBook Air M1 (16GB+1TB)
- **架构**: ARM64 (Apple Silicon)
- **Python**: 3.10 (Miniforge)
- **核心库**: NumPy, Pandas, Matplotlib, AKShare, Tushare, TA-Lib

## 📚 学习资源

- [AKShare 文档](https://www.akshare.xyz/)
- [Tushare 接口](https://tushare.pro/)
- [Pandas 金融分析](https://pandas.pydata.org/)
