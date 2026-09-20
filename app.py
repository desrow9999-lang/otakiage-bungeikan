import random
import io
import streamlit as st
from PIL import Image, ImageEnhance, ImageOps, ImageFilter

st.set_page_config(
    page_title="令和お焚き上げ文芸館",
    page_icon="🔥",
    layout="centered"
)

st.markdown("""
<style>
    .stApp {
        background-color: #0d0f19;
        color: #fafaef;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .main-title {
        font-size: 2.0rem;
        font-weight: 700;
        letter-spacing: -0.04em;
        background: linear-gradient(135deg, #ff7e5f 0%, #feb47b 50%, #e6ff6f 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .sub-title {
        color: #9ca3af;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
    }
    .stButton button {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.8rem 1rem;
        box-shadow: 0 4px 12px rgba(255, 65, 108, 0.3);
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🔥 令和お焚き上げ文芸館</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">あなたの日常のやらかし・失敗・悩みを、笑いとアートに昇華させて供養する総合アミューズメント</p>', unsafe_allow_html=True)

# セッション状態の初期化（入力内容をタブ間で共有するため）
if "yarakashi_text" not in st.session_state:
    st.session_state.yarakashi_text = ""
if "uploaded_img" not in st.session_state:
    st.session_state.uploaded_img = None

# タブの定義
tab1, tab2, tab3, tab4 = st.tabs(["🔥 お焚き上げ入力", "🍵 川柳館", "🤔 とんち館", "🎨 美術館ガチャ"])

with tab1:
    st.markdown("### ✍️ やらかし・悩みを奉納する")
    st.session_state.yarakashi_text = st.text_area(
        "最近やらかしたこと、失敗、愚痴などを入力してください",
        value=st.session_state.yarakashi_text,
        placeholder="例：ダイエット中なのに夜中にホールケーキを一人で食いつぶした"
    )
    
    st.markdown("### 📸 証拠品（写真）をアップロード（任意）")
    uploaded_file = st.file_uploader("ブレた写真や失敗の証拠", type=["jpg", "jpeg", "png", "webp"])
    if uploaded_file is not None:
        st.session_state.uploaded_img = Image.open(uploaded_file)
        st.image(st.session_state.uploaded_img, caption="奉納された証拠品", use_container_width=True)
        
    st.success("✨ 入力完了！上のタブ（川柳館・とんち館・美術館）に移動して、お焚き上げ結果を確認しよう！")

with tab2:
    st.markdown("### 🍵 川柳館（五・七・五で供養）")
    if st.button("✨ 川柳に変換する"):
        text = st.session_state.yarakashi_text
        if not text:
            st.warning("まずは最初のタブで「やらかし」を入力してください！")
        else:
            # サンプルの川柳生成ロジック（後でAIや高度な置換に進化可能）
            phrases_5 = ["深夜の罠", "財布が泣く", "後の祭り", "魔が差した", "冷や汗が"]
            phrases_7 = ["甘い誘惑負けて食う", "電車の中で爆睡す", "気づいた時にはもう遅い", "全額おごりで顔面蒼白"]
            phrases_5_end = ["あぁ無常", "明日から本気", "笑うしかない", "天罰覿面"]
            
            senryu = f"「{random.choice(phrases_5)}　{random.choice(phrases_7)}　{random.choice(phrases_5_end)}」"
            st.markdown(f"""
            <div style="background:#1f2937; padding:20px; border-radius:12px; border-left: 5px solid #ff416c; text-align:center;">
                <h2 style="color:#fafaef; letter-spacing: 0.1em;">{senryu}</h2>
                <p style="color:#9ca3af; font-size:0.85rem; margin-top:10px;">奉納文：{text}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("ボタンを押すと、あなたの失敗が風流な（自虐的な）川柳に生まれ変わります。")

with tab3:
    st.markdown("### 🤔 とんち館（ねづっち風謎かけ）")
    if st.button("🧠 謎かけで無理やり解決する"):
        text = st.session_state.yarakashi_text
        if not text:
            st.warning("まずは最初のタブで「やらかし」を入力してください！")
        else:
            tonchi = f"「{text[:10]}...」と掛けまして、〈真冬の冷蔵庫〉と解く。\n\nその心は……どちらも【開けた瞬間、冷や汗（冷気）が出ます】でしょう！"
            st.markdown(f"""
            <div style="background:#1f2937; padding:20px; border-radius:12px; border-left: 5px solid #feb47b;">
                <p style="font-size:1.1rem; color:#fafaef; font-weight:bold; white-space: pre-line;">{tonchi}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("ボタンを押すと、どんな悩みも強引なとんちでオチにされます。")

with tab4:
    st.markdown("### 🎨 美術館（失敗写真アートガチャ）")
    if st.session_state.uploaded_img is not None:
        if st.button("🎲 失敗写真をお焚き上げアートに変換"):
            with st.spinner("高衝撃変形エンジン作動中... 🔥"):
                img = st.session_state.uploaded_img.convert("RGB")
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
                
                st.success(f"✨ 演出スタイル「{chosen}」でモダンアートとして成仏しました！")
                st.image(img, use_container_width=True)
                
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                st.download_button("📥 現代アートをダウンロード", data=buf.getvalue(), file_name="otakiage-art.png", mime="image/png")
    else:
        st.warning("最初のタブで「証拠品（写真）」をアップロードすると、ここでアートガチャが回せるようになります！")
