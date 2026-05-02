from duckduckgo_search import DDGS

def get_links(query, max_results=10):
    """
    تقوم هذه الدالة بالبحث في الويب وإرجاع قائمة بالروابط المتعلقة بالطلب.
    """
    links = []
    print(f"🔍 TAKER يبحث الآن عن: {query}...")
    
    try:
        with DDGS() as ddgs:
            # البحث عن الروابط
            results = ddgs.text(query, max_results=max_results)
            for res in results:
                links.append({
                    'title': res['title'],
                    'url': res['href']
                })
        return links
    except Exception as e:
        print(f"❌ حدث خطأ أثناء البحث: {e}")
        return []

# تجربة المحرك بشكل منفصل
if name == "main":
    search_query = input("ما الذي تريد لـ TAKER أن يجده؟ ")
    results = get_links(search_query)
    for idx, item in enumerate(results, 1):
        print(f"{idx}. {item['title']} -> {item['url']}")
