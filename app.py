import streamlit as st
import pandas as pd
import google.generativeai as genai
import os

st.set_page_config(page_title="AI Data Analyst", layout="wide")
st.title("📊 AI Data Analysis Assistant")

# ดึง API Key จากระบบ (สำหรับ Render)
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    # ใช้รุ่น flash-latest เพื่อความใหม่ล่าสุด
    model = genai.GenerativeModel('gemini-1.0-pro')
else:
    st.error("กรุณาตั้งค่า GEMINI_API_KEY ใน Environment Variables")

uploaded_file = st.file_uploader("อัปโหลดไฟล์ CSV หรือ Excel", type=["csv", "xlsx"])

if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    st.subheader("ตัวอย่างข้อมูล (Preview)")
    st.dataframe(df.head(5))

    st.subheader("💬 ถาม AI เกี่ยวกับข้อมูลชุดนี้")
    user_query = st.text_input("ถามอะไรดี?")

    if user_query:
        data_info = f"Columns: {', '.join(df.columns)}\nData:\n{df.head(3).to_string()}"
        prompt = f"{data_info}\n\nคำถาม: {user_query}"
        
        with st.spinner('AI กำลังคิด...'):
            try:
                response = model.generate_content(prompt)
                st.info(response.text)
            except Exception as e:
                st.error(f"Error: {e}")