import streamlit as st
import requests
import threading
import random
import time
from queue import Queue

# --- إعدادات Streamlit خفيفة ---
st.set_page_config(
    page_title="Instagram Username Checker",
    page_icon="🔍",
    layout="centered"
)

# --- CSS خفيف جداً ---
st.markdown("""
<style>
.stApp {
    background-color: #f8f9fa;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}

.header {
    text-align: center;
    padding: 20px 0;
    border-bottom: 2px solid #e9ecef;
    margin-bottom: 30px;
}

.header h1 {
    color: #2d3436;
    font-size: 28px;
    font-weight: 600;
    margin-bottom: 8px;
}

.header p {
    color: #636e72;
    font-size: 14px;
}

.input-section {
    background: white;
    border-radius: 12px;
    padding: 25px;
    margin-bottom: 25px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    border: 1px solid #e9ecef;
}

.input-label {
    color: #2d3436;
    font-weight: 500;
    margin-bottom: 8px;
    display: block;
    font-size: 14px;
}

.stTextInput>div>div>input {
    border: 1.5px solid #dfe6e9;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 14px;
}

.stTextInput>div>div>input:focus {
    border-color: #6c5ce7;
    box-shadow: 0 0 0 2px rgba(108, 92, 231, 0.1);
}

.stButton>button {
    background: #6c5ce7;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.2s;
    width: 100%;
}

.stButton>button:hover {
    background: #5b4bcf;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(108, 92, 231, 0.2);
}

.stButton>button:disabled {
    background: #a29bfe;
    cursor: not-allowed;
}

.results-container {
    background: white;
    border-radius: 12px;
    padding: 20px;
    margin-top: 20px;
    border: 1px solid #e9ecef;
    max-height: 400px;
    overflow-y: auto;
}

.result-item {
    padding: 10px 12px;
    margin: 6px 0;
    border-radius: 6px;
    font-size: 13px;
    display: flex;
    align-items: center;
}

.result-good {
    background: #d4edda;
    color: #155724;
    border-left: 4px solid #28a745;
}

.result-bad {
    background: #f8d7da;
    color: #721c24;
    border-left: 4px solid #dc3545;
}

.result-error {
    background: #fff3cd;
    color: #856404;
    border-left: 4px solid #ffc107;
}

.stats-card {
    background: white;
    border-radius: 10px;
    padding: 15px;
    text-align: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    border: 1px solid #e9ecef;
}

.stat-value {
    font-size: 24px;
    font-weight: 600;
    color: #2d3436;
}

.stat-label {
    font-size: 12px;
    color: #636e72;
    margin-top: 4px;
}

.footer {
    text-align: center;
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid #e9ecef;
    color: #636e72;
    font-size: 12px;
}

.loading-spinner {
    display: inline-block;
    width: 20px;
    height: 20px;
    margin-right: 10px;
    border: 2px solid #f3f3f3;
    border-top: 2px solid #6c5ce7;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
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
🔍 *Instagram Username Found!*
            
🎯 **Username:** `{user}`
            
---
📱 *Developer:* @zeon_f9 • @bo_d7 • @K66Z6
📢 *Channel:* https://t.me/legox3
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
            time.sleep(random.uniform(0.5, 1.5))
    
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker)
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    return threads

# --- واجهة Streamlit الرئيسية ---
def main():
    # الهيدر
    st.markdown("""
    <div class="header">
        <h1>🔍 Instagram Username Checker</h1>
        <p>Automatically check available Instagram usernames</p>
    </div>
    """, unsafe_allow_html=True)
    
    # قسم الإدخال
    with st.container():
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<span class="input-label">💬 Telegram Chat ID</span>', unsafe_allow_html=True)
            chat_id = st.text_input("", placeholder="Enter your Chat ID", label_visibility="collapsed")
        
        with col2:
            st.markdown('<span class="input-label">🔑 Bot Token</span>', unsafe_allow_html=True)
            token = st.text_input("", placeholder="Enter your Bot Token", type="password", label_visibility="collapsed")
        
        st.markdown('<span class="input-label" style="margin-top: 20px;">⚡ Number of Threads</span>', unsafe_allow_html=True)
        num_threads = st.slider("", min_value=1, max_value=10, value=3, help="Recommended: 3-5 threads", label_visibility="collapsed")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # الأزرار والإحصائيات
    col1, col2, col3 = st.columns([2, 2, 3])
    
    with col1:
        start_button = st.button("🚀 Start Checking", disabled=st.session_state.get('running', False))
    
    with col2:
        stop_button = st.button("⏹️ Stop", disabled=not st.session_state.get('running', False))
    
    with col3:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        if 'stats' in st.session_state:
            st.markdown(f'<div class="stat-value">{st.session_state.stats["total"]}</div>', unsafe_allow_html=True)
            st.markdown('<div class="stat-label">Total Checked</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="stat-value">0</div>', unsafe_allow_html=True)
            st.markdown('<div class="stat-label">Total Checked</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # تهيئة حالة الجلسة
    if 'stats' not in st.session_state:
        st.session_state.stats = {'total': 0, 'good': 0, 'bad': 0, 'error': 0}
    
    if 'running' not in st.session_state:
        st.session_state.running = False
    
    if 'results' not in st.session_state:
        st.session_state.results = []
    
    # معالجة الأحداث
    if start_button and chat_id and token and not st.session_state.running:
        st.session_state.running = True
        st.session_state.stats = {'total': 0, 'good': 0, 'bad': 0, 'error': 0}
        st.session_state.results = []
        
        # بدء الخيوط
        global stop_threads
        stop_threads = False
        st.session_state.threads = generate_usernames(token, chat_id, num_threads)
        
        st.success("✅ Checking started!")
    
    if stop_button and st.session_state.running:
        global stop_threads
        stop_threads = True
        st.session_state.running = False
        st.warning("⏹️ Checking stopped!")
    
    # عرض النتائج
    if st.session_state.running or st.session_state.results:
        st.markdown("### 📊 Live Results")
        
        # تحديث النتائج
        if st.session_state.running:
            new_results = []
            while not results_queue.empty():
                status, username = results_queue.get()
                st.session_state.stats['total'] += 1
                
                if status == 'good':
                    st.session_state.stats['good'] += 1
                    new_results.append(f'<div class="result-item result-good">✅ Available: {username}</div>')
                elif status == 'bad':
                    st.session_state.stats['bad'] += 1
                    new_results.append(f'<div class="result-item result-bad">❌ Taken: {username}</div>')
                else:
                    st.session_state.stats['error'] += 1
                    new_results.append(f'<div class="result-item result-error">⚠️ Error: {username}</div>')
            
            if new_results:
                st.session_state.results = new_results + st.session_state.results
        
        # عرض النتائج
        results_container = st.empty()
        if st.session_state.results:
            results_html = '<div class="results-container">' + ''.join(st.session_state.results[:30]) + '</div>'
            results_container.markdown(results_html, unsafe_allow_html=True)
        
        # تحديث تلقائي عند التشغيل
        if st.session_state.running:
            time.sleep(0.5)
            st.rerun()
    
    # التذييل
    st.markdown("""
    <div class="footer">
        <p>🔧 Developed by <strong>EMO</strong> | 📱 Telegram: <a href="https://t.me/legox3" target="_blank" style="color:#6c5ce7; text-decoration:none;">@legox3</a></p>
        <p style="margin-top: 5px; opacity: 0.8;">For educational purposes only • Lightweight design for better performance</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
