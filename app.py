import streamlit as st
import config
import auth
import ui
import ai_judge
from datetime import datetime

# 1. 設定頁面
config.setup_page()

if "history" not in st.session_state:
    st.session_state.history = []

# --- 定義 Callback 函數 ---
def reset_history_selection():
    """
    當使用者點擊「返回」時觸發此函數。
    這會在頁面重新渲染前，先把下拉選單歸零。
    """
    st.session_state["history_selectbox"] = "請選擇要回顧的判決..."

# 2. 渲染側邊欄
api_key, judge_style_name, model_name = auth.render_sidebar()

# 3. 渲染標題
ui.render_header()

# 4. 歷史紀錄選單
selected_history_index = ui.render_history_selector(st.session_state.history)

# --- 核心邏輯 ---
# 情況 A：查看歷史紀錄
if selected_history_index is not None:
    record = st.session_state.history[selected_history_index]
    ui.show_history_detail(record)
    
    st.write("")
    col_back, _ = st.columns([1, 4])
    with col_back:
        # 使用 on_click 參數來觸發狀態重置
        st.button(
            "⬅️ 返回判決主畫面", 
            type="primary", 
            use_container_width=True, 
            on_click=reset_history_selection
        )

# 情況 B：顯示輸入介面
else:
    item_a, item_b = ui.render_inputs()

    # 確保兩欄都有輸入才顯示按鈕
    if item_a and item_b:
        if ui.render_judge_button():
            
            # --- API Key 檢查 (關鍵修復區域) ---
            final_api_key = api_key 
            
            # 嘗試讀取 Streamlit Secrets (雲端部署用)
            # 使用 try-except 包起來，避免在本機因為找不到檔案而崩潰
            try:
                # 只有在真的有 secrets 且裡面有 KEY 時才覆蓋
                if "GOOGLE_API_KEY" in st.secrets:
                    final_api_key = st.secrets["GOOGLE_API_KEY"]
            except Exception:
                # 發生錯誤(例如本機沒有 secrets 檔)，就忽略，繼續使用 config.py 的 Key
                pass

            # 防呆檢查
            if not final_api_key or "填在這裡" in final_api_key:
                ui.show_error("❌ API Key 無效！請檢查 config.py。")
                st.stop()
            
            try:
                # 顯示載入動畫
                spinner_text = f"⚖️ 【{judge_style_name}】正在審閱卷宗..."
                with st.spinner(spinner_text):
                    
                    system_prompt = config.JUDGE_STYLES[judge_style_name]
                    
                    # 呼叫 AI
                    result = ai_judge.get_verdict(final_api_key, model_name, item_a, item_b, system_prompt)
                    
                    # 儲存紀錄
                    new_record = {
                        "a": item_a,
                        "b": item_b,
                        "result": result,
                        "style": judge_style_name,
                        "model": model_name,
                        "time": datetime.now().strftime("%Y/%m/%d %H:%M")
                    }
                    st.session_state.history.insert(0, new_record)
                    
                    # 顯示結果
                    ui.show_result(result)
                    
            except Exception as e:
                error_msg = str(e)
                if "404" in error_msg or "models/" in error_msg:
                    ui.show_error(f"⚠️ 模型錯誤：Google 可能尚未開放 '{model_name}'。\n請到 config.py 切換回 'gemini-2.5-flash' 試試看。")
                elif "429" in error_msg:
                    ui.show_error("⚠️ 額度不足 (429)：請檢查你的 API Key 額度，或稍後再試。")
                else:
                    ui.show_error(f"AI 審判失敗：{error_msg}")
    
    elif item_a or item_b:
        st.info("💡 請完整輸入兩位選手的資訊，審判按鈕才會出現喔！")