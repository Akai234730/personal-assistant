# 私人助手 · 项目开发文档

> 面向初学者的完整企业级开发教程。

---

## 1. 企业级开发流程总览

```
需求分析 → 技术选型 → 架构设计 → 接口设计
    ↓
后端开发（先跑通核心逻辑）
    ↓
前端开发（对接接口）
    ↓
联调测试 → Bug修复 → 上线部署 → 迭代新功能
```

### 为什么先写后端再写前端？
1. 后端是核心逻辑，天气查询、AI 回复等真正的功能在后端
2. 后端接口稳定后，前端才知道调用什么
3. 可以不依赖前端直接测试：访问 `/docs` 即可

### 企业角色分工
| 角色 | 负责内容 |
|------|----------|
| 产品经理 | 需求文档，定义功能 |
| 架构师 | 设计架构，选技术栈 |
| 后端工程师 | API、业务逻辑 |
| 前端工程师 | 页面，对接 API |
| 测试工程师 | 验证功能正确性 |
| DevOps | 部署上线，运维 |

---

## 2. 项目架构设计

```
用户（浏览器）
    │  HTTP 请求（JSON）
    ▼
FastAPI 后端（localhost:8000）
    ├── /api/weather   → Weather Agent   → 天气API + GPT
    ├── /api/travel    → Travel Agent    → GPT
    ├── /api/translate → Translate Agent → GPT
    ├── /api/recipe    → Recipe Agent    → GPT
    └── /api/reply     → Reply Agent     → GPT
    │  HTTP 响应（JSON）
    ▼
前端展示（marked.js 渲染 Markdown）
```

### 技术栈
| 层级 | 技术 | 原因 |
|------|------|------|
| 前端 | HTML + CSS + JS 原生 | 初学者友好，零依赖 |
| 后端 | Python + FastAPI | 语法简单，自带交互式文档 |
| AI | OpenAI API | 最成熟，接口简单 |
| 天气 | OpenWeatherMap | 免费，支持中文 |

---

## 3. 多智能体原理

### 什么是 Agent？
**Agent = 有特定任务的 AI 模块**，包含：
- **System Prompt**：告诉 AI 「你是谁、你的职责」
- **处理函数**：接收输入，调用 AI，返回输出
- **可选工具**：天气 Agent 需调用天气 API

### 为什么用多 Agent？
```
❌ 单 Agent：提示词越来越长，AI 混乱，功能互相影响
✅ 多 Agent：每个职责单一，独立升级，扩展只需加新文件
            符合软件工程「单一职责原则」
```

### 数据流示例
```
用户输入「北京」点击查询天气
  → POST /api/weather { "city": "北京" }
  → Weather Agent:
      1. 调用天气API → { temp:22, desc:"晴", humidity:60 }
      2. 把数据发给 GPT，让它生成报告
      3. 返回 { success:true, data:"北京今天晴，22°C..." }
  → 前端 marked.parse() 渲染显示
```

---

## 4. 目录结构详解

```
e:\personal assistant\
├── README.md                 ← 快速启动
├── docs/PROJECT_PLAN.md      ← 本文件
├── backend/
│   ├── requirements.txt      ← pip 依赖列表
│   ├── .env.example          ← API Key 模板
│   └── app/
│       ├── __init__.py       ← 让 Python 识别为包
│       ├── main.py           ← 入口：注册路由，启动服务
│       ├── config.py         ← 读取 .env 配置
│       ├── models.py         ← 请求/响应数据格式
│       ├── agents/
│       │   ├── weather.py    ← 天气 Agent
│       │   ├── travel.py     ← 旅游规划 Agent
│       │   ├── translate.py  ← 翻译 Agent
│       │   ├── recipe.py     ← 食谱 Agent
│       │   └── reply_coach.py← 社恐回复 Agent
│       └── services/
│           ├── openai_client.py ← 封装 OpenAI（所有Agent共用）
│           └── weather_api.py   ← 封装天气 API
└── frontend/
    ├── index.html            ← 主页面结构
    ├── style.css             ← 深色主题样式
    └── app.js                ← 交互逻辑
```

### 为什么要有 services 层？
`openai_client.py` 封装 OpenAI 调用，5 个 Agent 共用同一个函数。
这是 **DRY 原则**（Don't Repeat Yourself）：哪天换模型，只改一个文件。

---

## 5. 开发顺序与分阶段计划

### 阶段一：环境搭建（第1天）
目标：服务器跑起来，访问 http://localhost:8000/docs

