# ============================================================
# services/openai_client.py - 千问 API 封装
# ============================================================
# 原理：
#   通义千问提供与 OpenAI 完全兼容的 API 接口
#   使用同一个 openai SDK，只需在创建客户端时：
#     1. 把 api_key 换成阿里云 DashScope Key
#     2. 把 base_url 指向千问的兼容接入点
#   调用方式、参数格式、返回格式完全一致，其他代码零修改
#
#   这就是「兼容层」设计模式的价值：
#   对外暴露统一接口，内部可以随时切换底层实现
# ============================================================

from openai import OpenAI
from app.config import DASHSCOPE_API_KEY, DASHSCOPE_BASE_URL, OPENAI_MODEL

# 创建客户端时传入两个额外参数：
# - api_key   : 你的阿里云 DashScope API Key
# - base_url  : 千问兼容 OpenAI 格式的接入地址
client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url=DASHSCOPE_BASE_URL,
)


def chat_with_ai(system_prompt: str, user_message: str, temperature: float = 0.7) -> str:
    """
    向千问 AI 发送对话请求，返回 AI 的回复文本

    参数：
    - system_prompt : 系统提示词，告诉 AI「你是谁、你的职责」
    - user_message  : 用户实际发送的内容
    - temperature   : 创造性程度 0.0~1.0（千问建议范围）
                      0.0=保守精确（适合翻译）
                      0.7=平衡（默认）
                      1.0=创意发散（适合食谱/旅游）

    注意：千问的 temperature 范围是 0~1（OpenAI 是 0~2）
          本项目各 Agent 使用的值都在 0~1 之间，无需调整
    """
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message},
        ],
        temperature=temperature,
    )
    return response.choices[0].message.content
