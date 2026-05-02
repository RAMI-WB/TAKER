import search_engine
import extractor

def taker_action(user_request, category):
    print(f"\n🚀 TAKER في مهمة لإحضار: {user_request}")
    
    # 1. بناء استعلام ذكي بناءً على النوع
    query = user_request
    if category == "book":
        query = f'"{user_request}" filetype:pdf OR filetype:epub'
    elif category == "tool":
        query = f'"{user_request}" (filetype:exe OR filetype:zip OR site:github.com)'
    
    # 2. البحث عن الروابط
    links = search_engine.get_links(query, max_results=5)
    
    if not links:
        print("❌ لم يجد TAKER أي مسار لهذا الطلب.")
        return

    print(f"✅ وجد TAKER {len(links)} مسارات محتملة. جاري فحص الروابط المباشرة...")

    # 3. محاولة استخراج روابط التحميل أو المحتوى
    for item in links:
        url = item['url']
        print(f"\n🔗 فحص الرابط: {url}")
        
        # إذا كان الطلب كتاباً، نبحث عن روابط PDF مباشرة داخل الصفحة
        if category == "book":
            direct_files = extractor.take_specific_links(url, ".pdf")
            if direct_files:
                print(f"🎯 وجد TAKER روابط تحميل مباشرة:")
                for file_url in direct_files:
                    print(f"   📥 {file_url}")
            else:
                print("   📄 لم يجد روابط مباشرة، قد تجد الملف يدوياً في الرابط أعلاه.")
        
        # إذا كان الطلب عاماً، نأخذ ملخص المحتوى
        else:
            content = extractor.take_content(url)
            print(f"📝 ملخص ما وجده TAKER:\n{content[:300]}...")

if name == "main":
    print("--- نظام TAKER للمهمات الصعبة ---")
    goal = input("ماذا تريد أن أحضر لك؟ ")
    cat = input("نوع الهدف (book / tool / general): ").lower()
    
    taker_action(goal, cat)
