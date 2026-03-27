# ACM Lite -- 本地轻量刷题平台

本地 Web 刷题平台，支持题目管理、在线编码、自动判题、每日一题和做题统计。纯 Python + Flask，零外部服务依赖。

---

## 快速开始

```bash
# 环境要求: Python 3.8+
pip install flask
python app.py              # 默认 8080 端口
python app.py -p 9000      # 自定义端口
```

启动后访问 `http://localhost:8080`。首次启动自动建库并导入 32 道内置题目（22 道 LeetCode 经典题 + 10 道阿里巴巴笔试真题）。

---

## 项目架构

```
acm_trainer/
├── app.py                          # Flask 入口，注册 Blueprint
├── backend/                        # 后端逻辑
│   ├── database.py                 #   数据层，SQLite 表定义 + CRUD
│   ├── judge.py                    #   判题引擎，subprocess 隔离执行
│   ├── daily.py                    #   每日一题，四级优先策略选题
│   ├── seed_data.py                #   种子数据加载器（从 JSON 读取）
│   └── routes/                     #   Flask Blueprint 路由
│       ├── problems.py             #     题目 CRUD + 测试用例 + 导入导出
│       ├── judge.py                #     代码运行 + 提交 + 提交历史
│       └── stats.py                #     统计 + 标签 + 每日一题
├── frontend/                       # 前端资源
│   ├── static/js/app.js            #   单页应用逻辑
│   └── templates/index.html        #   HTML 页面 (Tailwind + Monaco)
├── data/                           # 运行时数据（已 gitignore）
│   ├── acm_trainer.db              #   SQLite 数据库（自动生成）
│   └── problems_seed.json          #   32 道内置题目（22 LeetCode + 10 阿里真题）
├── README.md
└── .gitignore
```

### 模块职责

| 模块 | 职责 | 依赖 |
|------|------|------|
| app.py | 创建 Flask 应用、注册 Blueprint、启动服务 | backend.routes.* |
| backend/routes/problems.py | 题目 CRUD、测试用例管理、导入导出 | database |
| backend/routes/judge.py | 代码运行（调试）、提交（保存）、提交历史 | database, judge |
| backend/routes/stats.py | 做题统计、标签列表、每日一题管理 | database, daily |
| backend/database.py | 4 张表的 CRUD、统计、导入导出 | 无 |
| backend/judge.py | 代码执行、超时控制、输出比对 | 无 |
| backend/daily.py | 智能选题（薄弱题 > 遗忘复习 > 新题 > 随机） | database |
| backend/seed_data.py | 从 JSON 加载种子题目，增量插入数据库 | database |
| frontend/static/js/app.js | 前端路由、编辑器管理、API 调用、草稿保存 | Monaco, marked.js |

### 数据库表结构

- **problems** -- 题目（标题、描述、难度、标签、模板代码、核心代码模板/适配器）
- **test_cases** -- 测试用例（输入、期望输出、排序）
- **submissions** -- 提交记录（代码、状态、耗时、模式）
- **daily_problems** -- 每日一题记录（日期、完成状态）

---

## 内置题库

### LeetCode 经典题（22 道）

涵盖数组、链表、树、动态规划、贪心、设计类等常见考点。

### 阿里巴巴笔试真题（10 道）

| 题目 | 难度 | 标签 | 来源 |
|------|------|------|------|
| N×3方格填数 | Medium | DP、状态压缩 | 2021春招 |
| 词语模式匹配 | Easy | 哈希表、双射 | 2021春招 |
| 删除字符使字典序最小 | Medium | 贪心、单调栈 | 笔试真题 |
| 最小花费乘到目标 | Medium | DFS、数学 | 笔试真题 |
| 矩阵聚光灯得分 | Medium | 前缀和、矩阵 | 2022笔试 |
| 十六进制转二进制计1 | Easy | 位运算 | 2022/2023笔试 |
| 三元组差值统计 | Medium | 哈希表、组合数学 | 2023笔试 |
| 圣诞老人分糖果 | Medium | 贪心、数学 | 2026春招 |
| 字典序最大公共子序列 | Medium | 贪心、排列 | 2026春招 |
| 三星数字 | Hard | 二分查找、数位DP | 2026春招 |

---

## 功能说明

### 做题模式

| 模式 | 说明 |
|------|------|
| ACM | 自行处理标准输入输出，贴近竞赛真实环境 |
| 核心代码 | 只需实现函数/类，系统自动拼接 I/O 适配器 |

核心代码模式下，测试用例输入会转为可读参数形式（如 `nums = [1, 2, 3]`）。

### 判题状态

| 状态 | 含义 |
|------|------|
| Accepted | 全部用例通过 |
| Wrong Answer | 输出不匹配 |
| Time Limit Exceeded | 超时（默认 5 秒） |
| Runtime Error | 运行报错 |

### 快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl/Cmd + Enter | 提交代码 |
| Ctrl/Cmd + Shift + Enter | 运行代码 |
| Escape | 关闭弹窗 |

### 其他特性

- 代码草稿自动保存到 localStorage，切题再回来不丢失
- 编辑器字体大小可调（工具栏 +/- 按钮，持久化保存）
- 标签筛选：题库支持按标签过滤
- 每日一题智能推荐，30 天内不重复
- 题库 JSON 导入导出（页面底部）
- 题目分组展示：面试真题 / LeetCode 原题

---

## API 概览

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/problems` | 题目列表（支持 difficulty/tag/keyword 筛选） |
| POST | `/api/problems` | 创建题目 |
| GET/PUT/DELETE | `/api/problems/<id>` | 单题 CRUD |
| GET/POST | `/api/problems/<id>/testcases` | 测试用例 |
| PUT/DELETE | `/api/testcases/<id>` | 单用例操作 |
| POST | `/api/submit/<id>` | 提交判题（保存记录） |
| POST | `/api/run/<id>` | 调试运行（不保存） |
| GET | `/api/submissions` | 提交历史 |
| GET/POST | `/api/daily` `/api/daily/refresh` | 每日一题 |
| GET | `/api/stats` | 做题统计 |
| GET/POST | `/api/export` `/api/import` | 题库导入导出 |

---

## 常见问题

**数据存在哪？** `data/acm_trainer.db`，删除后重启即可重置。

**支持什么语言？** 当前仅 Python。

**如何备份？** 复制 db 文件，或使用页面底部「导出题库」。

---

## 技术栈

Python + Flask / SQLite / Tailwind CSS / Monaco Editor / Marked.js
