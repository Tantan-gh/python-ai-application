import logging
import streamlit as st
from tools.blog_writer import write_blog
from tools.email_reply import generate_email_reply
from tools.summarizer import summarize_text
from tools.proofreader import proofread_text
from tools.tone_converter import convert_tone, TONE_DESCRIPTIONS
from tools.sns_writer import write_sns_post, PLATFORM_SPECS

st.set_page_config(
    page_title="AI ライティングツール",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main-header { font-size: 2rem; font-weight: bold; margin-bottom: 0.2rem; }
    .sub-header { color: #666; margin-bottom: 1.5rem; }
    .result-box {
        background-color: #f8f9fa;
        border-left: 4px solid #4CAF50;
        padding: 1rem;
        border-radius: 0.25rem;
        margin-top: 1rem;
    }
    .stButton>button { width: 100%; }
</style>
""", unsafe_allow_html=True)

TOOLS = {
    "📝 ブログ記事作成": "blog",
    "📧 メール返信文生成": "email",
    "📋 文章要約": "summary",
    "🔍 文章校正・改善": "proofread",
    "🔄 トーン変換": "tone",
    "📱 SNS投稿文生成": "sns",
}

with st.sidebar:
    st.markdown("## ✍️ AI ライティングツール")
    st.markdown("---")
    selected_label = st.radio("ツールを選択", list(TOOLS.keys()), label_visibility="collapsed")
    st.markdown("---")
    st.markdown("### 使い方")
    st.markdown("1. ツールを選択\n2. 必要事項を入力\n3. 生成ボタンをクリック")
    st.markdown("---")
    st.caption("Powered by Gemini API")

tool = TOOLS[selected_label]
logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# ブログ記事作成
# ──────────────────────────────────────────────
if tool == "blog":
    st.markdown('<p class="main-header">📝 ブログ記事作成</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">テーマや条件を入力するだけで、ブログ記事を自動生成します。</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        topic = st.text_input("記事のテーマ・タイトル案 *", placeholder="例: 在宅ワークで生産性を上げる方法")
        tone = st.selectbox("文体・トーン", ["フレンドリー・読みやすい", "丁寧・信頼感", "専門的・詳しい", "カジュアル・面白い"])
        length = st.selectbox("文字数", ["短め（500字程度）", "普通（1000字程度）", "長め（2000字程度）"])
    with col2:
        target_audience = st.text_input("ターゲット読者", placeholder="例: 20〜30代の社会人")
        keywords = st.text_input("含めたいキーワード（任意）", placeholder="例: タスク管理, ポモドーロ, 集中力")

    if st.button("記事を生成する", type="primary"):
        with st.spinner("記事を生成中..."):
            try:
                result = write_blog(topic, tone, target_audience or "一般読者", length, keywords)
                st.markdown("### 生成結果")
                st.markdown(result)
                st.download_button("テキストをダウンロード", result, file_name="blog_article.md", mime="text/markdown")
            except Exception as e:
                logger.error("ブログ記事生成エラー", exc_info=True)
                st.error("エラーが発生しました。しばらくしてから再度お試しください。")

# ──────────────────────────────────────────────
# メール返信文生成
# ──────────────────────────────────────────────
elif tool == "email":
    st.markdown('<p class="main-header">📧 メール返信文生成</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">受信メールの内容と返信の意図を入力すると、適切な返信文を生成します。</p>', unsafe_allow_html=True)

    original_email = st.text_area("受信したメールの内容 *", height=180, max_chars=3000, placeholder="ここに受け取ったメールの本文を貼り付けてください...")
    col1, col2 = st.columns([1, 1])
    with col1:
        reply_intent = st.text_area("返信の意図・伝えたいこと *", height=100, max_chars=500, placeholder="例: 会議の日程を来週水曜から木曜に変更したい")
        tone = st.selectbox("文体・トーン", ["ビジネス丁寧語", "丁寧・柔らかい", "フォーマル・格式高い", "簡潔・要件のみ"])
    with col2:
        sender_name = st.text_input("自分の名前（署名用）", placeholder="例: 山田 太郎")

    if st.button("返信文を生成する", type="primary"):
        with st.spinner("返信文を生成中..."):
            try:
                result = generate_email_reply(original_email, reply_intent, tone, sender_name)
                st.markdown("### 生成結果")
                st.markdown(f"```\n{result}\n```")
                st.download_button("テキストをダウンロード", result, file_name="email_reply.txt", mime="text/plain")
            except Exception as e:
                logger.error("メール返信生成エラー", exc_info=True)
                st.error("エラーが発生しました。しばらくしてから再度お試しください。")

# ──────────────────────────────────────────────
# 文章要約
# ──────────────────────────────────────────────
elif tool == "summary":
    st.markdown('<p class="main-header">📋 文章要約</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">長い文章を指定のスタイルと長さで要約します。</p>', unsafe_allow_html=True)

    text = st.text_area("要約したい文章 *", height=220, max_chars=5000, placeholder="ここに要約したい文章を貼り付けてください...")
    col1, col2 = st.columns([1, 1])
    with col1:
        style = st.selectbox("要約スタイル", ["内容を簡潔にまとめる", "重要ポイントを抽出する", "子どもでも分かるように説明する", "専門的な観点でまとめる"])
        length = st.selectbox("要約の長さ", ["3行以内", "100字程度", "200字程度", "箇条書き（5項目）"])
    with col2:
        focus = st.text_input("特に注目してほしい点（任意）", placeholder="例: コスト削減の部分を重点的に")

    if st.button("要約する", type="primary"):
        with st.spinner("要約中..."):
            try:
                result = summarize_text(text, style, length, focus)
                st.markdown("### 要約結果")
                st.markdown(result)
                st.download_button("テキストをダウンロード", result, file_name="summary.txt", mime="text/plain")
            except Exception as e:
                logger.error("文章要約エラー", exc_info=True)
                st.error("エラーが発生しました。しばらくしてから再度お試しください。")

# ──────────────────────────────────────────────
# 文章校正・改善
# ──────────────────────────────────────────────
elif tool == "proofread":
    st.markdown('<p class="main-header">🔍 文章校正・改善</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">誤字脱字の修正から、読みやすさの改善まで対応します。</p>', unsafe_allow_html=True)

    text = st.text_area("校正したい文章 *", height=220, max_chars=5000, placeholder="ここに校正・改善したい文章を入力してください...")
    mode = st.selectbox("作業モード", ["誤字脱字の修正", "読みやすさの改善", "ビジネス文書向けに整える", "全て（修正＋改善）"])

    if st.button("校正・改善する", type="primary"):
        with st.spinner("校正中..."):
            try:
                result = proofread_text(text, mode)
                st.markdown("### 校正結果")
                st.markdown(result)
                st.download_button("テキストをダウンロード", result, file_name="proofread_result.md", mime="text/markdown")
            except Exception as e:
                logger.error("文章校正エラー", exc_info=True)
                st.error("エラーが発生しました。しばらくしてから再度お試しください。")

# ──────────────────────────────────────────────
# トーン変換
# ──────────────────────────────────────────────
elif tool == "tone":
    st.markdown('<p class="main-header">🔄 トーン変換</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">文章のトーン・文体を目的に合わせて変換します。</p>', unsafe_allow_html=True)

    text = st.text_area("変換したい文章 *", height=180, max_chars=5000, placeholder="ここに変換したい文章を入力してください...")
    target_tone = st.selectbox("変換先のトーン", list(TONE_DESCRIPTIONS.keys()))
    st.caption(f"選択中: {TONE_DESCRIPTIONS[target_tone]}")

    if st.button("トーンを変換する", type="primary"):
        with st.spinner("変換中..."):
            try:
                result = convert_tone(text, target_tone)
                st.markdown("### 変換結果")
                st.markdown(result)
                st.download_button("テキストをダウンロード", result, file_name="tone_converted.md", mime="text/markdown")
            except Exception as e:
                logger.error("トーン変換エラー", exc_info=True)
                st.error("エラーが発生しました。しばらくしてから再度お試しください。")

# ──────────────────────────────────────────────
# SNS投稿文生成
# ──────────────────────────────────────────────
elif tool == "sns":
    st.markdown('<p class="main-header">📱 SNS投稿文生成</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">プラットフォームに最適化されたSNS投稿文を3パターン生成します。</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        topic = st.text_input("投稿のテーマ・内容 *", placeholder="例: 新しいカフェのオープン告知")
        platform = st.selectbox("プラットフォーム", list(PLATFORM_SPECS.keys()))
    with col2:
        purpose = st.selectbox("投稿の目的", ["認知拡大・告知", "エンゲージメント向上", "商品・サービスのPR", "日常の共有・ブランディング", "イベント集客"])
        additional_info = st.text_input("追加情報（任意）", placeholder="例: 渋谷駅から徒歩3分、営業時間は10〜21時")

    spec = PLATFORM_SPECS[platform]
    st.caption(f"{platform} の目安: {spec['note']}")

    if st.button("投稿文を生成する", type="primary"):
        with st.spinner("投稿文を生成中..."):
            try:
                result = write_sns_post(topic, platform, purpose, additional_info)
                st.markdown("### 生成結果（3パターン）")
                st.markdown(result)
                st.download_button("テキストをダウンロード", result, file_name="sns_posts.txt", mime="text/plain")
            except Exception as e:
                logger.error("SNS投稿文生成エラー", exc_info=True)
                st.error("エラーが発生しました。しばらくしてから再度お試しください。")
