import os
import re
import time
import logging
import pandas as pd
from tqdm import tqdm

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from gensim import corpora
from gensim.models.ldamodel import LdaModel

# ---- YouTube API ----
try:
    from googleapiclient.discovery import build
except Exception:
    build = None

# ---- Selenium ----
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except Exception:
    webdriver = None

# ==============================
# 🧩 参数区（小天使只改这里）
# ==============================
VIDEO_URL = "https://www.youtube.com/watch?v=Dqstaunpae0"  # 👈 改这里：你的视频链接
API_KEY = ""  # 👈 可选：填入你的 YouTube Data API v3 Key
MAX_COMMENTS = 100
OUT_FILE = "youtube_comments.csv"

# ==============================
# 初始化环境
# ==============================
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
EN_STOPWORDS = set(stopwords.words("english"))

# ==============================
# 工具函数
# ==============================
def extract_video_id(url: str) -> str:
    m = re.search(r"(?:v=|/watch\?v=|youtu\.be/)([A-Za-z0-9_-]{11})", url)
    if m:
        return m.group(1)
    raise ValueError("❌ 无法提取视频ID，请检查链接")

# ==============================
# YouTube API 获取评论
# ==============================
def fetch_comments_api(api_key, video_id, max_comments=100):
    if not build:
        raise RuntimeError("googleapiclient 未安装，请 pip install google-api-python-client")
    youtube = build("youtube", "v3", developerKey=api_key)
    comments, next_page = [], None
    pbar = tqdm(total=max_comments, desc="📡 API 抓取中")
    while len(comments) < max_comments:
        req = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            pageToken=next_page,
            maxResults=min(100, max_comments - len(comments)),
            textFormat="plainText",
            order="relevance"
        )
        resp = req.execute()
        for it in resp.get("items", []):
            snip = it["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "author": snip.get("authorDisplayName"),
                "text": snip.get("textDisplay"),
                "publishedAt": snip.get("publishedAt"),
                "likeCount": snip.get("likeCount", 0)
            })
            pbar.update(1)
            if len(comments) >= max_comments:
                break
        next_page = resp.get("nextPageToken")
        if not next_page:
            break
    pbar.close()
    return comments

# ==============================
# Selenium 备用抓取
# ==============================
def fetch_comments_selenium(video_url, max_comments=100):
    if webdriver is None:
        raise RuntimeError("selenium 未安装，请 pip install selenium")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    driver.get(video_url)
    time.sleep(3)
    body = driver.find_element(By.TAG_NAME, "body")

    for _ in range(5):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)

    comments, seen = [], set()
    pbar = tqdm(total=max_comments, desc="🌀 Selenium 抓取中")
    while len(comments) < max_comments:
        elems = driver.find_elements(By.CSS_SELECTOR, "#content-text")
        for el in elems:
            text = el.text.strip()
            if text and text not in seen:
                comments.append({"text": text})
                seen.add(text)
                pbar.update(1)
                if len(comments) >= max_comments:
                    break
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(1)
        if len(comments) >= max_comments:
            break
    driver.quit()
    pbar.close()
    return comments

# ==============================
# 文本处理 & LDA 模型
# ==============================
def preprocess_texts(texts):
    cleaned = []
    for t in texts:
        s = re.sub(r"http\S+", "", t.lower())
        s = re.sub(r"[^a-z0-9\s']", " ", s)
        tokens = word_tokenize(s)
        tokens = [w for w in tokens if w not in EN_STOPWORDS and len(w) > 2]
        cleaned.append(tokens)
    return cleaned

def lda_analysis(tokenized_texts, num_topics=5):
    dictionary = corpora.Dictionary(tokenized_texts)
    dictionary.filter_extremes(no_below=2, no_above=0.8)
    corpus = [dictionary.doc2bow(text) for text in tokenized_texts]

    lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, passes=10, random_state=42)
    print("\n🧠 LDA 模型主题：")
    for idx, topic in lda.print_topics(num_words=8):
        print(f"主题 {idx+1}: {topic}")
    return lda, dictionary, corpus

# ==============================
# 主程序
# ==============================
if __name__ == "__main__":
    video_id = extract_video_id(VIDEO_URL)
    print(f"🎬 正在爬取视频评论：{VIDEO_URL}\n")

    if API_KEY:
        try:
            comments = fetch_comments_api(API_KEY, video_id, MAX_COMMENTS)
        except Exception as e:
            logging.warning(f"API 抓取失败：{e}，改用 Selenium。")
            comments = fetch_comments_selenium(VIDEO_URL, MAX_COMMENTS)
    else:
        comments = fetch_comments_selenium(VIDEO_URL, MAX_COMMENTS)

    if not comments:
        print("❌ 没抓到评论，请检查网络或视频链接。")
        exit()

    # 保存 CSV
    df = pd.DataFrame(comments)
    df.to_csv(OUT_FILE, index=False, encoding="utf-8-sig")
    print(f"✅ 已保存 {len(df)} 条评论到文件：{OUT_FILE}")

    # 进行 LDA 分析
    texts = [c["text"] for c in comments if c.get("text")]
    tokenized = preprocess_texts(texts)
    lda_analysis(tokenized, num_topics=5)
    print("\n✨ 全部完成！")
