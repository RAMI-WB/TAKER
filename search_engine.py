import requests
from duckduckgo_search import DDGS

# مكتبة الـ Dorks الخارقة لـ TAKER
DORKS_LIBRARY = {
    "book": 'intitle:"index of" (pdf|epub|mobi) "{query}"',
    "tool": 'intitle:"index of" (exe|zip|rar|msi) "{query}"',
    "cloud": '(site:mediafire.com | site:mega.nz | site:drive.google.com) "{query}"',
    "leak": 'site:pastebin.com | site:github.com | site:controlc.com "{query}"',
    "web": '{query}'
}

def get_links(query, category="web", max_results=10):
    """
    البحث المتقدم باستخدام Dorks لجلب روابط مباشرة ومخفية.
    """
    # اختيار الـ Dork المناسب أو البحث العادي
    search_query = DORKS_LIBRARY.get(category, "{query}").format(query=query)
    
    links = []
    print(f"\n[!] TAKER Searching for: {search_query}")
    
    try:
        with DDGS() as ddgs:
            results = ddgs.text(search_query, max_results=max_results)
            if not results:
                return []
            
            for res in results:
                links.append({
                    'title': res['title'],
                    'url': res['href']
                })
        return links
    except Exception as e:
        print(f"[-] Search Error: {e}")
        return []

if name == "main":
    # تجربة سريعة للملف
    q = input("Enter target: ")
    res = get_links(q, "book")
    for r in res:
        print(f"[*] Found: {r['url']}")
