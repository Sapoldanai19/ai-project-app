import streamlit as st
import google.generativeai as genai

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="AI Data Analysis Assistant", page_icon="🤖")
st.title("💬 My AI Assistant")

# 2. เชื่อมต่อ API Key จาก Secrets (ที่เราใส่ไว้ใน Streamlit Cloud)
# เปลี่ยนจากรับค่าใน Sidebar มาดึงค่าอัตโนมัติจากระบบ
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("ไม่พบ API Key ใน Secrets! กรุณาตั้งค่าใน Streamlit Cloud")
    st.stop() # หยุดการทำงานถ้าไม่มี Key

# 3. ระบบจำประวัติการคุย
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. ส่วนรับข้อความ
if prompt := st.chat_input("พิมพ์คำถามของคุณที่นี่..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # ใช้ model.generate_content โดยตรง
            response = model.generate_content(prompt)
            full_response = response.text
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")