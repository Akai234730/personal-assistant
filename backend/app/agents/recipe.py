# ============================================================
# agents/recipe.py - 食谱推荐 Agent
# ============================================================
# 原理：根据用户的食材、口味、时间、难度，让 GPT 推荐菜谱
#       temperature 设高一点让推荐更多样化
# ============================================================

from app.services.openai_client import chat_with_ai


def recipe_agent(ingredients: str, taste: str, cook_time: int, difficulty: str) -> str:
    """
    食谱推荐 Agent：输入食材/口味/时间/难度，输出3道菜食谱
    """
    ingredient_prompt = (
        f"用户现有食材：{ingredients}（优先使用，可补充少量常见调料）"
        if ingredients.strip()
        else "用户未指定食材，推荐需要常见食材的菜肴"
    )

    system_prompt = f"""你是经验丰富的家庭厨师，擅长根据现有条件推荐实用家常菜。

用户条件：
- {ingredient_prompt}
- 口味偏好：{taste}
- 可用时间：{cook_time} 分钟以内
- 难度要求：{difficulty}

请推荐 3 道菜，每道菜格式如下（Markdown）：

## 🍽️ [菜名]

**所需食材**
- 食材：用量

**制作步骤**
1. 步骤一
2. 步骤二

**小贴士** 关键技巧

**预计时间**：XX分钟 | **难度**：{difficulty}

---
"""
    # temperature=0.9 较高，让推荐更多样化
    return chat_with_ai(system_prompt, "请为我推荐今天的菜谱", temperature=0.9)
