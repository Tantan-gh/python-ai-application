from utils.gemini_client import generate


def proofread_text(text: str, mode: str) -> str:
    text = text[:5000].strip()
    mode_instructions = {
        "誤字脱字の修正": "誤字・脱字・変換ミスを修正してください。文体や内容は変えないでください。",
        "読みやすさの改善": "文章の流れ・読みやすさ・構成を改善してください。意味は保ちつつ、より自然な日本語にしてください。",
        "ビジネス文書向けに整える": "ビジネス文書として適切な敬語・表現・構成に整えてください。",
        "全て（修正＋改善）": "誤字脱字の修正、読みやすさの向上、文体の統一を総合的に行ってください。",
    }
    instruction = mode_instructions.get(mode, mode_instructions["全て（修正＋改善）"])

    prompt = f"""あなたはプロの校正者です。以下の文章を校正・改善してください。

【作業内容】{instruction}

【元の文章】
{text}

以下の形式で出力してください：

## 修正後の文章
（修正・改善した文章をここに記載）

## 変更点のポイント
（主な変更箇所を箇条書きで3〜5点説明）"""

    return generate(prompt)
