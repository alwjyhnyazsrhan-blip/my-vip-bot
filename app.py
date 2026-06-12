import streamlit as st
import hashlib
import re
import asyncio
from pyrogram import Client

# --- 1. الإعدادات ---
st.set_page_config(page_title="VIP ACCESS", page_icon="👑")
st.markdown("""
    <style>
    .stApp {background-color: #0e1117;}
    .stButton>button {width: 100%; background-color: #00ff88; color: black; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

# --- 2. الدوال ---
def check_key(hwid, key):
    return key == hashlib.sha256((hwid + "MY_SECRET_KEY").encode()).hexdigest()[:12].upper()

def clean_groups(raw_input):
    urls = re.findall(r'(https?://t\.me/[+a-zA-Z0-9_]+|t\.me/[+a-zA-Z0-9_]+)', raw_input)
    return list(set(urls))

# --- 3. الواجهة (نظام القفل) ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
hwid = hashlib.md5(st.context.headers.get("User-Agent", "").encode()).hexdigest()[:10].upper()

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
    # --- 4. لوحة التحكم (محرك النشر الذكي) ---
    st.title("🚀 لوحة تحكم النشر")
    api_id = st.text_input("API ID")
    api_hash = st.text_input("API HASH", type="password")
    groups_raw = st.text_area("روابط المجموعات:")
    message = st.text_area("نص الرسالة:")
    
    if st.button("بدء النشر الذكي"):
        groups = clean_groups(groups_raw)
        st.write(f"⚙️ جاري النشر في {len(groups)} مجموعة...")
        
        async def start_publishing():
            async with Client("my_session", api_id=int(api_id), api_hash=api_hash) as app:
                for group in groups:
                    try:
                        await app.join_chat(group)
                        await app.send_message(group, message)
                        st.success(f"✅ تم بنجاح: {group}")
                    except Exception as e:
                        st.warning(f"⚠️ تخطي {group}: خطأ تقني")
                        continue
        
        # --- حل مشكلة Event Loop ---
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(start_publishing())
        except Exception as e:
            st.error(f"خطأ في تشغيل المحرك: {e}")
