import streamlit as st
import hashlib
import re
import asyncio
from pyrogram import Client

# --- 1. الإعدادات والتصميم ---
st.set_page_config(page_title="VIP ACCESS", page_icon="👑")
st.markdown("""
    <style>
    .stApp {background-color: #0e1117;}
    .vip-card {text-align: center; padding: 20px; border: 1px solid #333; border-radius: 15px; background: #121212;}
    .stButton>button {width: 100%; background-color: #00ff88; color: black; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

# --- 2. دوال النظام ---
def check_key(hwid, key):
    # يمكنك تغيير "MY_SECRET_KEY" لأي كلمة سر خاصة بك
    return key == hashlib.sha256((hwid + "MY_SECRET_KEY").encode()).hexdigest()[:12].upper()

def clean_groups(raw_input):
    urls = re.findall(r'(https?://t\.me/[+a-zA-Z0-9_]+|t\.me/[+a-zA-Z0-9_]+)', raw_input)
    return list(set(urls))

# --- 3. المنطق الأساسي ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
hwid = hashlib.md5(st.context.headers.get("User-Agent", "").encode()).hexdigest()[:10].upper()

# --- 4. الواجهة ---
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center;'>👑 VIP ACCESS</h1>", unsafe_allow_html=True)
    st.code(hwid, language=None)
    key_input = st.text_input("🔑 أدخل مفتاح التفعيل هنا:")
    
    if st.button("تسجيل الدخول"):
        if check_key(hwid, key_input):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("مفتاح التفعيل غير صحيح!")
            
    st.markdown("""
        <a href="https://wa.me/966548607477" style="display: block; text-align: center; 
        padding: 10px; background: #ffd700; color: black; border-radius: 5px; text-decoration: none; font-weight: bold;">
        💎 شراء كود VIP
        </a>
    """, unsafe_allow_html=True)

else:
    # --- 5. لوحة التحكم بعد الدخول ---
    st.title("🚀 لوحة التحكم")
    api_id = st.text_input("API ID")
    api_hash = st.text_input("API HASH", type="password")
    groups_raw = st.text_area("أدخل روابط المجموعات (يمكنك لصق نص كامل):")
    message = st.text_area("نص الرسالة:")
    
    if st.button("بدء النشر الذكي"):
        groups = clean_groups(groups_raw)
        st.write(f"تم تنظيم {len(groups)} مجموعة.")
        # هنا يمكنك استدعاء دالة النشر (smart_publisher)
        st.success("جاري النشر في المجموعات...")
