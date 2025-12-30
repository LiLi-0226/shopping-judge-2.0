import streamlit as st

# 定義主題顏色
THEME_COLOR = "#1A237E"  # 深靛藍
ACCENT_COLOR = "#FFC107" # 金黃色

def render_header():
    """顯示靛藍色滿版標題"""
    st.markdown(f"""
        <style>
        /* 1. 修正側邊欄消失問題：移除隱藏 header 的代碼 */
        .block-container {{
            padding-top: 1rem !important;
            max-width: 100% !important;
        }}
        .stApp {{ background-color: white !important; }}

        /* 靛藍色滿版標題框 */
        .indigo-full-header {{
            background-color: {THEME_COLOR};
            width: 100vw;
            margin-left: calc(-50vw + 50%);
            padding: 20px 0;
            text-align: center;
            box-shadow: 0 4px 12px rgba(26, 35, 126, 0.2);
            margin-top: -3rem; /* 往上拉一點 */
            margin-bottom: 30px;
        }}
        .indigo-full-header h1 {{
            color: white !important;
            font-size: 40px !important;
            font-weight: 900 !important;
            margin: 0 !important;
            letter-spacing: 6px;
        }}
        .indigo-full-header p {{
            color: #E0E0E0 !important;
            font-size: 16px !important;
            font-weight: 400 !important;
            margin-top: 8px !important;
            letter-spacing: 2px;
        }}

        /* 歷史紀錄區塊樣式 */
        .history-section {{
            margin-bottom: 20px !important;
            padding: 0 2%;
        }}
        
        /* 強化標題字體 */
        h3 {{
            font-size: 28px !important;
            font-weight: 900 !important;
            color: {THEME_COLOR} !important;
            border-left: 6px solid {THEME_COLOR};
            padding-left: 15px;
            margin-bottom: 20px !important;
        }}
        </style>
       
        <div class="indigo-full-header">
            <h1>購物大判官</h1>
            <p>AI 毒舌決策輔助系統</p>
        </div>
    """, unsafe_allow_html=True)

def render_history_selector(history_list):
    """在標題下方顯示歷史紀錄下拉選單"""
    st.markdown('<div class="history-section">', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1]) 
    with col2:
        # 使用 session_state 綁定 Key
        options = ["請選擇要回顧的判決..."]
        if history_list:
            for i, record in enumerate(history_list):
                options.append(f"#{len(history_list)-i} | {record['time'][5:]} [{record['style'][:2]}]")
        
        selected_option = st.selectbox(
            "🗄️ 調閱歷史卷宗", # 加上標題比較清楚
            options, 
            key="history_selectbox"
        )
        
        if selected_option != options[0]:
            idx_str = selected_option.split('#')[1].split(' |')[0]
            real_index = len(history_list) - int(idx_str)
            return real_index
        return None
    st.markdown('</div>', unsafe_allow_html=True)

def render_inputs():
    """顯示商品輸入區域 (已移除 Tab 分頁)"""
    
    st.markdown("<p style='font-size: 22px !important; margin: 0 0 30px 0; color: #555; text-align:center;'>請輸入兩位選手資訊，讓 AI 幫你斬斷雜念。</p>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        st.markdown("### 📦 選手 A")
        product_a = st.text_area("商品 A 資訊", height=280, placeholder="貼上商品 A 的規格、價格、描述...", key="input_a_main", label_visibility="collapsed")
    with col_b:
        st.markdown("### 📦 選手 B")
        product_b = st.text_area("商品 B 資訊", height=280, placeholder="貼上商品 B 的規格、價格、描述...", key="input_b_main", label_visibility="collapsed")
    
    return product_a, product_b

def render_judge_button():
    """高對比度的大型按鈕"""
    st.markdown(f"""
        <style>
        div.stButton > button {{
            background-color: {ACCENT_COLOR} !important;
            color: {THEME_COLOR} !important;
            font-size: 32px !important;
            font-weight: 900 !important;
            height: 80px !important;
            border-radius: 12px !important;
            border: 3px solid {THEME_COLOR} !important;
            margin-top: 30px;
            box-shadow: 0 8px 15px rgba(0,0,0,0.1);
        }}
        div.stButton > button:hover {{
            background-color: #FFD54F !important;
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.15);
        }}
        </style>
    """, unsafe_allow_html=True)
    return st.button("🔨 啟動判決模式 🔨", use_container_width=True)

def show_error(msg): 
    st.error(f"⛔ 發生錯誤：{msg}", icon="🚫")
def show_warning(msg): 
    st.warning(msg, icon="⚠️")

def show_result(result_text):
    st.divider()
    st.markdown(f"<h2 style='color: {THEME_COLOR}; font-size: 36px; font-weight: 900; text-align:center; margin-bottom: 30px;'>📄 最終判決書</h2>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style='border: 4px solid {THEME_COLOR}; padding: 40px; border-radius: 16px;
                    background-color: #FFFFFF; font-size: 20px; font-weight: 500; color: #333;
                    box-shadow: 0 10px 30px rgba(26, 35, 126, 0.15); line-height: 1.6;'>
            {result_text}
        </div>
    """, unsafe_allow_html=True)

def show_history_detail(record):
    """顯示單筆歷史紀錄"""
    st.divider()
    st.markdown(f"<h2 style='color: {THEME_COLOR}; text-align:center;'>📜 歷史卷宗回顧</h2>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 30px; padding: 10px; background: #F0F2FA; border-radius: 8px; color: {THEME_COLOR};'>
        📅 審判時間：<b>{record['time']}</b> &nbsp;|&nbsp; 
        🎭 值班法官：<b>{record['style']}</b>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("### 📦 當時選手 A")
        st.text_area("", record['a'], height=200, disabled=True, key="hist_a", label_visibility="collapsed")
    with col2:
        st.markdown("### 📦 當時選手 B")
        st.text_area("", record['b'], height=200, disabled=True, key="hist_b", label_visibility="collapsed")
    
    show_result(record['result'])