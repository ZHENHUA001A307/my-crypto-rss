import requests
import re
import json
from datetime import datetime

# --- 【你的私人定制滤网】 ---
GOD_TRADERS = ["Rewkang", "ryzzqq", "Cbb0fe", "Arthur Hayes", "GCR", "Vida"]
MARKET_KEYWORDS = ["BTC", "ETH", "USD", "USDT", "USDC", "黄金", "GOLD", "XAU", "SPX", "S&P", "NDX", "NASDAQ", "纳斯达克"]
MIN_SCORE = 1 
# -------------------------

def get_real_data():
    url = "https://x-gpt.bwequation.com/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        r = requests.get(url, headers=headers, timeout=15)
        html = r.text
        
        # 使用正则表达式寻找网页中隐藏的 JSON 数据块
        # 该网站的数据通常存储在像 { "tweet_username": ... } 这样的结构里
        pattern = r'\{ "tweet_username":.*?"final_score": -?\d+ \}'
        matches = re.findall(pattern, html, re.DOTALL)
        
        results = []
        for m in matches:
            try:
                # 清理并解析 JSON
                data = json.loads(m)
                user = data.get("tweet_username", "")
                content = data.get("current_tweet_content", "")
                score = data.get("final_score", 0)
                
                # --- 三重过滤逻辑 ---
                # 1. 检查是否是大V (God Trader)
                is_god = any(god.lower() in user.lower() for god in GOD_TRADERS)
                # 2. 检查是否包含你关心的标的 (Market Keywords)
                is_target = any(kw.lower() in content.lower() for kw in MARKET_KEYWORDS)
                # 3. 检查评分
                is_high_score = score >= MIN_SCORE
                
                if is_god and is_target and is_high_score:
                    results.append({
                        "title": f"[{user}] Score: {score}",
                        "desc": f"内容: {content}<br><br>关注标的: {', '.join([k for k in MARKET_KEYWORDS if k.lower() in content.lower()])}",
                        "link": f"https://x.com/{user.split(' ')[0]}" # 尝试拼凑推特链接
                    })
            except:
                continue
        return results
    except Exception as e:
        print(f"抓取异常: {e}")
        return []

def build_xml(items):
    now = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")
    xml = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
    <title>God Traders Alpha Feed</title>
    <link>https://x-gpt.bwequation.com/</link>
    <description>监控: BTC/ETH/USD/Gold/SPX/Nasdaq</description>
    <lastBuildDate>{now}</lastBuildDate>"""
    
    if not items:
        xml += f"<item><title>暂无匹配今日行情的高分推文</title><description>当前时间: {now}</description></item>"
    else:
        for item in items:
            xml += f"""
    <item>
        <title><![CDATA[{item['title']}]]></title>
        <description><![CDATA[{item['desc']}]]></description>
        <link>{item['link']}</link>
        <guid isPermaLink="false">{hash(item['desc'])}</guid>
    </item>"""
    
    xml += "\n</channel></rss>"
    return xml

# 运行
final_items = get_real_data()
rss_content = build_xml(final_items)

with open("rss.xml", "w", encoding="utf-8") as f:
    f.write(rss_content)
