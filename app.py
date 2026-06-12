import streamlit as st
import hashlib
import re
import asyncio

# --- 1. الإعدادات والتصميم ---
st.set_page_config(page_title="VIP ACCESS", page_icon="👑")
st.markdown("""
    <style>
    .stApp {background-color: #050505 !important;}
    .vip-card {background-color: #050505; padding: 20px; border-radius: 15px; text-align: center;}
    .stTextInput>div>div>input {background-color: #1a1a1a !important; color: #888 !important; border: 1px solid #333 !important; border-radius: 10px !important; text-align: center;}
    div.stButton>button[kind="primary"] {background-color: #00ff88 !important; color: black !important; font-weight: bold !important; width: 100% !important; height: 50px !important; border-radius: 10px !important;}
    div.stButton>button {background-color: #1a1a1a !important; color: white !important; width: 100% !important; height: 50px !important; border-radius: 10px !important; border: 1px solid #333 !important;}
    </style>
""", unsafe_allow_html=True)

# --- 2. المنطق البرمجي ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
hwid = hashlib.md5(st.context.headers.get("User-Agent", "").encode()).hexdigest()[:10].upper()

st.markdown("<div class='vip-card'>", unsafe_allow_html=True)
st.markdown("<h3 style='color: white;'>👑 VIP ACCESS</h3>", unsafe_allow_html=True)

if not st.session_state.authenticated:
    st.code(hwid, language=None)
    key_input = st.text_input("", placeholder="🔑 أدخل مفتاح التفعيل")
    if st.button("تسجيل الدخول", type="primary"):
        if key_input == hashlib.sha256((hwid + "MY_SECRET_KEY").encode()).hexdigest()[:12].upper():
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("مفتاح خاطئ")
else:
    # --- 3. لوحة تحكم البوت (المدمجة) ---
    st.write("✅ تم الدخول بنجاح")
    api_id = st.text_input("API ID")
    api_hash = st.text_input("API HASH", type="password")
    groups = st.text_area("روابط المجموعات (رابط لكل سطر)")
    msg = st.text_area("نص الرسالة")
    
    if st.button("🚀 بدء النشر الذكي"):
        from pyrogram import Client
        
        async def publish_task():
            async with Client("my_session", api_id=int(api_id), api_hash=api_hash) as app:
                for group in groups.splitlines():
                    try:
                        await app.join_chat(group)
                        await app.send_message(group, msg)
                        st.success(f"تم النشر في: {group}")
                    except Exception as e:
                        st.error(f"خطأ في {group}: {e}")
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(publish_task())
        except Exception as e:
            st.error(f"حدث خطأ في محرك البوت: {e}")

st.markdown("</div>", unsafe_allow_html=True)
