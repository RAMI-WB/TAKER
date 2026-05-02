import search_engine
import extractor
import os
import sqlite3
import requests
from datetime import datetime

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

# --- وظيفة التحميل التلقائي ---

def download_file(url, folder_name):
    """تحميل الملف وحفظه في مجلد المهمة"""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    # استخراج اسم الملف من الرابط
    file_name = url.split('/')[-1].split('?')[0]
    if not file_name:
        file_name = f"downloaded_file_{datetime.now().strftime('%H%M%S')}"
    
    file_path = os.path.join(folder_name, file_name)
    
    try:
        print(f"    📥 جاري تحميل: {file_name}...")
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, stream=True, timeout=30)
        
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"    ✅ تم التحميل بنجاح: {file_path}")
            return file_path
        else:
            print(f"    ❌ فشل التحميل (Status: {response.status_code})")
            return "Failed"
    except Exception as e:
        print(f"    ❌ خطأ أثناء التحميل: {e}")
        return "Error"

# --- واجهة المستخدم والمنطق الأساسي ---

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    init_db()
    clear_screen()
    print("""
    #########################################
    #           TAKER v1.2 - PRO            #
    #    The Ultimate File & Info Hunter    #
    #########################################
    """)
    
    print("[1] مهمة صيد وتحميل جديدة")
    print("[2] استعراض الخزنة (The Vault)")
    action = input("\n[?] اختر العمليّة: ")

    if action == "2":
        show_vault()
        return

    goal = input("\n[?] ماذا تريد أن أحضر لك؟ ")
    print("\n[1] كتاب (PDF/EPUB)\n[2] أداة/برنامج (EXE/ZIP)\n[3] بحث عام ومعلومات")
    choice = input("\n[?] اختر النوع: ")
    
    mode_map = {"1": "book", "2": "tool", "3": "web"}
    category = mode_map.get(choice, "web")
    
    # إنشاء مجلد خاص للمهمة
    folder_name = f"downloads/{goal.replace(' ', '_')}"
    
    # 1. مرحلة البحث
    results = search_engine.get_links(goal, category)
    
    if not results:
        print("\n[-] TAKER لم يجد أي نتائج.")
        return

    print(f"\n[+] وجد TAKER {len(results)} مصادر. يبدأ الاستحواذ الآن...")

    # 2. مرحلة الاستخراج والتحميل
    for i, item in enumerate(results, 1):
        url = item['url']
        title = item['title']
        print(f"\n[{i}] فحص: {title}")
        
        # حفظ الرابط في القاعدة
        save_loot(goal, category, title, url)
        
        if category in ["book", "tool"]:
            direct_links = extractor.take_direct_links(url, category)
            if direct_links:
                for d_url in direct_links:
                    saved_path = download_file(d_url, folder_name)
                    if saved_path not in ["Failed", "Error"]:
                        save_loot(goal, f"{category}_file", title, d_url, saved_path)
                        else:
                print("    [-] لا توجد روابط مباشرة قابلة للتحميل في هذا المصدر.")
        else:
            content = extractor.take_content(url)
            print(f"    📝 محتوى: {content[:200]}...")

    print(f"\n[!] انتهت المهمة. الملفات موجودة في المجلد: {folder_name}")

def show_vault():
    clear_screen()
    print("--- TAKER VAULT (تاريخ الصيد) ---")
    conn = sqlite3.connect('taker_vault.db')
    cursor = conn.cursor()
    cursor.execute('SELECT goal, title, file_path FROM loot WHERE file_path != "None" ORDER BY timestamp DESC')
    rows = cursor.fetchall()
    
    if not rows:
        print("لا توجد ملفات محملة في الخزنة بعد.")
    for row in rows:
        print(f"\n[الهدف]: {row[0]}")
        print(f"[الملف]: {row[1]}")
        print(f"[المسار]: {row[2]}")
        print("-" * 30)
    conn.close()
    input("\nاضغط Enter للعودة...")
    main()

if name == "main":
    main()
