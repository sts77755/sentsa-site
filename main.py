# main.py

import requests
from bs4 import BeautifulSoup
import time
import random

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0 Safari/537.36"
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def fetch_page(url):
    headers = {'User-Agent': get_random_user_agent()}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"请求 {url} 失败: {e}")
        return None

def search_baidu(keyword, num_results=5):
    print(f"正在从百度搜索关键词: {keyword}")
    search_url = f"https://www.baidu.com/s?wd={keyword}"
    html_content = fetch_page(search_url)
    results = []
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        # Baidu search results often have a class like 'c-container'
        for item in soup.find_all('div', class_='c-container', limit=num_results):
            title_tag = item.find('h3')
            link_tag = item.find('a')
            if title_tag and link_tag:
                title = title_tag.get_text(strip=True)
                url = link_tag['href']
                # Baidu's links are often redirected, try to get the real URL
                try:
                    real_url_response = requests.head(url, allow_redirects=True, timeout=5)
                    real_url = real_url_response.url
                except requests.exceptions.RequestException:
                    real_url = url # Fallback to original URL if redirection fails
                results.append({'title': title, 'url': real_url})
    time.sleep(random.uniform(2, 5)) # 随机延迟2到5秒
    return results

def search_google(keyword, num_results=5):
    print(f"正在从谷歌搜索关键词: {keyword}")
    # Note: Google might block direct scraping easily. Using a custom search engine or API is more robust.
    # This basic example might not always work reliably without proxies or more advanced techniques.
    search_url = f"https://www.google.com/search?q={keyword}"
    html_content = fetch_page(search_url)
    results = []
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        # Google search results often have a class like 'tF2CMy' or 'g'
        for item in soup.find_all('div', class_='g', limit=num_results):
            title_tag = item.find('h3')
            link_tag = item.find('a')
            if title_tag and link_tag:
                title = title_tag.get_text(strip=True)
                url = link_tag['href']
                results.append({'title': title, 'url': url})
    time.sleep(random.uniform(3, 7)) # 随机延迟3到7秒
    return results

def main():
    keywords = ["华纳万宝路官网", "万宝路公司客服", "华纳万宝路开户注册步骤", "华纳万宝路app下载"]
    
    for keyword in keywords:
        keyword = keyword.strip()
        if not keyword:
            continue

        print(f"\n--- 搜索结果 for '{keyword}' ---")
        
        baidu_results = search_baidu(keyword)
        print("\n百度搜索结果:")
        if baidu_results:
            for i, result in enumerate(baidu_results):
                print(f"{i+1}. 标题: {result['title']}\n   URL: {result['url']}")
        else:
            print("未找到百度搜索结果或请求失败。")

        google_results = search_google(keyword)
        print("\n谷歌搜索结果:")
        if google_results:
            for i, result in enumerate(google_results):
                print(f"{i+1}. 标题: {result['title']}\n   URL: {result['url']}")
        else:
            print("未找到谷歌搜索结果或请求失败。这可能是由于谷歌的反爬机制。")

if __name__ == "__main__":
    main()
