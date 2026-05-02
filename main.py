import search_engine
import extractor
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    print("""
    #########################################
    #           TAKER v1.0 - Alpha          #
    #    The Ultimate File & Info Hunter    #
    #########################################
    """)
    
    goal = input("[?] ماذا تريد من TAKER أن يحضر لك؟ ")
    print("\n[1] كتاب (PDF/EPUB)\n[2] أداة أو برنامج (EXE/ZIP)\n[3] بحث عام ومعلومات\n[4] تسريبات ومستودعات برمجية")
    choice = input("\n[?] اختر رقم المهمة: ")
    
    # تحويل الاختيار إلى تصنيف
    mode_map = {"1": "book", "2": "tool", "3": "web", "4": "leak"}
    category = mode_map.get(choice, "web")
    
    # 1. مرحلة البحث
    results = search_engine.get_links(goal, category)
    
    if not results:
        print("\n[-] TAKER لم يجد أي نتائج لهذه المهمة.")
        return

    print(f"\n[+] تم العثور على {len(results)} مصادر. يبدأ الفحص الآن...")

    # 2. مرحلة الاستخراج
    for i, item in enumerate(results, 1):
        url = item['url']
        print(f"\n[{i}] المصدر: {item['title']}")
        print(f"    الرابط: {url}")
        
        # إذا كان الهدف ملفات (كتاب أو أداة)
        if category in ["book", "tool"]:
            files = extractor.take_direct_links(url, category)
            if files:
                print("    🎯 روابط تحميل مباشرة وجدها TAKER:")
                for f in files:
                    print(f"       📥 {f}")
            else:
                print("    [-] لم يتم العثور على روابط تحميل مباشرة في هذا الرابط.")
        
        # إذا كان الهدف معلومات عامة
        else:
            content = extractor.take_content(url)
            print("    📝 ملخص المحتوى:")
            print(f"       {content[:400]}..." if content else "       (لا يوجد نص قابل للقراءة)")

    print("\n[!] انتهت المهمة. TAKER في انتظار أوامر جديدة.")

if name == "main":
    main()
