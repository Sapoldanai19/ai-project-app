import streamlit as st
import google.generativeai as genai

# เพิ่ม 2 บรรทัดนี้ลงไปครับ
st.subheader("🔍 System Check")
st.write(f"Library Version: `{genai.__version__}`")

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="AI Assistant", page_icon="🤖")
st.title("💬 My AI Assistant")

# 2. เชื่อมต่อ API ผ่าน Secrets (ไม่ต้องพิมพ์ Key ในหน้าเว็บแล้ว)
try:
    # ดึงค่าจากที่ตั้งไว้ใน Advanced Settings > Secrets
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # ใช้รุ่น 1.5 Flash
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("กรุณาตั้งค่า GEMINI_API_KEY ใน Streamlit Secrets ก่อนนะครับ")
    st.stop()

# 3. ส่วนของระบบแชท (เหมือนเดิมที่คุณทำไว้)
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("พิมพ์คำถามของคุณที่นี่..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # เพิ่มการตั้งค่าเพื่อความปลอดภัยในการเรียกใช้
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")