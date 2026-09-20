import io
import random
import urllib.parse
import streamlit as st
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import google.generativeai as genai

st.set_page_config(
    page_title="令和お焚き上げ文芸館",
    page_icon="🔥",
    layout="centered"
)

# セッションステートの初期化
if "history" not in st.session_state:
    st.session_state.history = []

# --- サイドバー：APIキー設定 ---
with st.sidebar:
    st.markdown("### ⚙️ 設定")
    api_key_input = st.text_input(
        "Gemini API キー",
        type="password",
        placeholder="AIによる無限生成に必要です",
        help="Google AI Studio等で取得したAPIキーを入力してください。ブラウザ内でのみ一時的に使用されます。"
    )
    st.markdown("---")
    st.markdown("""
    **💡 ヒント**
    APIキーを設定すると、入力された「やらかし」に合わせてAIが毎回完全にオリジナルの川柳ととんちを無限に生成します！
    """)

# バラエティ番組風カスタムCSS
st.markdown("""
<style>
    .stApp {
        background-color: #0d0f18;
        color: #f3f4f6;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    
    .hero-container {
        text-align: center;
        padding: 1.8rem 1rem;
        background: linear-gradient(180deg, #1e1b4b 0%, #0d0f18 100%);
        border-bottom: 3px solid #ff2d55;
        border-radius: 0 0 20px 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(244, 63, 94, 0.15);
    }
    .main-title {
        font-size: 1.65rem;
        font-weight: 900;
        letter-spacing: -0.01em;
        background: linear-gradient(135deg, #ff2d55 0%, #ff9500 50%, #ffcc00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.4rem;
        white-space: nowrap;
    }
    .sub-title {
        color: #9ca3af;
        font-size: 0.78rem;
        font-weight: 500;
        max-width: 480px;
        margin: 0 auto;
        line-height: 1.4;
    }

    .card-senryu {
        background: #131826;
        border: 2px solid #374151;
        border-left: 6px solid #ff2d55;
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.6);
    }
    .card-tonchi {
        background: #131826;
        border: 2px solid #374151;
        border-left: 6px solid #ff9500;
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.6);
    }
    .card-art {
        background: #131826;
        border: 2px solid #374151;
        border-left: 6px solid #ffcc00;
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.6);
    }

    .section-label {
        font-weight: 700;
        font-size: 0.88rem;
        color: #f9fafb;
        margin-top: 1.2rem;
        margin-bottom: 0.4rem;
    }

    .stButton button {
        background: linear-gradient(135deg, #ff2d55 0%, #ff5e3a 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 900;
        font-size: 1.05rem;
        padding: 0.9rem 1rem;
        box-shadow: 0 6px 20px rgba(255, 45, 85, 0.4);
        width: 100%;
        letter-spacing: 0.03em;
        transition: all 0.2s ease;
    }
    .stButton button:hover {
        opacity: 0.95;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 45, 85, 0.6);
    }
</style>
""", unsafe_allow_html=True)

