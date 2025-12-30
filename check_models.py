import google.generativeai as genai
import os

# 在這裡填入你的 API KEY，或者設定環境變數
API_KEY = "AIzaSyBYV439MtEMCXTinWI4zGgnpIwVj3FE1Pg"

def list_google_models():
    if not API_KEY:
        print("❌ 錯誤：請先在程式碼中填入 API Key")
        return

    try:
        genai.configure(api_key=API_KEY)
        print(f"正在連線 Google 查詢可用模型...\n")
        
        print(f"{'模型名稱 (Model Name)':<40} | {'顯示名稱 (Display Name)'}")
        print("-" * 70)
        
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                # 只顯示支援「對話/生成內容」的模型
                print(f"{m.name:<40} | {m.display_name}")
                
    except Exception as e:
        print(f"發生錯誤：{e}")

if __name__ == "__main__":
    list_google_models()