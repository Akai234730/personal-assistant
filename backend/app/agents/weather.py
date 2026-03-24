# ============================================================
# agents/weather.py - 天气 Agent
# ============================================================
# 开发顺序：Services 写完后第一个写（最简单）
# 原理：
#   1. 调用天气 API 拿到原始数据（数字）
#   2. 把数据发给 GPT，生成人类可读的报告
#   原始数据：{ temp: 22.5, humidity: 65, description: '小雨' }
#   GPT生成：「北京今天22.5°C，有小雨，建议带伞，穿薄外套...」
# ============================================================

from app.services.openai_client import chat_with_ai
from app.services.weather_api import get_weather


def weather_agent(city: str) -> str:
    """
    天气 Agent：输入城市名，输出天气报告+生活建议
    """
    # 步骤1：调用天气 API 获取原始数据
    weather_data = get_weather(city)

    # 步骤2：定义系统提示词（Agent 的「灵魂」）
    system_prompt = """你是一个专业的天气播报员兼生活助手。
根据天气数据生成友好实用的天气报告，包含：
1. 当前天气概况（温度、天气状况）
2. 体感温度说明
3. 穿衣建议
4. 出行提示（是否需要带伞、防晒等）
5. 一句暖心的话结尾
语气亲切自然，像朋友聊天，不用 Markdown 格式。"""

    # 步骤3：把天气数据格式化后发给 GPT
    user_message = f"""请根据以下天气数据生成报告：
城市：{weather_data['city']}, {weather_data['country']}
当前温度：{weather_data['temp']}°C
体感温度：{weather_data['feels_like']}°C
今日最低/最高：{weather_data['temp_min']}°C / {weather_data['temp_max']}°C
天气状况：{weather_data['description']}
湿度：{weather_data['humidity']}%
风速：{weather_data['wind_speed']} 米/秒
能见度：{weather_data['visibility']} 米"""

    # temperature=0.5 偏低，让报告更稳定准确
    return chat_with_ai(system_prompt, user_message, temperature=0.5)
