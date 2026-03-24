# ============================================================
# models.py - 数据模型定义
# ============================================================
# 开发顺序：第二个写，紧接 config.py
# 原理：
#   用 Pydantic 定义每个 API 的请求体和响应体格式
#   FastAPI 自动：
#     1. 验证传入数据类型是否正确
#     2. 在 /docs 生成参数说明文档
#     3. 格式不对时自动返回 422 错误
# ============================================================

from pydantic import BaseModel, Field
from typing import Optional, Literal


# 统一响应格式 - 所有接口都返回这个结构
class ApiResponse(BaseModel):
    success: bool            # True=成功, False=失败
    data: Optional[str]      # 成功时的内容
    error: Optional[str]     # 失败时的错误信息


# 天气查询请求
class WeatherRequest(BaseModel):
    city: str = Field(..., description="城市名，支持中文或英文", examples=["北京", "Shanghai"])


# 旅游规划请求
class TravelRequest(BaseModel):
    destination: str = Field(..., description="目的地", examples=["云南大理"])
    departure: str   = Field(..., description="出发城市", examples=["北京"])
    days: int        = Field(..., description="旅行天数", ge=1, le=30)
    budget: str      = Field(..., description="预算范围", examples=["3000-5000元"])
    preference: str  = Field(default="综合", description="偏好类型", examples=["美食", "历史文化", "自然风光", "综合"])


# 翻译请求
class TranslateRequest(BaseModel):
    text: str            = Field(..., description="需要翻译的原文")
    target_language: str = Field(default="中文", description="目标语言", examples=["英文", "中文", "日文"])
    scene: Literal["日常对话", "正式文件", "技术文档", "文学作品"] = Field(default="日常对话", description="使用场景")


# 食谱推荐请求
class RecipeRequest(BaseModel):
    ingredients: str = Field(default="", description="现有食材，逗号分隔", examples=["鸡蛋, 西红柿"])
    taste: str       = Field(default="随意", description="口味偏好", examples=["清淡", "辣", "酸甜"])
    cook_time: int   = Field(default=30, description="可用时间（分钟）", ge=5, le=120)
    difficulty: Literal["简单", "中等", "较难"] = Field(default="简单", description="难度")


# 社恐回复请求（参数最多，是核心功能）
class ReplyRequest(BaseModel):
    sender_role: Literal["领导", "同事", "朋友", "家人", "客户", "陌生人"] = Field(..., description="对方身份")
    message: str     = Field(..., description="对方发来的消息原文")
    my_goal: Literal["礼貌拒绝", "礼貌拖延", "表达感谢", "道歉", "寻求帮助", "随便回复"] = Field(..., description="我想达到的目的")
    tone: Literal["正式", "随和", "幽默"] = Field(default="随和", description="语气风格")
    extra_context: Optional[str] = Field(default=None, description="补充背景（可选）")
