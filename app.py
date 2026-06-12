import streamlit as st
import hashlib
import re
import asyncio
from pyrogram import Client

# --- الإعدادات ---
st.set_page_config(page_title="VIP ACCESS", page_icon="👑")

# --- الدوال الأساسية ---
def check_key(hwid, key):
    return key == hashlib.sha256((hwid + "MY_SECRET_KEY").encode()).hexdigest()[:12].upper()

def clean_groups(raw_input):
    urls = re.findall(r'(https?://t\.me/[+a-zA-Z0-9_]+|t\.me/[+a-zA-Z0-9_]+)', raw_input)
    return list(set(urls))

# --- واجهة القفل ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
hwid = hashlib.md5(st.context.headers.get("User-Agent", "").encode()).hexdigest()[:10].upper()

if not st.session_state.authenticated:
    st.title("👑 VIP ACCESS")
    st.code(hwid)
    key_input = st.text_input("🔑 مفتاح التفعيل:")
    if st.button("دخول"):
        if check_key(hwid, key_input):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("مفتاح خاطئ")
else:
    # --- لوحة التحكم ---
    st.title("🚀 لوحة تحكم النشر")
    api_id = st.text_input("API ID")
    api_hash = st.text_input("API HASH", type="password")
    groups_raw = st.text_area("الروابط:")
    message = st.text_area("الرسالة:")
    
    if st.button("بدء النشر الذكي"):
        groups = clean_groups(groups_raw)
        
        # الحل الجذري: نستخدم دالة بسيطة للتشغيل
        async def main_task():
            async with Client("my_session", api_id=int(api_id), api_hash=api_hash) as app:
                for group in groups:
                    try:
                        await app.join_chat(group)
                        await app.send_message(group, message)
                        st.success(f"✅ تم: {group}")
                    except Exception:
                        st.warning(f"⚠️ تعذر: {group}")
                        continue

        # هذا الجزء هو الأهم لتجاوز الخطأ
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(main_task())
        except Exception as e:
            st.write(f"حدث خطأ: {e}")
