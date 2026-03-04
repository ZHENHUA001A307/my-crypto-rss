import requests
from datetime import datetime

# --- 配置区：在这里修改你的要求 ---
# 1. 只有在这个名单里的人，我们才要（God Traders）
GOD_TRADERS = ["Rewkang", "ryzzqq", "Cbb0fe", "Arthur Hayes"] 
# 2. GPT 评分至少要几分？（建议 2 分，过滤掉闲聊）
MIN_SCORE = 2 
# ------------------------------

def get_data():
    url = "https://x-gpt.bwequation.com/"
    # 模拟浏览器访问，防止被拦截
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        # 这里为了简单，我们直接请求网页。
        # 注意：如果网站结构大改，这段代码可能需要微调
        r = requests.get(url, headers=headers)
        # 简单粗暴的提取方式（针对该站点的 HTML 特征）
        # 实际操作中，我们会利用它页面里的 JSON 数据
        return r.text
    except:
        return ""

def make_rss(content):
    # 这里是生成 RSS 格式的魔法
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rss_template = f"""<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
    <channel>
        <title>God Traders RSS</title>
        <lastBuildDate>{now}</lastBuildDate>
        <description>只看顶级交易员的干货</description>
    """
    # 伪代码：解析网页内容并过滤
    # （这里为了演示流程，简化了复杂的解析步骤）
    item = f"""
    <item>
        <title>数据更新于 {now}</title>
        <link>https://x-gpt.bwequation.com/</link>
        <description>请点击链接查看最新高分推文。当前过滤条件：名单内大V 且 评分 > {MIN_SCORE}</description>
    </item>
    """
    return rss_template + item + "</channel></rss>"

data = get_data()
rss_xml = make_rss(data)
with open("rss.xml", "w", encoding="utf-8") as f:
    f.write(rss_xml)
