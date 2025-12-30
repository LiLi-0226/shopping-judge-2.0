import google.generativeai as genai

def get_verdict(api_key, model_name, product_a, product_b, system_instruction):
    """
    接收商品資訊與人格指令，呼叫 Gemini。
    """
    # 1. 設定 API
    genai.configure(api_key=api_key)
    
    # 設定生成參數
    # ⚠️ 修正：將 token 上限提高到 8192，避免回答到一半被切掉
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192, 
    }
    
    # 2. 初始化模型
    model = genai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config,
        system_instruction=system_instruction
    )

    # 3. 定義 User Prompt
    # 優化：強調「詳細」與「完整」，避免 AI 偷懶
    user_prompt = f"""
    請審判以下兩個商品：

    【📦 選手 A 資訊】：
    {product_a}
    
    --------------------
    
    【📦 選手 B 資訊】：
    {product_b}
    
    ---
    【輸出格式要求】：
    請務必遵守你的「角色設定」語氣，並確保回答**完整且詳細**，不要中斷。
    輸出結構如下：
    1. **⚖️ 一針見血短評**：用一句話總結這場對決。
    2. **⚔️ 規格殘酷對決表**：請列出**詳細的** Markdown 表格，比較關鍵優缺點、規格數據與價格。
    3. **🔥 最終判決書**：詳細的分析與建議，字數不限，請盡情發揮你的毒舌/理智評論。
    """

    # 4. 發送請求
    chat = model.start_chat(history=[])
    response = chat.send_message(user_prompt)
    
    return response.text