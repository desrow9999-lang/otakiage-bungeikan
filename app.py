import random
import io
import streamlit as st
from PIL import Image, ImageEnhance, ImageOps, ImageFilter

st.set_page_config(
    page_title="令和お焚き上げ文芸館",
    page_icon="🔥",
    layout="centered"
)

# プロ仕様の洗練されたカスタムCSS（モダンダーク、美しいタイポグラフィと余白）
st.markdown("""
<style>
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    
    /* ヒーローヘッダー（プロ仕様の洗練されたデザイン） */
    .hero-container {
        text-align: center;
        padding: 2.5rem 1rem 2rem 1rem;
        background: radial-gradient(circle at center, #1e1b4b 0%, #0b0f19 75%);
        border-bottom: 1px solid #1f2937;
        margin: -4rem -4rem 2rem -4rem; /* Streamlitのデフォルト余白を綺麗にまたぐ */
    }
    .main-title {
        font-size: 2.25rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #f43f5e 0%, #fb923c 50%, #facc15 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        color: #9ca3af;
        font-size: 0.95rem;
        font-weight: 400;
        max-width: 520px;
        margin: 0 auto;
        line-height: 1.5;
    }

    /* 各セクションのカード（高級感のあるシャドウとボーダー） */
    .card-senryu {
        background: #111827;
        border: 1px solid #374151;
        border-left: 4px solid #f43f5e;
        border-radius: 12px;
        padding: 24px;
        margin-top: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    .card-tonchi {
        background: #111827;
        border: 1px solid #374151;
        border-left: 4px solid #fb923c;
        border-radius: 12px;
        padding: 24px;
        margin-top: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    .card-art {
        background: #111827;
        border: 1px solid #374151;
        border-left: 4px solid #facc15;
        border-radius: 12px;
        padding: 24px;
        margin-top: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }

    .section-label {
        font-weight: 600;
        font-size: 0.95rem;
        color: #e5e7eb;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        letter-spacing: 0.02em;
    }

    /* プロっぽい洗練されたボタン */
    .stButton button {
        background: linear-gradient(135deg, #f43f5e 0%, #fb923c 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 700;
        font-size: 1rem;
        padding: 0.85rem 1rem;
        box-shadow: 0 4px 14px rgba(244, 63, 94, 0.3);
        width: 100%;
        letter-spacing: 0.03em;
        transition: all 0.2s ease;
    }
    .stButton button:hover {
        opacity: 0.95;
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(244, 63, 94, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# プロ仕様のヘッダー
st.markdown("""
<div class="hero-container">
    <div class="main-title">🔥 令和お焚き上げ文芸館</div>
    <div class="sub-title">あなたの日常のやらかしや悩みを、ユーモアとアートで盛大に成仏させる総合バラエティプラットフォーム</div>
</div>
""", unsafe_allow_html=True)

# 入力セクション
st.markdown('<p class="section-label">✍️ ステップ1: やらかし・悩みを入力する</p>', unsafe_allow_html=True)
yarakashi_text = st.text_area(
    "",
    placeholder="例：靴下に大きな穴が空いていた、大事な会議で盛大に噛んだ、など",
    height=90,
    label_visibility="collapsed"
)

st.markdown('<p class="section-label">📸 ステップ2: 証拠品（写真）をアップロード（任意）</p>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png", "webp"], label_visibility="collapsed")

uploaded_img = None
if uploaded_file is not None:
    try:
        uploaded_img = Image.open(uploaded_file)
        st.image(uploaded_img, caption="奉納された証拠品", use_container_width=True)
    except Exception as e:
        st.error(f"画像の読み込みに失敗しました: {e}")

st.markdown("<br>", unsafe_allow_html=True)

# 実行ボタン
if st.button("🔥 一網打尽でお焚き上げを実行する"):
    if not yarakashi_text and uploaded_img is None:
        st.warning("⚠️ まずはやらかしの内容を入力するか、写真をアップロードしてください。")
    else:
        st.balloons()
        
        theme = yarakashi_text.strip() if yarakashi_text else "名もなき失態"
        
        # 川柳
        senryu_templates = [
            f"「気がつけば　{theme}の　悲劇かな」",
            f"「全力を　注ぎ込んだ結果が　{theme}」",
            f"「神様も　思わず二度見す　{theme}」",
            f"「歴史とは　かくも無残な　{theme}」"
        ]
        senryu_text = random.choice(senryu_templates)
        
        st.markdown(f"""
        <div class="card-senryu">
            <div style="color: #f43f5e; font-weight: 700; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;">🍵 川柳館 ｜ 本日のドヤ顔一句</div>
            <h3 style="color:#f3f4f6; text-align:center; font-size: 1.25rem; font-weight: 700; letter-spacing: 0.05em; margin: 15px 0;">{senryu_text}</h3>
            <div style="color: #6b7280; font-size: 0.75rem; text-align: right; margin-top: 10px;">奉納テーマ：{theme}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 謎かけ
        tonchi_templates = [
            f"「{theme}」と掛けまして、〈おろしたての高級じゅうたん〉と解く。\n\nその心は……どちらも【踏み入れた瞬間に、取り返しのつかない絶望が訪れます】でしょう！",
            f"「{theme}」と掛けまして、〈サプライズゲストの登場〉と解く。\n\nその心は……どちらも【誰も望んでいないのに、盛大にやらかします】でしょう！",
            f"「{theme}」と掛けまして、〈真冬のホラー映画〉と解く。\n\nその心は……どちらも【直視したくない現実がそこにはあります】でしょう！"
        ]
        tonchi_text = random.choice(tonchi_templates)
        
        st.markdown(f"""
        <div class="card-tonchi">
            <div style="color: #fb923c; font-weight: 700; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;">🤔 とんち館 ｜ 無理やり整いました</div>
            <div style="color:#f3f4f6; font-size:0.95rem; font-weight: 600; white-space: pre-line; line-height: 1.6; margin-top: 10px;">{tonchi_text}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # アート
        if uploaded_img is not None:
            st.markdown("""
            <div class="card-art">
                <div style="color: #facc15; font-weight: 700; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;">🎨 美術館 ｜ 証拠品・強制モダンアート化</div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.spinner("高衝撃変形エンジン作動中..."):
                img = uploaded_img.convert("RGB")
                img = ImageEnhance.Contrast(img).enhance(3.0)
                
                styles = ["ネオン・フロー", "グリッチ・ポップ", "抽象的破片"]
                chosen = random.choice(styles)
                
                if chosen == "ネオン・フロー":
                    img = ImageOps.solarize(img, threshold=100).convert("RGB")
                elif chosen == "グリッチ・ポップ":
                    edges = img.filter(ImageFilter.FIND_EDGES).convert("RGB")
                    img = Image.blend(img, edges, alpha=0.5)
                else:
                    img = img.filter(ImageFilter.DETAIL)
                
                st.success(f"✨ 演出スタイル「{chosen}」で盛大に成仏しました！")
                st.image(img, use_container_width=True)
                
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                st.download_button("📥 成仏アートをダウンロード (PNG)", data=buf.getvalue(), file_name="otakiage-art.png", mime="image/png")
else:
    st.info("💡 テキストや写真を準備してボタンを押すと、すべてのエンタメ変換結果が一気に縦に飛び出します！")
