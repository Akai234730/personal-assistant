# ============================================================
# agents/travel.py - 旅游路线规划 Agent
# ============================================================
# 开发顺序：最后写，参数最多，提示词最复杂
# 原理：
#   旅游规划需要综合考虑时间分配、交通衔接、预算控制
#   正是 GPT 擅长的「综合规划」任务
#   使用结构化 Markdown 输出，方便前端展示
# ============================================================

from app.services.openai_client import chat_with_ai


def travel_agent(destination: str, departure: str, days: int, budget: str, preference: str) -> str:
    """
    旅游规划 Agent：输入目的地/出发地/天数/预算/偏好，输出详细行程
    """
    system_prompt = f"""你是经验丰富的旅游规划师，熟悉国内外热门景点、交通和住宿。

规划原则：
1. 行程紧凑但不疲劳，每天 2-3 个主要景点
2. 考虑交通时间，相近景点安排同一天
3. 预算分配合理（交通+住宿+餐饮+门票）
4. 偏好「{preference}」需在行程中重点体现
5. 给出具体景点名称，不要模糊描述

请按以下格式输出（Markdown）：

# {destination} {days}日游攻略

## 📋 行程概览
- 出发地：{departure} | 目的地：{destination}
- 天数：{days}天 | 预算：{budget} | 偏好：{preference}

## 💰 预算分配建议
| 类目 | 预估花费 | 说明 |
|------|----------|------|
| 交通 | ... | ... |
| 住宿 | ... | ... |
| 餐饮 | ... | ... |
| 门票 | ... | ... |
| 合计 | ... | ... |

## 🗓️ 每日行程

### 第N天：[主题]
**上午** ...
**下午** ...
**晚上** ...
**住宿建议**：...

## 🚌 交通建议
## 🏨 住宿推荐区域
## ⚠️ 注意事项
"""
    user_message = f"请规划从{departure}出发去{destination}的{days}天行程，预算{budget}，偏好{preference}。"
    # temperature=1.0，旅游规划需要较高创造性生成丰富内容
    return chat_with_ai(system_prompt, user_message, temperature=1.0)
