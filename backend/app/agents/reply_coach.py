# ============================================================
# agents/reply_coach.py - 社恐回复 Agent
# ============================================================
# 开发顺序：第四个，最有特色的功能
# 原理：
#   「角色扮演 + 场景理解」型 Agent
#   关键：System Prompt 让 AI 理解社交场合的微妙之处
#   通过「身份 + 目的 + 语气」三维度生成有针对性的回复
#   给出 3 个版本让用户选择，降低选择焦虑
# ============================================================

from app.services.openai_client import chat_with_ai
from typing import Optional


def reply_coach_agent(
    sender_role: str,
    message: str,
    my_goal: str,
    tone: str,
    extra_context: Optional[str] = None
) -> str:
    """
    社恐回复 Agent：输入对方身份/消息/目的/语气，输出3种风格回复
    """
    context_prompt = f"\n补充背景：{extra_context}" if extra_context else ""

    # 每种身份对应不同的社交规则说明
    # 这是提示词工程技巧：给 AI 提供「角色对应的社交规则」让判断更准确
    role_context = {
        "领导": "保持专业和尊重，措辞不能太随意，但也不要过于谄媚",
        "同事": "平级关系，可以相对随和，但要维持职场礼仪",
        "朋友": "关系亲近，可以更真实直接，甚至适当幽默",
        "家人": "最亲近的关系，避免引发矛盾，保持家庭和谐",
        "客户": "服务关系，需要耐心礼貌，维护长期合作",
        "陌生人": "保持礼貌距离，不需过度热情，简洁明了即可",
    }
    role_tip = role_context.get(sender_role, "保持基本礼貌")

    system_prompt = f"""你是精通人际沟通的高情商助手，专门帮助在社交场合感到焦虑的人。

【当前场景】
- 对方身份：{sender_role}（{role_tip}）
- 我的目的：{my_goal}
- 回复语气：{tone}{context_prompt}

【任务】生成 3 个不同版本的回复。

要求：
1. 每个版本都必须符合「{my_goal}」这个目的
2. 语气符合与「{sender_role}」的身份关系
3. 三个版本之间要有明显差异
4. 每个回复可以直接复制发送
5. 长度合理：不太短显得敷衍，不太长显得啰嗦

【输出格式】（Markdown）

**版本 A · 简短直接版**
> [回复内容]

*适用：不想解释太多，快速回应*

---

**版本 B · 标准礼貌版**
> [回复内容]

*适用：大多数情况下的安全之选*

---

**版本 C · 高情商版**
> [回复内容]

*适用：想留下好印象，或关系比较重要*

---

**💡 小提示**
[一句话说明这类回复的沟通技巧]"""

    # temperature=0.8，需要一定创造性来生成有差异的三个版本
    return chat_with_ai(system_prompt, f"对方发来的消息：\"{message}\"", temperature=0.8)
