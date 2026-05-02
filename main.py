import search_engine
import extractor
import os
import sqlite3
from datetime import datetime

# --- وظائف قاعدة البيانات ---

def init_db():
    """إنشاء قاعدة البيانات والجداول إذا لم تكن موجودة"""
    conn = sqlite3.connect('taker_vault.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS loot (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal TEXT,
            category TEXT,
            title TEXT,
            url TEXT,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    return conn

def save_loot(goal, category, title, url):
    """حفظ النتائج التي عثر عليها TAKER"""
    conn = sqlite3.connect('taker_vault.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO loot (goal, category, title, url, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (goal, category, title, url, datetime.now()))
    conn.commit()
    conn.close()

# --- واجهة المستخدم والمنطق ---

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # تهيئة قاعدة البيانات
    init_db()
    
    clear_screen()
    print("""
    #########################################
    #           TAKER v1.1 - Vault Ed.      #
    #    The Ultimate File & Info Hunter    #
    #########################################
    """)
    
    print("[1] مهمة بحث جديدة")
    print("[2] استعراض الصيد القديم (The Vault)")
    action = input("\n[?] اختر ماذا تريد: ")

    if action == "2":
        show_vault()
        return

    goal = input("\n[?] ماذا تريد من TAKER أن يحضر لك؟ ")
    print("\n[1] كتاب (PDF/EPUB)\n[2] أداة أو برنامج (EXE/ZIP)\n[3] بحث عام ومعلومات\n[4] تسريبات ومستودعات برمجية")
    choice = input("\n[?] اختر رقم المهمة: ")
    
    mode_map = {"1": "book", "2": "tool", "3": "web", "4": "leak"}
    category = mode_map.get(choice, "web")
    
    # 1. مرحلة البحث
    results = search_engine.get_links(goal, category)
    
    if not results:
        print("\n[-] TAKER لم يجد أي نتائج لهذه المهمة.")
        return

    print(f"\n[+] تم العثور على {len(results)} مصادر. جاري الفحص والحفظ في الخزنة...")

    # 2. مرحلة الاستخراج والحفظ
    for i, item in enumerate(results, 1):
        url = item['url']
        title = item['title']
        print(f"\n[{i}] فحص: {title}")
        
        # حفظ الرابط الأساسي في قاعدة البيانات
        save_loot(goal, category, title, url)
        
        if category in ["book", "tool"]:
            files = extractor.take_direct_links(url, category)
            if files:
                print("    🎯 روابط تحميل مباشرة وجدها TAKER:")
                for f in files:
                    print(f"       📥 {f}")
                    # حفظ كل رابط تحميل مباشر كصيد منفصل
                    save_loot(goal, f"{category}_direct", title, f)
            else:
                print("    [-] لم يتم العثور على روابط تحميل مباشرة.")
        else:
            print(f"    [+] تم حفظ الرابط في الخزنة: {url}")

    print("\n[!] انتهت المهمة. تم تحديث الخزنة (taker_vault.db).")

def show_vault():
    """عرض البيانات المخزنة سابقاً"""
    clear_screen()
    print("--- TAKER VAULT (تاريخ الصيد) ---")
    conn = sqlite3.connect('taker_vault.db')
    cursor = conn.cursor()
    cursor.execute('SELECT goal, title, url FROM loot ORDER BY timestamp DESC LIMIT 20')
    rows = cursor.fetchall()
    
    if not rows:
        print("الخزنة فارغة حالياً.")
    for row in rows:
        print(f"\n[الهدف]: {row[0]}")
        print(f"[العنوان]: {row[1]}")
        print(f"[الرابط]: {row[2]}")
        print("-" * 30)
    conn.close()
    input("\nاضغط Enter للعودة...")
    main()

if name == "main":
    main()
