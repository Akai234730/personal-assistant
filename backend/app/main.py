# ============================================================
# main.py - FastAPI 应用入口
# ============================================================
# 开发顺序：所有 Agent 写完后最后写这个
# 原理：
#   main.py 是整个后端的「总指挥」，负责：
#   1. 创建 FastAPI 应用实例
#   2. 配置 CORS（允许前端跨域访问后端）
#   3. 注册所有 API 路由（URL路径 → 处理函数）
#
# 什么是路由？
#   路由 = URL路径 → 处理函数的映射
#   例如：用户访问 /api/weather → 执行 weather_endpoint()
#
# 什么是 CORS？
#   浏览器默认禁止网页向不同域名/端口发请求（安全限制）
#   前端在 localhost:5500，后端在 localhost:8000，端口不同
#   必须在后端配置 CORS，浏览器才允许前端来访问
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import (
    WeatherRequest, TravelRequest, TranslateRequest,
    RecipeRequest, ReplyRequest, ApiResponse
)
from app.agents.weather import weather_agent
from app.agents.travel import travel_agent
from app.agents.translate import translate_agent
from app.agents.recipe import recipe_agent
from app.agents.reply_coach import reply_coach_agent

# ============================================================
# 创建 FastAPI 实例
# title/description 显示在自动生成的 /docs 文档页面
# ============================================================
app = FastAPI(
    title="私人助手 API",
    description="多智能体个人助手：天气、旅游、翻译、食谱、社恐回复",
    version="1.0.0",
)

# ============================================================
# 配置 CORS 中间件
# 中间件：每个请求到达路由函数「之前」都会经过的处理层
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # 开发阶段允许所有来源，生产环境应指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 健康检查接口：快速确认服务器是否正常运行
@app.get("/", summary="健康检查")
def root():
    return {"status": "ok", "message": "私人助手服务运行正常 ✅"}


# ============================================================
# 天气查询接口
# @app.post 装饰器：把函数注册为 POST /api/weather 的处理函数
# response_model：告诉 FastAPI 返回值的格式（用于文档生成）
# ============================================================
@app.post("/api/weather", response_model=ApiResponse, summary="天气查询")
def weather_endpoint(request: WeatherRequest):
    """根据城市名查询天气，生成包含穿衣建议的天气报告"""
    try:
        result = weather_agent(request.city)
        return ApiResponse(success=True, data=result, error=None)
    except Exception as e:
        # 捕获所有异常，统一返回错误格式，防止服务器崩溃
        return ApiResponse(success=False, data=None, error=str(e))


@app.post("/api/travel", response_model=ApiResponse, summary="旅游路线规划")
def travel_endpoint(request: TravelRequest):
    """根据目的地、天数、预算生成详细旅游攻略"""
    try:
        result = travel_agent(
            destination=request.destination,
            departure=request.departure,
            days=request.days,
            budget=request.budget,
            preference=request.preference,
        )
        return ApiResponse(success=True, data=result, error=None)
    except Exception as e:
        return ApiResponse(success=False, data=None, error=str(e))


@app.post("/api/translate", response_model=ApiResponse, summary="智能翻译")
def translate_endpoint(request: TranslateRequest):
    """多语言翻译，提供直译和意译两个版本"""
    try:
        result = translate_agent(
            text=request.text,
            target_language=request.target_language,
            scene=request.scene,
        )
        return ApiResponse(success=True, data=result, error=None)
    except Exception as e:
        return ApiResponse(success=False, data=None, error=str(e))


@app.post("/api/recipe", response_model=ApiResponse, summary="食谱推荐")
def recipe_endpoint(request: RecipeRequest):
    """根据现有食材和偏好推荐菜谱，含详细步骤"""
    try:
        result = recipe_agent(
            ingredients=request.ingredients,
            taste=request.taste,
            cook_time=request.cook_time,
            difficulty=request.difficulty,
        )
        return ApiResponse(success=True, data=result, error=None)
    except Exception as e:
        return ApiResponse(success=False, data=None, error=str(e))


@app.post("/api/reply", response_model=ApiResponse, summary="社恐回复助手")
def reply_endpoint(request: ReplyRequest):
    """根据对方身份和消息，生成3种风格的回复供选择"""
    try:
        result = reply_coach_agent(
            sender_role=request.sender_role,
            message=request.message,
            my_goal=request.my_goal,
            tone=request.tone,
            extra_context=request.extra_context,
        )
        return ApiResponse(success=True, data=result, error=None)
    except Exception as e:
        return ApiResponse(success=False, data=None, error=str(e))


# 直接运行此文件时的入口（通常用 uvicorn 命令启动）
if __name__ == "__main__":
    import uvicorn
    from app.config import HOST, PORT
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
