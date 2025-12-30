import streamlit as st
import config

def render_sidebar():
    """
    渲染側邊欄：只保留風格選擇，模型已鎖定
    回傳: (api_key, selected_style_name, selected_model)
    """
    # 1. 讀取 API Key
    api_key = config.API_KEY
    
    # 2. 自動鎖定唯一的模型 (讀取列表中的第一個)
    selected_model = config.AVAILABLE_MODELS[0]
    
    with st.sidebar:
        st.header("⚙️ 設定面板")
        
        # 顯示目前鎖定的模型 (純資訊，不可修改)
        st.info(f"🔒 AI 核心已鎖定：\n**{selected_model}**")
        
        st.divider()
        
        # --- 風格選擇 ---
        st.header("🎭 判官性格")
        style_options = list(config.JUDGE_STYLES.keys())
        selected_style = st.selectbox(
            "選擇毒舌程度：",
            style_options
        )
        
        st.markdown("---")
        
    # 依然回傳 3 個值，讓主程式 app.py 不需要修改
    return api_key, selected_style, selected_model