import streamlit as st
import requests
import threading
import random
import datetime
import time
import sys
from queue import Queue

# --- إعدادات Streamlit ---
st.set_page_config(
    page_title="تم تطوير من قبل ايمو ",
    page_icon="",
    layout="centered"
)

# --- CSS مخصص للتصميم ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.main-container {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 30px;
    margin: 20px 0;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.title {
    text-align: center;
    font-size: 2.5rem;
    background: linear-gradient(90deg, #ff7e5f, #feb47b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    color: #d1c4e9;
    margin-bottom: 30px;
    font-size: 1.1rem;
}

.input-box {
    background: rgba(255, 255, 255, 0.1);
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 12px;
    padding: 20px;
    margin: 15px 0;
}

.stButton>button {
    background: linear-gradient(45deg, #ff7e5f, #feb47b);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 30px;
    font-size: 1.1rem;
    font-weight: bold;
    transition: all 0.3s ease;
    width: 100%;
    margin-top: 20px;
}

.stButton>button:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 20px rgba(255, 126, 95, 0.3);
}

.results-box {
    background: rgba(0, 0, 0, 0.3);
    border-radius: 12px;
    padding: 20px;
    margin: 20px 0;
    max-height: 400px;
    overflow-y: auto;
}

.status-good {
    color: #4CAF50;
    font-weight: bold;
    padding: 5px 10px;
    background: rgba(76, 175, 80, 0.1);
    border-radius: 6px;
    margin: 5px 0;
}

.status-bad {
    color: #f44336;
    padding: 5px 10px;
    background: rgba(244, 67, 54, 0.1);
    border-radius: 6px;
    margin: 5px 0;
}

.status-error {
    color: #ff9800;
    padding: 5px 10px;
    background: rgba(255, 152, 0, 0.1);
    border-radius: 6px;
    margin: 5px 0;
}

.footer {
    text-align: center;
    margin-top: 30px;
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.9rem;
    padding-top: 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.2);
}
</style>
""", unsafe_allow_html=True)

# --- المتغيرات العامة ---
insta = "1234567890qwertyuiopasdfghjklzxcvbnm"
all_chars = "_"
results_queue = Queue()
stop_threads = False

# --- دالة التحقق من اسم المستخدم ---
def check_instagram_username(user, token, chat_id):
    global stop_threads
    
    if stop_threads:
        return
        
    url = 'https://www.instagram.com/accounts/web_create_ajax/attempt/'
    
    headers = {
        'Host': 'www.instagram.com',
        'content-length': '85',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101"',
        'x-ig-app-id': '936619743392459',
        'x-ig-www-claim': '0',
        'sec-ch-ua-mobile': '?0',
        'x-instagram-ajax': '81f3a3c9dfe2',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'x-asbd-id': '198387',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Safari/537.36',
        'x-csrftoken': 'jzhjt4G11O37lW1aDFyFmy1K0yIEN9Qv',
        'sec-ch-ua-platform': '"Linux"',
        'origin': 'https://www.instagram.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.instagram.com/accounts/emailsignup/',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-IQ,en;q=0.9'
    }
    
    cookies = {
        'csrftoken': 'jzhjt4G11O37lW1aDFyFmy1K0yIEN9Qv',
        'mid': 'YtsQ1gABAAEszHB5wT9VqccwQIUL',
        'ig_did': '227CCCC2-3675-4A04-8DA5-BA3195B46425',
        'ig_nrcb': '1'
    }
    
    data = f'email=aakmnnsjskksmsnsn%40gmail.com&username={user}&first_name=&opt_into_one_tap=false'
    
    try:
        response = requests.post(url, headers=headers, cookies=cookies, data=data, timeout=10)
        
        if stop_threads:
            return
            
        if '{"message":"feedback_required","spam":true,"feedback_title":"Try Again Later"' in response.text:
            results_queue.put(('error', user))
            
        elif '"errors": {"username":' in response.text or '"code": "username_is_taken"' in response.text:
            results_queue.put(('bad', user))
            
        else:
            results_queue.put(('good', user))
            # إرسال إلى تيليجرام
            message = f"""
* المطور ايمو*
            
 **𝒖𝒔𝒆𝒓:** `{user}`
            
---
 *قناة الخاصه بالادوات المدفوع:* https://t.me/+s7YdDEz2RLNjMDEy
 *قناتي الاساسية:* https://t.me/emoi2
