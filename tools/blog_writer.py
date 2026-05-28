from utils.gemini_client import generate


def write_blog(
    topic: str,
    tone: str,
    target_audience: str,
    length: str,
    keywords: str = "",
) -> str:
    topic = topic[:200].strip()
    target_audience = target_audience[:100].strip()
    keywords = keywords[:200].strip()
    keyword_instruction = f"\n以下のキーワードを自然に含めてください: {keywords}" if keywords else ""
    length_map = {"短め（500字程度）": "500字程度", "普通（1000字程度）": "1000字程度", "長め（2000字程度）": "2000字程度"}
    length_str = length_map.get(length, "1000字程度")

    prompt = f"""あなたはプロのブログライターです。以下の条件でブログ記事を執筆してください。

【テーマ】{topic}
【文体・トーン】{tone}
【ターゲット読者】{target_audience}
【文字数の目安】{length_str}{keyword_instruction}

記事は以下の構成で書いてください：
- タイトル（## で表記）
- 導入文（読者の興味を引く）
- 本文（適切な見出しで区切る）
- まとめ

マークダウン形式で出力してください。"""

    return generate(prompt)
