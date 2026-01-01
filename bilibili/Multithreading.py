#多视频爬取


import requests
import re
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed


def crawl_bilibili_video(url, cookie=None):
    """爬取单个B站视频"""
    headers = {
        "Referer": url,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    if cookie:
        headers["Cookie"] = cookie

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        html = response.text

        # 获取视频标题
        title_match = re.findall(r'<title.*?>(.*?)</title>', html)
        title = title_match[0].replace("_哔哩哔哩_bilibili", "").strip() if title_match else "未命名视频"
        title = re.sub(r'[\\/:*?"<>|]', '', title)
        print(f"\n正在下载：{title}")

        # 提取播放信息
        info_match = re.findall(r'window\.__playinfo__=(.*?)</script>', html)
        if not info_match:
            print(f"未找到视频信息：{url}")
            return False

        info = json.loads(info_match[0])
        video_url = info['data']['dash']['video'][0]['baseUrl']
        audio_url = info['data']['dash']['audio'][0]['baseUrl']

        # 创建目录
        os.makedirs("video", exist_ok=True)
        os.makedirs("audio", exist_ok=True)

        # 下载视频
        video_path = os.path.join("video", f"{title}.mp4")
        with open(video_path, "wb") as f:
            f.write(requests.get(video_url, headers=headers).content)

        # 下载音频
        audio_path = os.path.join("audio", f"{title}.mp3")
        with open(audio_path, "wb") as f:
            f.write(requests.get(audio_url, headers=headers).content)

        print(f"{title} 下载完成")
        return True

    except Exception as e:
        print(f"下载出错 {url}：{e}")
        return False


def batch_download(video_urls, cookie=None, max_workers=5):
    """批量下载视频（多线程）"""
    print(f"\n开始批量下载，共 {len(video_urls)} 个视频...\n")
    success_count = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(crawl_bilibili_video, url, cookie): url for url in video_urls}
        for future in as_completed(futures):
            url = futures[future]
            try:
                if future.result():
                    success_count += 1
            except Exception as e:
                print(f"任务失败：{url} - {e}")

    print(f"\n下载完成：成功 {success_count} 个 / 失败 {len(video_urls) - success_count} 个")


if __name__ == "__main__":
    # 从 txt 文件读取 URL 列表
    urls_file = "urls.txt"
    if not os.path.exists(urls_file):
        print(f"未找到 {urls_file} 文件，请创建一个包含视频链接的 txt 文件。")
        exit(1)

    with open(urls_file, "r", encoding="utf-8") as f:
        video_urls = [line.strip() for line in f if line.strip()]

    if not video_urls:
        print("urls.txt 中没有可用的视频链接。")
        exit(1)

    #  你的 Cookie（可选）
    cookie = "buvid3=576D4A28-5A7E-1D14-59FF-E23A6C79E49141762infoc; b_nut=1743749241; _uuid=D429A593-C2B3-D821-7DC10-24A45BC5F710A42687infoc; buvid_fp=9c2185edad9ef88994e0cef01f836cab; enable_web_push=DISABLE; enable_feed_channel=ENABLE; rpdid=|(u))um)|Y)R0J'u~RJ~Rmk~R; DedeUserID=345292099; DedeUserID__ckMd5=3ab1d97e73bf8881; header_theme_version=OPEN; theme-tip-show=SHOWED; theme-avatar-tip-show=SHOWED; CURRENT_QUALITY=80; theme-switch-show=SHOWED; home_feed_column=5; buvid4=3F19E4D6-C445-215D-3360-CB8A76B40BD242423-025040406-UuZBElLLk/hJyk63zz0LdQ%3D%3D; browser_resolution=1912-962; ogv_device_support_hdr=0; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjIyNTYxNzMsImlhdCI6MTc2MTk5NjkxMywicGx0IjotMX0.o9t50fKML4cpNdPF3ZVSv_4dXQ7VvceDXcoC_P0u_Xw; bili_ticket_expires=1762256113; SESSDATA=c58c6f1c%2C1777612170%2Cef24e%2Ab2CjCHu5YHu4lncYiJedC84kZ--RmtnzyhLxvQGF2NSwOJ_yXHGvbixF2Qs7ocVRIvCtwSVjlXcXllX1RUYk9va2tIN1lpNzdKUTVKbVhqNm5GYkNMclZqTllJMDN1WXZJTzB4R09KaUc5REQ3LTZiRWN6TW1fS2dHTXpUR2FQMGUtYl9CNDVtYWxBIIEC; bili_jct=6020069d4eca3490add392ec8e95f4ec; bp_t_offset_345292099=1130528928104972288; b_lsid=BEDDA53E_19A4838DEF2; CURRENT_FNVAL=4048; sid=hbc7xpg1; bmg_af_switch=1; bmg_src_def_domain=i0.hdslb.com"  # 例如 "SESSDATA=xxxx; bili_jct=xxxx"

    # 开始批量下载
    batch_download(video_urls, cookie=cookie, max_workers=5)