---
            """
            telegram_url = f'https://api.telegram.org/bot{token}/sendMessage'
            payload = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'Markdown'
            }
            try:
                requests.post(telegram_url, data=payload, timeout=5)
            except:
                pass
                
    except Exception as e:
        if not stop_threads:
            results_queue.put(('error', f"{user} - Connection Error"))

# --- دالة توليد الأسماء ---
def generate_usernames(token, chat_id, num_threads=7):
    global stop_threads
    stop_threads = False
    
    def worker():
        while not stop_threads:
            v1 = str(''.join((random.choice(insta) for i in range(1))))
            v2 = str(''.join((random.choice(insta) for i in range(1))))
            v3 = str(''.join((random.choice(insta) for i in range(1))))
            v4 = str(''.join((random.choice(insta) for i in range(1))))
            v5 = str(''.join((random.choice(all_chars) for i in range(1))))
            
            user1 = (v5+v1+v2+v3+v4)
            user2 = (v1+v5+v2+v3+v4)
            user3 = (v1+v2+v5+v3+v4)
            user4 = (v1+v2+v3+v5+v4)
            
            possible_users = [user1, user2, user3, user4]
            user = random.choice(possible_users)
            
            check_instagram_username(user, token, chat_id)
            time.sleep(random.uniform(0.5, 1.5))  # تأخير عشوائي
    
    # إنشاء الخيوط
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker)
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    return threads

# --- واجهة Streamlit الرئيسية ---
def main():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="title">تطوير ايمو</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">✧✧✧✧✧✧✧✧✧✧✧✧✧✧✧</p>', unsafe_allow_html=True)
    
    # قسم الإدخال
    with st.container():
        st.markdown('<div class="input-box">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            chat_id = st.text_input("𝙸𝙳", placeholder="عزيزي ضع الـ 𝙸𝙳 هنا")
        
        with col2:
            token = st.text_input("𝙱𝚘𝚝 𝚃𝚘𝚔𝚎𝚗", placeholder="عزيزي ضع 𝚃𝚘𝚔𝚎𝚗 هنا", type="password")
        
        num_threads = st.slider("𝙽𝚞𝚖𝚋𝚎𝚛 𝚘𝚏 𝚃𝚑𝚛𝚎𝚊𝚍𝚜", min_value=1, max_value=20, value=7, help="More threads = faster checking")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # قسم التحكم
    col_start, col_stop, col_stats = st.columns(3)
    
    with col_start:
        start_button = st.button("𝚂𝚝𝚊𝚛𝚝 𝙲𝚑𝚎𝚌𝚔𝚒𝚗𝚐", use_container_width=True)
    
    with col_stop:
        stop_button = st.button("𝚂𝚝𝚘𝚙", use_container_width=True)
    
    # قسم الإحصائيات والنتائج
    if 'stats' not in st.session_state:
        st.session_state.stats = {'total': 0, 'good': 0, 'bad': 0, 'error': 0}
    
    if 'running' not in st.session_state:
        st.session_state.running = False
    
    # معالجة زر البدء
    if start_button and chat_id and token:
        if not st.session_state.running:
            st.session_state.running = True
            st.session_state.stats = {'total': 0, 'good': 0, 'bad': 0, 'error': 0}
            st.session_state.results = []
            
            # بدء الخيوط في خلفية منفصلة
            st.session_state.threads = generate_usernames(token, chat_id, num_threads)
            
            st.success("✅ Checking started! Results will appear below.")
    
    # معالجة زر الإيقاف
    if stop_button:
        if st.session_state.running:
            global stop_threads
            stop_threads = True
            st.session_state.running = False
            st.warning("⏹️ Checking stopped!")
    
    # عرض الإحصائيات
    with col_stats:
        st.metric("📊 Total Checked", st.session_state.stats['total'])
        st.metric("✅ Available", st.session_state.stats['good'])
    
    # قسم النتائج
    if st.session_state.running or 'results' in st.session_state:
        st.markdown("### 📋 Results")
        results_container = st.empty()
        
        # تحديث النتائج في الوقت الحقيقي
        while st.session_state.running:
            new_results = []
            while not results_queue.empty():
                status, username = results_queue.get()
                st.session_state.stats['total'] += 1
                
                if status == 'good':
                    st.session_state.stats['good'] += 1
                    new_results.append(f'<div class="status-good">✅ Available: {username}</div>')
                elif status == 'bad':
                    st.session_state.stats['bad'] += 1
                    new_results.append(f'<div class="status-bad">❌ Taken: {username}</div>')
                else:
                    st.session_state.stats['error'] += 1
                    new_results.append(f'<div class="status-error">⚠️ Error: {username}</div>')
            
            if new_results:
                if 'results' not in st.session_state:
                    st.session_state.results = []
                st.session_state.results = new_results + st.session_state.results
            
            # تحديث العرض
            if 'results' in st.session_state and st.session_state.results:
                results_html = '<div class="results-box">' + ''.join(st.session_state.results[:50]) + '</div>'
                results_container.markdown(results_html, unsafe_allow_html=True)
            
            time.sleep(0.5)
        
        # عرض النتائج النهائية بعد التوقف
        if 'results' in st.session_state and st.session_state.results:
            results_html = '<div class="results-box">' + ''.join(st.session_state.results[:50]) + '</div>'
            results_container.markdown(results_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # التذييل
    st.markdown("""
    <div class="footer">
    <p>✧<strong>EMO</strong> | قناة المطور ايمو: <a href="https://t.me/emoi2" style="color:#ff7e5f;">@legox3</a></p>
    <p style="font-size:0.8rem; opacity:0.7;">This tool is for educational purposes only</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
