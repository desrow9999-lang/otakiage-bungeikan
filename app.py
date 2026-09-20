import random
import io
import streamlit as st
from PIL import Image, ImageEnhance, ImageOps, ImageFilter

st.set_page_config(
    page_title="令和お焚き上げ文芸館",
    page_icon="🔥",
    layout="centered"
)

# スタイリッシュ＆お笑い風のカスタムCSS（タイトルと文章のバランスを調整）
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #090a0f 0%, #1a1c29 100%);
        color: #fafaef;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .header-container {
        text-align: center;
        padding: 1.5rem 0 1rem 0;
    }
    .main-title {
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #ff3366 0%, #ff9933 50%, #ffff33 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .sub-title {
        color: #9ca3af;
        font-size: 0.85rem;
        margin-bottom: 1.5rem;
        line-height: 1.4;
    }
    .card-senryu {
        background: linear-gradient(145deg, #1f2937 0%, #111827 100%);
        border: 2px solid #ff3366;
        border-radius: 16px;
        padding: 20px;
        margin-top: 15px;
        box-shadow: 0 8px 24px rgba(255, 51, 102, 0.2);
    }
    .card-tonchi {
        background: linear-gradient(145deg, #1f2937 0%, #111827 100%);
        border: 2px solid #ff9933;
        border-radius: 16px;
        padding: 20px;
        margin-top: 15px;
        box-shadow: 0 8px 24px rgba(255, 153, 51, 0.2);
    }
    .section-header {
        font-weight: 700;
        font-size: 1rem;
        color: #e5e7eb;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .stButton button {
        background: linear-gradient(135deg, #ff3366 0%, #ff9933 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1.05rem;
        padding: 0.8rem 1rem;
        box-shadow: 0 6px 20px rgba(255, 51, 102, 0.4);
        width: 100%;
        letter-spacing: 0.05em;
    }
    .stButton button:hover {
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# ヘッダー部分のバランスを調整
st.markdown("""
<div class="header-container">
    <div class="main-title">🔥 令和お焚き上げ文芸館</div>
    <div class="sub-title">あなたのやらかしを、笑いとアートで盛大に成仏させる総合バラエティ</div>
</div>
""", unsafe_allow_html=True)

# 入力セクション
st.markdown('<p class="section-header">✍️ ステップ1: やらかし・悩みをブチ込む</p>', unsafe_allow_html=True)
yarakashi_text = st.text_area(
    "",
    placeholder="例：靴下に穴が空いていた、会議で盛大に噛んだ、など",
    height=80,
    label_visibility="collapsed"
)

st.markdown('<p class="section-header">📸 ステップ2: 証拠品（写真）を添える（任意）</p>', unsafe_allow_html=True)
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
if st.button("🔥 一網打尽でお焚き上げする（ガチャ回転）"):
    if not yarakashi_text and uploaded_img is None:
        st.warning("⚠️ まずはやらかしの内容を入力するか、写真をアップロードしてください！")
    else:
        st.balloons()
        
        # 1. よりテーマに絡んだセンスのある川柳生成ロジック
        theme = yarakashi_text.strip() if yarakashi_text else "名もなき失態"
        
        senryu_templates = [
            f"「気がつけば　{theme}の　悲劇かな」",
            f"「全力を　注ぎ込んだ結果が　{theme}」",
            f"「神様も　思わず二度見す　{theme}」",
            f"「歴史とは　かくも無残な　{theme}」"
        ]
        senryu_text = random.choice(senryu_templates)
        
        st.markdown(f"""
        <div class="card-senryu">
            <div style="color: #ff3366; font-weight: bold; font-size: 0.85rem; margin-bottom: 5px;">🍵 【川柳館】本日のドヤ顔一句</div>
            <h3 style="color:#fafaef; text-align:center; letter-spacing:0.08em; margin: 15px 0;">{senryu_text}</h3>
            <p style="color:#9ca3af; font-size:0.8rem; text-align:right; margin:0;">奉納テーマ：{theme}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 2. より機知に富んだ謎かけ生成ロジック
        tonchi_templates = [
            f"「{theme}」と掛けまして、〈おろしたての高級じゅうたん〉と解く。\n\nその心は……どちらも【踏み入れた瞬間に、取り返しのつかない絶望（穴・シミ）が訪れます】でしょう！",
            f"「{theme}」と掛けまして、〈サプライズゲストの登場〉と解く。\n\nその心は……どちらも【誰も望んでいないのに、盛大にやらかします】でしょう！",
            f"「{theme}」と掛けまして、〈真冬のホラー映画〉と解く。\n\nその心は……どちらも【直視したくない現実がそこにはあります】でしょう！"
        ]
        tonchi_text = random.choice(tonchi_templates)
        
        st.markdown(f"""
        <div class="card-tonchi">
            <div style="color: #ff9933; font-weight: bold; font-size: 0.85rem; margin-bottom: 5px;">🤔 【とんち館】無理やり整いました！</div>
            <p style="color:#fafaef; font-size:0.95rem; font-weight:bold; white-space: pre-line; line-height: 1.5; margin: 10px 0;">{tonchi_text}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 3. 美術館アート生成（写真がある場合）
        if uploaded_img is not None:
            st.markdown("""
            <div style="background: linear-gradient(145deg, #1f2937 0%, #111827 100%); border: 2px solid #ffff33; border-radius: 16px; padding: 20px; margin-top: 15px; box-shadow: 0 8px 24px rgba(255, 255, 51, 0.2);">
                <div style="color: #ffff33; font-weight: bold; font-size: 0.85rem; margin-bottom: 5px;">🎨 【美術館】証拠品・強制モダンアート化</div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.spinner("高衝撃変形エンジン作動中... 🚀"):
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
