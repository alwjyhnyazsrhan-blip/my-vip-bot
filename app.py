import streamlit as st
import hashlib
import re
import asyncio

# --- الإعدادات وتنسيق التصميم الاحترافي ---
st.set_page_config(page_title="VIP ACCESS", page_icon="👑")

st.markdown("""
    <style>
    /* تغيير لون خلفية الصفحة بالكامل */
    .stApp {
        background-color: #0e1117 !important;
    }
    /* تصميم البطاقة المركزية */
    .vip-card {
        background-color: #1a1a1a;
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #333;
        text-align: center;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
    }
    /* تنسيق زر تسجيل الدخول */
    div.stButton > button:first-child {
        background-color: #00ff88;
        color: #000;
        font-weight: bold;
        width: 100%;
        border-radius: 10px;
    }
    /* تنسيق النصوص */
    h1 { color: white !important; }
    </style>
""", unsafe_allow_html=True)

# --- منطق الكود ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
hwid = hashlib.md5(st.context.headers.get("User-Agent", "").encode()).hexdigest()[:10].upper()

# --- بناء الواجهة (مغلفة داخل حاوية لتنسيقها) ---
st.markdown("<div class='vip-card'>", unsafe_allow_html=True)
st.markdown("<h1>👑 VIP ACCESS</h1>", unsafe_allow_html=True)

if not st.session_state.authenticated:
    st.code(hwid, language=None)
    key_input = st.text_input("🔑 أدخل مفتاح التفعيل هنا:")
    
    if st.button("تسجيل الدخول"):
        # منطق التحقق (نفس الذي استخدمناه سابقاً)
        secret_salt = "MY_SECRET_KEY"
        valid_key = hashlib.sha256((hwid + secret_salt).encode()).hexdigest()[:12].upper()
        if key_input == valid_key:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("مفتاح التفعيل غير صحيح!")
            
    # زر شراء الكود (تنسيق ذهبي)
    st.markdown("""
        <a href="https://wa.me/966548607477" style="display: block; text-align: center; 
        padding: 10px; background: #ffd700; color: black; border-radius: 10px; text-decoration: none; font-weight: bold; margin-top: 10px;">
        💎 شراء كود VIP
        </a>
    """, unsafe_allow_html=True)
else:
    st.success("تم الدخول بنجاح!")
    # هنا ضع محتويات لوحة التحكم الخاصة بك
st.markdown("</div>", unsafe_allow_html=True)
