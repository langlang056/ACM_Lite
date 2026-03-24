# ACM Trainer -- 本地轻量刷题平台

本地 Web 刷题平台，支持题目管理、在线编码、自动判题、每日一题和做题统计。纯 Python + Flask 实现，零外部服务依赖。

---

## 快速开始

### 环境要求

- Python 3.8+
- pip

### 安装与启动

```bash
cd acm_trainer
pip install flask
python app.py            # 默认端口 8080
python app.py -p 9000    # 指定端口
```

启动后访问 `http://localhost:8080`。首次启动自动建库并导入 21 道内置题目，后续启动会增量补充新题。

---

## 项目结构

```
acm_trainer/
├── app.py            # Flask 主程序，全部 API 路由
├── database.py       # SQLite 数据层，表定义与 CRUD
├── judge.py          # 判题引擎，subprocess 隔离执行 + 输出比对
├── daily.py          # 每日一题，四级优先策略智能选题
├── seed_data.py      # 内置题目数据（21 题），启动时增量插入
├── data/
│   └── acm_trainer.db    # SQLite 数据库（自动生成）
├── static/
│   ├── css/style.css
│   └── js/app.js         # 前端单页应用逻辑
├── templates/
│   └── index.html        # 主页面（Tailwind + Monaco Editor）
└── problems/             # 预留目录
```

### 模块说明

- **app.py** -- Flask 后端，包含题目、测试用例、判题、每日一题、统计、导入导出等 API。
- **database.py** -- SQLite 单文件数据库，4 张表（problems / test_cases / submissions / daily_problems），支持自动迁移。如果项目目录不可写会自动回退到 `~/.acm_trainer/`。
- **judge.py** -- 将用户代码写入临时文件，通过 subprocess 隔离运行，逐用例比对输出。支持 ACM 和核心代码两种模式。
- **daily.py** -- 按薄弱题优先 > 遗忘复习 > 新题探索 > 随机兜底的四级策略选题，自动去重近 30 天推荐。
- **seed_data.py** -- 21 道内置题，涵盖数组、链表、树、DP、贪心、设计等题型。每道题包含 ACM 模板、核心代码模板、适配器和输入格式模板。

---

## 功能说明

### 题库管理

创建、编辑、删除题目。每道题支持：标题、Markdown 描述、难度（Easy/Medium/Hard）、标签、来源、原题链接、ACM 代码模板、核心代码模板及适配器。支持 JSON 格式的导入导出。

### 做题模式

在做题页面的编辑器工具栏可切换两种模式：

| 模式 | 说明 |
|------|------|
| ACM | 用户自己处理标准输入输出 |
| 核心代码 | 只需实现函数/类，系统自动处理 I/O |

- 核心代码模式下，系统将用户代码与适配器拼接后执行，测试用例共享
- 核心代码模式下，测试用例输入会按格式模板转为可读的参数形式（如 `nums = [1, 2, 3]`）
- 切换模式时自动保存/恢复代码

### 判题状态

| 状态 | 含义 |
|------|------|
| Accepted | 全部用例通过 |
| Wrong Answer | 输出不匹配 |
| Time Limit Exceeded | 超时（默认 5 秒） |
| Runtime Error | 运行报错 |

### 每日一题

每天自动推荐一道题，优先级：做错 >=2 次 > 超过 7 天未复习 > 未做过 > 随机。支持手动换题。

### 快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl + Enter | 运行代码 |
| Ctrl + Shift + Enter | 提交代码 |

---

## 内置题目

| # | 题目 | 难度 | 来源 |
|---|------|------|------|
| 1 | 两数之和 | Easy | LeetCode #1 |
| 2 | 最长递增子序列 | Medium | LeetCode #300 |
| 3 | 接雨水 | Hard | LeetCode #42 |
| 4 | 合并区间 | Medium | LeetCode #56 |
| 5 | 岛屿数量 | Medium | LeetCode #200 |
| 6 | 移掉K位数字 | Medium | LeetCode #402 |
| 7 | 累加数 | Medium | LeetCode #306 |
| 8 | 目标和 | Medium | LeetCode #494 |
| 9 | 分隔链表 | Medium | LeetCode #86 |
| 10 | 分隔链表为k部分 | Medium | LeetCode #725 |
| 11 | 小于n的最大数 | Medium | 面试高频 |
| 12 | 恰好有n个因子的最小正整数 | Medium | 面试高频 |
| 13 | 两两交换链表中的节点 | Medium | LeetCode #24 |
| 14 | 二叉树的最近公共祖先 | Medium | LeetCode #236 |
| 15 | 二叉树的最大宽度 | Medium | LeetCode #662 |
| 16 | 字典序的第K小数字 | Hard | LeetCode #440 |
| 17 | 序列切分使两部分方差和最大 | Medium | 面试高频 |
| 18 | LRU 缓存 | Medium | LeetCode #146 |
| 19 | 实现前缀树 | Medium | LeetCode #208 |
| 20 | 寻找峰值 | Medium | LeetCode #162 |
| 21 | 最长连续序列 | Medium | LeetCode #128 |

---

## API 概览

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/problems` | 题目列表（支持 difficulty/tag/keyword 筛选） |
| POST | `/api/problems` | 创建题目 |
| GET/PUT/DELETE | `/api/problems/<id>` | 单题操作 |
| GET/POST | `/api/problems/<id>/testcases` | 测试用例 |
| PUT/DELETE | `/api/testcases/<id>` | 单个用例操作 |
| POST | `/api/submit/<id>` | 提交判题（保存记录） |
| POST | `/api/run/<id>` | 调试运行（不保存） |
| GET | `/api/submissions` | 提交历史 |
| GET | `/api/daily` | 今日一题 |
| POST | `/api/daily/refresh` | 换一题 |
| GET | `/api/stats` | 统计数据 |
| GET/POST | `/api/export` / `/api/import` | 导入导出 |

---

## 常见问题

**数据库在哪里？** 默认 `data/acm_trainer.db`，不可写时回退到 `~/.acm_trainer/acm_trainer.db`。

**如何重置？** 删除 `data/acm_trainer.db` 后重启即可。

**支持什么语言？** 当前仅支持 Python。

**如何备份？** 复制 db 文件，或使用页面底部的「导出题库」功能。

---

## 技术栈

| 组件 | 技术 |
|------|------|
| 后端 | Python + Flask |
| 数据库 | SQLite |
| 前端 | HTML/CSS/JS 单页应用 |
| 编辑器 | Monaco Editor |
| 样式 | Tailwind CSS |
| Markdown | Marked.js |
