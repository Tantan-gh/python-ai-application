from utils.gemini_client import generate


def summarize_text(
    text: str,
    style: str,
    length: str,
    focus: str = "",
) -> str:
    text = text[:5000].strip()
    focus = focus[:200].strip()
    focus_instruction = f"\n特に以下の点に注目して要約してください: {focus}" if focus else ""
    length_map = {
        "3行以内": "3行以内の超短い要約",
        "100字程度": "100字程度の短い要約",
        "200字程度": "200字程度の要約",
        "箇条書き（5項目）": "箇条書き5項目の要約",
    }
    length_str = length_map.get(length, "200字程度の要約")

    prompt = f"""あなたは優秀な文章要約の専門家です。以下の文章を要約してください。

【要約スタイル】{style}
【要約の長さ】{length_str}{focus_instruction}

【要約対象の文章】
{text}

要約結果のみを出力してください。"""

    return generate(prompt)
