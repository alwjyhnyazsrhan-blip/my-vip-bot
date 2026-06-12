import streamlit as st
import hashlib
import asyncio
import os

# إعداد الصفحة
st.set_page_config(page_title="VIP ACCESS", page_icon="👑")

# المنطق البرمجي
if 'authenticated' not in st.session_state: st.session_state.authenticated = False

hwid = hashlib.md5(st.context.headers.get("User-Agent", "").encode()).hexdigest()[:10].upper()

if not st.session_state.authenticated:
    st.write(f"معرف جهازك: `{hwid}`")
    key_input = st.text_input("🔑 أدخل مفتاح التفعيل")
    
    if st.button("تسجيل الدخول"):
        correct_key = hashlib.sha256((hwid + "MY_SECRET_KEY").encode()).hexdigest()[:12].upper()
        if key_input == correct_key:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("مفتاح التفعيل غير صحيح")
else:
    api_id = st.text_input("API ID")
    api_hash = st.text_input("API HASH", type="password")
    groups_raw = st.text_area("روابط المجموعات")
    msg = st.text_area("نص الرسالة")
    
    if st.button("🚀 بدء النشر"):
        # 1. الاستيراد هنا داخل الدالة يحل مشكلة الـ Import Error
        os.environ["PYROGRAM_SKIP_TELETHON_SYNC"] = "1"
        from pyrogram import Client
        
        async def run_bot():
            async with Client("my_session", api_id=int(api_id), api_hash=api_hash) as app:
                for group in groups_raw.splitlines():
                    try:
                        await app.join_chat(group.strip())
                        await app.send_message(group.strip(), msg)
                        st.success(f"تم النشر في: {group}")
                    except Exception as e:
                        st.error(f"خطأ في {group}: {e}")
        
        # 2. تشغيل الـ Loop
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(run_bot())
        except Exception as e:
            st.error(f"خطأ تقني: {e}")
