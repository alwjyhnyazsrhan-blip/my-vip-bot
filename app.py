import streamlit as st
import hashlib
import asyncio
import os

# إعداد المتغيرات البيئية لـ Pyrogram
os.environ["PYROGRAM_SKIP_TELETHON_SYNC"] = "1"
from pyrogram import Client

# --- 1. الإعدادات ---
st.set_page_config(page_title="VIP ACCESS", page_icon="👑")

st.markdown("""
    <style>
    .stApp {background-color: #050505 !important;}
    .vip-card {background-color: #1a1a1a; padding: 20px; border-radius: 15px; color: white;}
    div.stButton > button[kind="primary"] {background-color: #00ff88 !important; color: black !important; font-weight: bold !important; width: 100%;}
    </style>
""", unsafe_allow_html=True)

# --- 2. المنطق ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False

# توليد معرف الجهاز (HWID)
hwid = hashlib.md5(st.context.headers.get("User-Agent", "").encode()).hexdigest()[:10].upper()

st.markdown("<div class='vip-card'>", unsafe_allow_html=True)
st.markdown("<h1>👑 VIP ACCESS</h1>", unsafe_allow_html=True)

if not st.session_state.authenticated:
    st.write("معرف جهازك:")
    st.code(hwid, language=None)
    key_input = st.text_input("", placeholder="🔑 أدخل مفتاح التفعيل")
    
    # مفتاح التفعيل يعتمد على الـ HWID المدخل
    if st.button("تسجيل الدخول", type="primary"):
        correct_key = hashlib.sha256((hwid + "MY_SECRET_KEY").encode()).hexdigest()[:12].upper()
        if key_input == correct_key:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("مفتاح التفعيل غير صحيح")

else:
    st.success("تم الدخول بنجاح")
    api_id = st.text_input("API ID")
    api_hash = st.text_input("API HASH", type="password")
    groups_raw = st.text_area("روابط المجموعات (رابط لكل سطر)")
    msg = st.text_area("نص الرسالة")
    
    if st.button("🚀 بدء النشر"):
        async def publish_task():
            async with Client("my_session", api_id=int(api_id), api_hash=api_hash) as app:
                for group in groups_raw.splitlines():
                    if group.strip():
                        try:
                            await app.join_chat(group)
                            await app.send_message(group, msg)
                            st.write(f"✅ تم النشر في: {group}")
                        except Exception as e:
                            st.error(f"⚠️ خطأ في {group}: {e}")

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(publish_task())
        except Exception as e:
            st.error(f"خطأ في محرك البوت: {e}")

st.markdown("</div>", unsafe_allow_html=True)
