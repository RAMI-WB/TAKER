import search_engine
import extractor
import os
import sqlite3
import requests
from datetime import datetime

# --- إعدادات تلجرام ---
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN_HERE"
CHAT_ID = "YOUR_CHAT_ID_HERE"

# --- وظائف قاعدة البيانات ---

def init_db():
    conn = sqlite3.connect('taker_vault.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS loot (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal TEXT,
            category TEXT,
            title TEXT,
            url TEXT,
            file_path TEXT,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()

def save_loot(goal, category, title, url, file_path="None"):
    conn = sqlite3.connect('taker_vault.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO loot (goal, category, title, url, file_path, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (goal, category, title, url, file_path, datetime.now()))
    conn.commit()
    conn.close()

# --- وظيفة الإرسال إلى تلجرام ---

def send_to_telegram(file_path, caption):
    """إرسال الملف إلى تلجرام ثم حذفه لتوفير مساحة الهاتف"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
    try:
        with open(file_path, 'rb') as f:
            files = {'document': f}
            data = {'chat_id': CHAT_ID, 'caption': caption}
            response = requests.post(url, files=files, data=data)
            if response.status_code == 200:
                print(f"    ☁️ تم الرفع إلى سحابة تلجرام بنجاح!")
                # اختيارياً: حذف الملف من الهاتف بعد الرفع لتوفير مساحة
                # os.remove(file_path) 
            else:
                print(f"    ⚠️ فشل الرفع لتلجرام: {response.status_code}")
    except Exception as e:
        print(f"    ⚠️ خطأ في اتصال تلجرام: {e}")

# --- وظيفة التحميل التلقائي ---

def download_file(url, folder_name, goal):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    file_name = url.split('/')[-1].split('?')[0]
    if not file_name:
        file_name = f"file_{datetime.now().strftime('%H%M%S')}"
    
    file_path = os.path.join(folder_name, file_name)
    
    try:
        print(f"    📥 جاري قنص: {file_name}...")
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, stream=True, timeout=60)
        
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"    ✅ تم التحميل محلياً.")
            # إرسال للسحابة فوراً
            send_to_telegram(file_path, f"🎯 TAKER صيد جديد!\nالهدف: {goal}\nالملف: {file_name}")
            return file_path
        return "Failed"
    except Exception as e:
        return "Error"

# --- المنطق الأساسي ---

def main():
    init_db()
    os.system('clear')
    print("""
    #########################################
    #        TAKER v1.3 - CLOUD EDITION     #
    #     Hunter: Termux + Telegram Cloud   #
    #########################################
    """)
    
    goal = input("\n[?] ماذا تريد من TAKER أن يصطاد الآن؟ ")
    print("\n[1] كتاب (PDF/EPUB)\n[2] أداة (EXE/ZIP/RAR)\n[3] معلومة محددة")
    choice = input("\n[?] اختر المهمة: ")
    
    mode_map = {"1": "book", "2": "tool", "3": "web"}
    category = mode_map.get(choice, "web")
    
    folder_name = "downloads"
    
    results = search_engine.get_links(goal, category)
    if not results:
        print("\n[-] لم يتم العثور على أهداف.")
        return

    print(f"\n[+] بدأ الاستحواذ على {len(results)} مصادر...")

    for i, item in enumerate(results, 1):
        url = item['url']
        title = item['title']
        print(f"\n[{i}] فحص المصدر: {title}") 
        
 save_loot(goal, category, title, url)
        
        if category in ["book", "tool"]:
            # نمرر goal_name لتحسين الدقة (التي شرحناها سابقاً)
            direct_links = extractor.take_direct_links(url, category, goal)
            if direct_links:
                for d_url in direct_links:
                    saved_path = download_file(d_url, folder_name, goal)
                    if saved_path not in ["Failed", "Error"]:
                        save_loot(goal, f"{category}_file", title, d_url, saved_path)
            else:
                print("    [-] لم أجد رابط تحميل مباشر هنا.")

    print(f"\n[!] انتهت المهمة. تفقد حسابك في تلجرام!")

if name == "main":
    main()
