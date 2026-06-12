import streamlit as st
import hashlib
import asyncio
import os
import nest_asyncio

# تفعيل nest_asyncio للسماح للـ loops بالعمل داخل Streamlit
nest_asyncio.apply()

# إعداد المتغيرات لتجنب تعارض Pyrogram
os.environ["PYROGRAM_SKIP_TELETHON_SYNC"] = "1"
from pyrogram import Client

# إعداد الصفحة
st.set_page_config(page_title="VIP ACCESS", page_icon="👑")

# المنطق البرمجي
if 'authenticated' not in st.session_state: st.session_state.authenticated = False

# توليد معرف الجهاز (HWID)
hwid = hashlib.md5(st.context.headers.get("User-Agent", "").encode()).hexdigest()[:10].upper()

st.markdown("<h1 style='text-align: center;'>👑 VIP ACCESS</h1>", unsafe_allow_html=True)

if not st.session_state.authenticated:
    st.write(f"**معرف جهازك:** `{hwid}`")
    key_input = st.text_input("🔑 أدخل مفتاح التفعيل")
    
    if st.button("تسجيل الدخول"):
        # المفتاح يتم حسابه بناءً على المعرف
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
        if not api_id or not api_hash or not groups_raw:
            st.warning("يرجى ملء جميع البيانات")
        else:
            async def run_bot():
                # إنشاء الجلسة
                async with Client("my_session", api_id=int(api_id), api_hash=api_hash) as app:
                    for group in groups_raw.splitlines():
                        if group.strip():
                            try:
                                await app.join_chat(group.strip())
                                await app.send_message(group.strip(), msg)
                                st.write(f"✅ تم النشر في: `{group.strip()}`")
                            except Exception as e:
                                st.error(f"⚠️ خطأ في {group.strip()}: {e}")

            # تشغيل العملية
            try:
                loop = asyncio.get_event_loop()
                loop.run_until_complete(run_bot())
            except Exception as e:
                st.error(f"خطأ في تشغيل البوت: {e}")
