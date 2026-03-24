# 私人助手 · Personal AI Assistant

> 多智能体协作的私人 AI 助手，包含天气查询、旅游规划、智能翻译、食谱推荐、社恐回复五大功能。
> 面向初学者，每一行关键代码都附有详细注释和原理说明。

---

## 项目结构

```
personal assistant/
├── docs/
│   └── PROJECT_PLAN.md     # 完整开发文档（必读）
├── backend/
│   ├── requirements.txt    # Python 依赖
│   ├── .env.example        # 配置模板
│   └── app/
│       ├── main.py         # FastAPI 入口
│       ├── config.py       # 读取配置
│       ├── models.py       # 数据模型
│       ├── agents/         # 各功能 Agent
│       └── services/       # 外部 API 封装
└── frontend/
    ├── index.html          # 主页面
    ├── style.css           # 样式
    └── app.js              # 交互逻辑
```

---

## 快速启动（5步）

### 第一步：安装 Python 依赖

```bash
cd backend
pip install -r requirements.txt
```

### 第二步：配置 API Key

```bash
copy .env.example .env
```

然后打开 `.env`，填入：
- `DASHSCOPE_API_KEY`：从 https://dashscope.console.aliyun.com/apiKey 获取（注册阿里云账号，进入百炼控制台，有免费额度）
- `WEATHER_API_KEY`：从 https://openweathermap.org/api 免费注册获取
- `QWEN_MODEL`：默认 `qwen-turbo`，可改为 `qwen-plus`（均衡）或 `qwen-max`（最强）

### 第三步：启动后端服务器

```bash
uvicorn app.main:app --reload
```

看到 `Uvicorn running on http://0.0.0.0:8000` 说明启动成功。

### 第四步：打开 API 文档测试后端

浏览器访问：http://localhost:8000/docs

### 第五步：打开前端网页

直接用浏览器打开 `frontend/index.html`。

---

## 功能说明

| 功能 | 说明 | 依赖 |
|------|------|------|
| 🌤 天气查询 | 实时天气 + 穿衣建议 | OpenWeatherMap + 千问 |
| ✈️ 旅游规划 | 每日行程 + 预算分配 | 通义千问 |
| 🌐 智能翻译 | 直译 + 意译双版本 | 通义千问 |
| 🍳 食谱推荐 | 按食材推荐 + 详细步骤 | 通义千问 |
| 💬 社恐回复 | 三种风格回复可选 | 通义千问 |

---

## 开发文档

详细的开发顺序、代码原理、企业流程说明请阅读：

**[📖 docs/PROJECT_PLAN.md](docs/PROJECT_PLAN.md)**

---

## 常见问题

**Q: 启动后访问 /docs 报错？**
A: 检查 `.env` 文件是否存在，且在 `backend` 目录下执行启动命令。

**Q: 天气查询返回错误？**
A: 确认 `WEATHER_API_KEY` 已填写，城市名支持中文和英文。

**Q: AI 功能不工作？**
A: 确认 `DASHSCOPE_API_KEY` 有效。可在阿里云百炼控制台查看余额：https://dashscope.console.aliyun.com

**Q: 前端显示「网络请求失败」？**
A: 后端服务器未启动，请先执行第三步。
