import requests
from bs4 import BeautifulSoup
import trafilatura

def take_content(url):
    """
    هذه الدالة هي التي تقوم بـ 'أخذ' المحتوى من الرابط.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    
    try:
        # محاولة جلب الصفحة
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            # استخدام trafilatura لاستخلاص النص الأساسي بدقة (يتجاوز الإعلانات والقوائم)
            downloaded = response.text
            content = trafilatura.extract(downloaded)
            
            if content:
                return content
            else:
                # إذا فشل trafilatura، نستخدم BeautifulSoup كخطة بديلة
                soup = BeautifulSoup(response.text, 'html.parser')
                return soup.get_text(separator='\n', strip=True)[:2000] # نأخذ أول 2000 حرف
        else:
            return f"❌ تعذر الدخول للموقع. رمز الحالة: {response.status_code}"
            
    except Exception as e:
        return f"❌ خطأ أثناء الاستخراج من {url}: {str(e)}"

# الجزء الخاص بالتجربة
if name == "main":
    target = input("أدخل الرابط الذي تريد لـ TAKER أن يفرغه: ")
    print("\n⏳ جاري السحب...\n")
    print(take_content(target))