```bash
# 1. 安装依赖
cd backend
pip install -r requirements.txt

# 2. 配置 Key
copy .env.example .env
# 用编辑器打开 .env，填写 OPENAI_API_KEY 和 WEATHER_API_KEY

# 3. 启动服务器
uvicorn app.main:app --reload
```

> 学习重点：什么是服务器、端口、API、JSON

### 阶段二：第一个 Agent（第2天）
目标：天气接口返回真实数据

- 注册 OpenWeatherMap：https://openweathermap.org（免费）
- 注册 OpenAI：https://platform.openai.com
- 填好 `.env` 后在 `/docs` 测试 `/api/weather`

> 学习重点：HTTP 请求/响应结构，环境变量的意义

### 阶段三：其余 Agent（第3-5天）
**开发顺序（按复杂度）：翻译 → 食谱 → 社恐回复 → 旅游规划**

每个 Agent 的固定流程：
1. `models.py` 添加数据模型
2. 写 Agent 函数（设计提示词 + 调用 GPT）
3. `main.py` 注册新路由
4. `/docs` 测试验证

### 阶段四：前端界面（第6-7天）
1. `index.html`：HTML 结构（骨架）
2. `style.css`：样式（外观）
3. `app.js`：JS 交互（用 fetch 调用后端）

### 阶段五：联调优化（第8天）
前后端跑通 → 修复 Bug → 优化提示词

---

## 6. 各功能模块逻辑

### 天气 Agent
```
城市名 → 天气API（温度/湿度/描述）→ GPT生成报告 → 返回文本
```

### 社恐回复 Agent（核心功能）
```
对方身份 + 消息原文 + 我的目的 + 语气
  → GPT 生成 3 种风格：
      A. 简短直接版
      B. 标准礼貌版
      C. 高情商版
  → 可直接复制发送
```
设计思路：社恐的根源是「不知道说什么」，AI 把模糊规则变成具体文字。

### 旅游规划 Agent
```
目的地 + 天数 + 预算 + 偏好
  → GPT 生成每日行程（上午/下午/晚上）+ 交通 + 住宿 + 预算分配
```

### 翻译 Agent
```
原文 + 目标语言 + 场景
  → GPT 提供直译版 + 意译版 + 术语注释
```

### 食谱 Agent
```
食材 + 口味 + 时间 + 难度
  → GPT 推荐 3 道菜（食材清单 + 步骤 + 技巧）
```

---

## 7. API 设计规范

所有接口使用 HTTP POST，请求体和响应体均为 JSON。

### 统一响应格式
```json
{ "success": true,  "data": "AI生成的内容", "error": null }
{ "success": false, "data": null, "error": "错误描述" }
```
前端通过 `success` 字段判断成功/失败，统一处理。

### 接口列表
| 路径 | 请求参数 |
|------|----------|
| POST /api/weather | city |
| POST /api/travel | destination, departure, days, budget, preference |
| POST /api/translate | text, target_language, scene |
| POST /api/recipe | ingredients, taste, cook_time, difficulty |
| POST /api/reply | sender_role, message, my_goal, tone, extra_context |

---

## 8. 如何运行项目

```bash
# 终端1：启动后端
cd "e:\personal assistant\backend"
pip install -r requirements.txt
uvicorn app.main:app --reload

# 测试后端（浏览器打开）
http://localhost:8000/docs

# 终端2（可选）：前端直接打开文件
# 用浏览器打开 e:\personal assistant\frontend\index.html
```

---

## 9. 学习路线建议

### 推荐阅读顺序
1. `config.py` — 最短，理解环境变量
2. `models.py` — 理解数据格式定义
3. `services/openai_client.py` — 理解如何调 AI
4. `agents/weather.py` — 最简单的 Agent
5. `agents/reply_coach.py` — 最复杂的 Agent，重点学提示词设计
6. `main.py` — 理解路由注册
7. `frontend/app.js` — 理解 fetch 调用后端

### 关键概念对照表
| 概念 | 类比 |
|------|------|
| 服务器 | 餐厅后厨，等待客人（前端）点菜 |
| API 接口 | 菜单上的菜品，每个有固定名字和规格 |
| HTTP 请求 | 服务员把点菜单送到后厨 |
| JSON | 一种标准化的「格式」，前后端都能读懂 |
| Agent | 专门做某类菜的厨师（天气厨师/翻译厨师）|
| 环境变量 | 保险柜里的密钥，不写在菜谱上 |
| CORS | 餐厅规定「只接受本店客人点菜」，配置后放开限制 |
