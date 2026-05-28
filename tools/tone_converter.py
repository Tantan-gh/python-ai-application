from utils.gemini_client import generate


TONE_DESCRIPTIONS = {
    "丁寧語・です・ます調": "丁寧な「です・ます」調の敬語表現",
    "カジュアル・友達口調": "くだけた友達同士の会話口調",
    "ビジネス丁寧語": "ビジネスシーンで使う格式高い敬語表現",
    "フォーマル・書き言葉": "論文やレポートで使う硬い書き言葉調",
    "SNS・ポップ調": "SNSで使うような短くテンポよい表現",
}


def convert_tone(text: str, target_tone: str) -> str:
    text = text[:5000].strip()
    tone_desc = TONE_DESCRIPTIONS.get(target_tone, target_tone)

    prompt = f"""あなたは日本語表現の専門家です。以下の文章を指定されたトーン・文体に変換してください。

【変換先のトーン】{tone_desc}

【元の文章】
{text}

以下の形式で出力してください：

## 変換後の文章
（変換した文章をここに記載）

## 変換のポイント
（トーン変換で変えた主な点を2〜3点説明）"""

    return generate(prompt)
