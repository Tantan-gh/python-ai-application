from utils.gemini_client import generate


def generate_email_reply(
    original_email: str,
    reply_intent: str,
    tone: str,
    sender_name: str = "",
) -> str:
    original_email = original_email[:3000].strip()
    reply_intent = reply_intent[:500].strip()
    sender_name = sender_name[:50].strip()
    signature = f"\n署名者の名前: {sender_name}" if sender_name else ""

    prompt = f"""あなたはビジネスメールの専門家です。以下の受信メールに対する返信文を作成してください。

【受信したメール】
{original_email}

【返信の意図・内容】
{reply_intent}

【文体・トーン】{tone}{signature}

以下の点に注意して返信文を作成してください：
- 適切な宛名と挨拶
- 簡潔で分かりやすい本文
- 丁寧な締めの言葉
- 自然な日本語

件名と本文を含む完全なメール形式で出力してください。"""

    return generate(prompt)
