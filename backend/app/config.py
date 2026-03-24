# ============================================================
# config.py - 配置读取模块
# ============================================================
# 原理：
#   千问 API 兼容 OpenAI 接口格式（同样用 openai SDK 调用）
#   只需把 base_url 指向阿里云的千问 API 地址
#   api_key 换成你的通义千问 API Key
# ============================================================

from dotenv import load_dotenv
import os

load_dotenv()

# 通义千问 API Key
# 获取地址：https://dashscope.console.aliyun.com/apiKey
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")

# 千问模型选择：
#   qwen-turbo       速度最快，费用最低，适合开发测试
#   qwen-plus        均衡版本，推荐日常使用
#   qwen-max         效果最好，适合生产环境
#   qwen-long        超长上下文，适合长文档处理
OPENAI_MODEL = os.getenv("QWEN_MODEL", "qwen-turbo")

# 千问 API 的 base_url（兼容 OpenAI 格式的接入点）
# 原理：阿里云提供了与 OpenAI SDK 完全兼容的接口
#       只需修改 base_url，其他代码一行不用改
DASHSCOPE_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# 启动检查
if not DASHSCOPE_API_KEY:
    print("⚠️  警告：DASHSCOPE_API_KEY 未设置，AI 功能将无法使用")
    print("       获取地址：https://dashscope.console.aliyun.com/apiKey")
if not WEATHER_API_KEY:
    print("⚠️  警告：WEATHER_API_KEY 未设置，天气功能将无法使用")
