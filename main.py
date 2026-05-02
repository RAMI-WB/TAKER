import requests
from bs4 import BeautifulSoup
import trafilatura
import random

# قائمة User-Agents لجعل TAKER يبدو كمتصفحات مختلفة لتجنب الحظر
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/115.0"
]

def take_content(url):
    """استخراج النص الصافي من الصفحة بذكاء."""
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            content = trafilatura.extract(response.text)
            return content if content else "No readable text found."
        return f"Access Denied (Status: {response.status_code})"
    except Exception as e:
        return f"Extraction Error: {str(e)}"

def take_direct_links(url, category):
    """صيد الروابط المباشرة بناءً على نوع الهدف (كتاب أو أداة)."""
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    extensions = {
        "book": [".pdf", ".epub", ".mobi"],
        "tool": [".exe", ".zip", ".rar", ".msi", ".tar.gz"]
    }.get(category, [])

    found_files = []
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            # التحقق من أن الرابط ينتهي بإحدى الصيغ المطلوبة
            if any(href.lower().endswith(ext) for ext in extensions):
                # تصحيح الروابط النسبية لتصبح كاملة
                if href.startswith('/'):
                    from urllib.parse import urljoin
                    href = urljoin(url, href)
                found_files.append(href)
        
        return list(set(found_files)) # إزالة التكرار
    except:
        return []
