import streamlit as st
import hashlib
import asyncio
import os
import nest_asyncio

# تفعيل nest_asyncio للسماح بالـ Loops المتداخلة داخل Streamlit
nest_asyncio.apply()

# إعداد المتغيرات قبل استيراد Pyrogram
os.environ["PYROGRAM_SKIP_TELETHON_SYNC"] = "1"
from pyrogram import Client

st.set_page_config(page_title="VIP ACCESS", page_icon="👑")

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
    groups_raw = st.text_area("روابط المجموعات (رابط لكل سطر)")
    msg = st.text_area("نص الرسالة")
    
    if st.button("🚀 بدء النشر"):
        async def run_bot():
            # استخدام جلسة باسم فريد لتجنب التضارب
            async with Client("my_session_name", api_id=int(api_id), api_hash=api_hash) as app:
                for group in groups_raw.splitlines():
                    if group.strip():
                        try:
                            await app.join_chat(group.strip())
                            await app.send_message(group.strip(), msg)
                            st.success(f"✅ تم النشر في: {group}")
                        except Exception as e:
                            st.error(f"⚠️ خطأ في {group}: {e}")

        # تشغيل المهمة
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_bot())
