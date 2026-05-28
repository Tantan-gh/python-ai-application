from utils.gemini_client import generate


PLATFORM_SPECS = {
    "X（Twitter）": {"max_chars": 140, "note": "140字以内。ハッシュタグ2〜3個を末尾に付ける。"},
    "Instagram": {"max_chars": 300, "note": "300字程度。改行を活用し読みやすく。絵文字を適度に使用。ハッシュタグ5〜10個。"},
    "Facebook": {"max_chars": 400, "note": "400字程度。自然な語り口で親しみやすく。"},
    "LinkedIn": {"max_chars": 500, "note": "500字程度。プロフェッショナルなトーン。学びや気づきを共有する形式。"},
    "Threads": {"max_chars": 300, "note": "300字程度。カジュアルで会話的なトーン。"},
}


def write_sns_post(
    topic: str,
    platform: str,
    purpose: str,
    additional_info: str = "",
) -> str:
    topic = topic[:200].strip()
    additional_info = additional_info[:200].strip()
    spec = PLATFORM_SPECS.get(platform, {"max_chars": 300, "note": "300字程度。"})
    extra = f"\n追加情報: {additional_info}" if additional_info else ""

    prompt = f"""あなたはSNSマーケティングの専門家です。以下の条件でSNS投稿文を作成してください。

【投稿プラットフォーム】{platform}
【投稿のテーマ・内容】{topic}
【投稿の目的】{purpose}
【文字数・スタイル】{spec['note']}{extra}

バリエーションとして3パターンの投稿文を作成してください。
各パターンを「--- パターン1 ---」のように区切って出力してください。"""

    return generate(prompt)
