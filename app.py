import streamlit as st
import hashlib
import re
import asyncio

# إعداد الصفحة وتنسيق التصميم
st.set_page_config(page_title="VIP ACCESS", page_icon="👑")

st.markdown("""
    <style>
    .stApp {background-color: #0e1117 !important;}
    .main-container {
        background: #0e1117;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
    }
    .stTextInput>div>div>input {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #333 !important;
    }
    div.stButton > button {
        background-color: #00ff88 !important;
        color: black !important;
        font-weight: bold !important;
        width: 100% !important;
        border-radius: 5px !important;
    }
    .copy-btn {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #333 !important;
        width: 100% !important;
        padding: 10px !important;
        border-radius: 5px !important;
        margin-top: 10px !important;
    }
    .wa-btn {
        display: block;
        text-align: center;
        padding: 10px;
        background: #ffd700;
        color: black;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# منطق النظام
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
hwid = hashlib.md5(st.context.headers.get("User-Agent", "").encode()).hexdigest()[:10].upper()

st.markdown("<div class='main-container'>", unsafe_allow_html=True)
st.markdown("<h1>👑 VIP ACCESS</h1>", unsafe_allow_html=True)

if not st.session_state.authenticated:
    st.code(hwid, language=None)
    key_input = st.text_input("", placeholder="🔑 أدخل مفتاح التفعيل هنا")
    
    if st.button("تسجيل الدخول"):
        if key_input == hashlib.sha256((hwid + "MY_SECRET_KEY").encode()).hexdigest()[:12].upper():
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("مفتاح التفعيل غير صحيح")
            
    if st.button("📋 نسخ المعرف", key="copy"):
        st.write(f"المعرف: {hwid}")
        
    st.markdown("<a href='https://wa.me/966548607477' class='wa-btn'>💎 شراء كود VIP</a>", unsafe_allow_html=True)

else:
    st.success("تم الوصول المميز بنجاح")
    # هنا ضع محتوى لوحة تحكمك
    
st.markdown("</div>", unsafe_allow_html=True)
