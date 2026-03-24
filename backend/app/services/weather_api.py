# ============================================================
# services/weather_api.py - 天气 API 封装
# ============================================================
# 原理：
#   OpenWeatherMap 提供免费天气数据 API
#   通过 HTTP GET 请求获取 JSON 数据
#   封装成函数让 Weather Agent 直接调用
# ============================================================

import requests
from app.config import WEATHER_API_KEY

BASE_URL = "https://api.openweathermap.org/data/2.5"


def get_weather(city: str) -> dict:
    """
    根据城市名获取当前天气数据
    返回包含温度、湿度、天气描述等字段的字典
    """
    params = {
        "q": city,
        "units": "metric",   # metric=摄氏度
        "lang": "zh_cn",     # 天气描述用中文
        "appid": WEATHER_API_KEY,
    }
    # timeout=10：超过10秒没响应就放弃，避免程序卡住
    response = requests.get(f"{BASE_URL}/weather", params=params, timeout=10)
    # 状态码 4xx/5xx 时自动抛出异常（200=成功, 404=城市不存在, 401=Key错误）
    response.raise_for_status()
    data = response.json()

    return {
        "city":        data["name"],
        "country":     data["sys"]["country"],
        "temp":        round(data["main"]["temp"], 1),
        "feels_like":  round(data["main"]["feels_like"], 1),
        "temp_min":    round(data["main"]["temp_min"], 1),
        "temp_max":    round(data["main"]["temp_max"], 1),
        "humidity":    data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "wind_speed":  data["wind"]["speed"],
        "visibility":  data.get("visibility", 0),
    }