# ヘッダー
st.markdown("""
<div class="hero-container">
    <div class="main-title">🔥 令和お焚き上げ文芸館</div>
    <div class="sub-title">あなたの日常のやらかしや絶望を、ユーモアと毒で盛大に成仏させるバラエティ機関</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔥 新規お焚き上げ", "📜 成仏の履歴書"])

with tab1:
    st.markdown('<p class="section-label">✍️ ステップ1: やらかし・不運・黒歴史を入力する</p>', unsafe_allow_html=True)
    yarakashi_text = st.text_area(
        "",
        placeholder="例：黒かりんとうだと思ったらうんこだった",
        height=90,
        label_visibility="collapsed",
        key="input_yarakashi"
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

    if st.button("🔥 全力でお焚き上げを実行する"):
        if not yarakashi_text and uploaded_img is None:
            st.warning("⚠️ まずはやらかしの内容を入力するか、写真をアップロードしてください。")
        else:
            theme = yarakashi_text.strip() if yarakashi_text else "名もなき失態"
            
            # --- AIによる無限生成処理 ---
            senryu_text = ""
            tonchi_text = ""
            
            if api_key_input:
                try:
                    genai.configure(api_key=api_key_input)
                    # 高速かつ軽量なモデルを使用
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    prompt = f"""
                    あなたは毒舌かつユーモアあふれるバラエティ番組の構成作家です。
                    以下のユーザーの「やらかし・失敗談」を元に、次の2点を作成してください。

                    【やらかし内容】
                    {theme}

                    1. 川柳（5・7・5の形式で、哀愁と笑いを誘うもの。「〜かな」「〜けり」などの文語体や、ドヤ顔感のあるフレーズ）
                    2. とんち（「〇〇と掛けまして、××と解く。その心は……」の形式で、キレのあるオチ・ツッコミを入れたもの）

                    出力は必ず以下の形式のJSONまたはテキストで、余計な挨拶は抜きでそれぞれ明確に分けて出力してください。
                    [川柳]
                    「〜」
                    [とんち]
                    「〜」と掛けまして、〈〜〉と解く。
                    その心は……どちらも【〜】でしょう！
                    """
                    
                    with st.spinner("✨ AIがお焚き上げの文言を無限生成中..."):
                        response = model.generate_content(prompt)
                        result_str = response.text
                        
                        # 簡易パース処理
                        lines = result_str.strip().split("\n")
                        s_temp = []
                        t_temp = []
                        mode = None
                        for line in lines:
                            if "[川柳]" in line:
                                mode = "senryu"
                                continue
                            elif "[とんち]" in line:
                                mode = "tonchi"
                                continue
                            
                            if mode == "senryu":
                                s_temp.append(line)
                            elif mode == "tonchi":
                                t_temp.append(line)
                        
                        senryu_text = "\n".join(s_temp).strip()
                        tonchi_text = "\n".join(t_temp).strip()
                        
                        if not senryu_text or not tonchi_text:
                            # パースに失敗した場合は全文をそのまま割り当て
                            senryu_text = f"「気がつけば　{theme}の　悲劇かな」"
                            tonchi_text = result_str
                            
                except Exception as e:
                    st.error(f"⚠️ API生成エラー: {e}\nフォールバックとして定型モードで実行します。")
            
            # APIキー未設定、またはエラー時のフォールバック（従来のランダムプール）
            if not senryu_text or not tonchi_text:
                fallback_senryus = [
                    f"「気がつけば　{theme}の　悲劇かな」",
                    f"「全力を　注ぎ込んだ結果が　{theme}」",
                    f"「神様も　思わず二度見す　{theme}」",
                    f"「歴史とは　かくも無残な　{theme}」"
                ]
                fallback_tonchis = [
                    f"「{theme}」と掛けまして、〈サプライズゲストの登場〉と解く。\n\nその心は……どちらも【誰も望んでいないのに、盛大にやらかします】でしょう！",
                    f"「{theme}」と掛けまして、〈真冬のホラー映画〉と解く。\n\nその心は……どちらも【直視したくない現実がそこにはあります】でしょう！"
                ]
                senryu_text = random.choice(fallback_senryus)
                tonchi_text = random.choice(fallback_tonchis)
                if not api_key_input:
                    st.info("💡 サイドバーにGemini APIキーを入力すると、AIによる完全無限のオリジナル生成に切り替わります！")

            st.balloons()
            
            # 履歴に保存
            st.session_state.history.insert(0, {
                "theme": theme,
                "senryu": senryu_text,
                "tonchi": tonchi_text
            })
            
            # 画面出力
            st.markdown(f"""
            <div class="card-senryu">
                <div style="color: #ff2d55; font-weight: 800; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;">🍵 川柳館 ｜ 本日のドヤ顔一句</div>
                <h3 style="color:#f3f4f6; text-align:center; font-size: 1.15rem; font-weight: 800; letter-spacing: 0.05em; margin: 12px 0;">{senryu_text}</h3>
                <div style="color: #6b7280; font-size: 0.75rem; text-align: right; margin-top: 10px;">奉納テーマ：{theme}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="card-tonchi">
                <div style="color: #ff9500; font-weight: 800; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;">🤔 とんち館 ｜ 無理やり整いました</div>
                <div style="color:#f3f4f6; font-size:0.9rem; font-weight: 600; white-space: pre-line; line-height: 1.6; margin-top: 10px;">{tonchi_text}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # アート変換
            if uploaded_img is not None:
                st.markdown("""
                <div class="card-art">
                    <div style="color: #ffcc00; font-weight: 800; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;">🎨 美術館 ｜ 証拠品・強制モダンアート化</div>
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

            # SNSシェア導線
            st.markdown("<br>", unsafe_allow_html=True)
            share_text = f"私の上手くいかなかった出来事：【{theme}】\n\nAIに盛大にお焚き上げしてもらいました🔥\n\n#令和お焚き上げ文芸館 #今日のやらかし"
            encoded_text = urllib.parse.quote(share_text)
            twitter_url = f"https://twitter.com/intent/tweet?text={encoded_text}"
            
            st.markdown(f"""
            <div style="text-align: center; margin-top: 1.5rem; padding: 15px; background: #131826; border-radius: 12px; border: 1px dashed #374151;">
                <p style="font-size: 0.85rem; color: #9ca3af; margin-bottom: 10px;">この成仏結果を世界に共有して供養を完了する</p>
                <a href="{twitter_url}" target="_blank" style="display: inline-block; background: #000000; color: #ffffff; padding: 10px 20px; border-radius: 9999px; font-weight: 700; text-decoration: none; font-size: 0.9rem; border: 1px solid #374151;">
                    𝕏 でこのやらかしをシェアする
                </a>
            </div>
            """, unsafe_allow_html=True)

    else:
        if not st.session_state.history:
            st.info("💡 サイドバーにAPIキーを入力し、テキストや写真を準備してボタンを押すと、AIが無限のエンタメ変換結果を生み出します！")

with tab2:
    st.markdown("### 📜 過去に成仏させたやらかし一覧")
    if not st.session_state.history:
        st.info("まだお焚き上げされた歴史はありません。最初のやらかしを供養しましょう！")
    else:
        for i, item in enumerate(st.session_state.history):
            st.markdown(f"""
            <div style="background: #131826; border: 1px solid #374151; border-radius: 10px; padding: 15px; margin-bottom: 12px;">
                <div style="color: #ff2d55; font-weight: 700; font-size: 0.8rem; margin-bottom: 4px;">第 {len(st.session_state.history) - i} 回供養</div>
                <div style="font-size: 0.95rem; font-weight: 600; color: #f3f4f6; margin-bottom: 8px;">テーマ：{item['theme']}</div>
                <div style="font-size: 0.85rem; color: #9ca3af; background: #0d0f18; padding: 8px; border-radius: 6px;">
                    {item['senryu']}<br>{item['tonchi']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("🗑️ 履歴をすべて消去する"):
            st.session_state.history = []
            st.rerun()
