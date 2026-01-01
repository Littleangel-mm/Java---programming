import os
import yt_dlp
from concurrent.futures import ThreadPoolExecutor, as_completed


def download_youtube_video(url, output_dir="downloads", cookie_file=None):
    """下载单个 YouTube 视频"""
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),  # 保存文件名
        'format': 'bestvideo+bestaudio/best', 
        'merge_output_format': 'mp4',  # 合并格式
        'quiet': True,  # 不输出太多信息
        'noplaylist': True,  # 单视频模式
        'nocheckcertificate': True,  # 忽略证书问题
        'progress_hooks': [lambda d: print_progress(d)],  # 下载进度
        'concurrent_fragment_downloads': 5,  # 每个视频并行下载 5 个片段
        'max_downloads': 0,  # 下载无限数量的视频
    }

    if cookie_file and os.path.exists(cookie_file):
        ydl_opts['cookiefile'] = cookie_file

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "未命名视频")
            print(f"下载完成: {title}")
            return True
    except Exception as e:
        print(f"下载失败 {url}：{e}")
        return False


def print_progress(d):
    """显示下载进度"""
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '').strip()
        eta = d.get('eta', 0)
        print(f"\r正在下载: {percent} 剩余 {eta}s", end='')
    elif d['status'] == 'finished':
        print("\n 正在合并音视频...")



def batch_download(video_urls, cookie_file=None, max_workers=10):
    """批量下载视频"""
    print(f"\n 共 {len(video_urls)} 个视频待下载...\n")
    success_count = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(download_youtube_video, url, "downloads", cookie_file): url
            for url in video_urls
        }
        for future in as_completed(futures):
            url = futures[future]
            try:
                if future.result():
                    success_count += 1
            except Exception as e:
                print(f"任务失败 {url}：{e}")

    print(f"\n下载完成：成功 {success_count}/{len(video_urls)} 个\n")


if __name__ == "__main__":
    urls_file = "urls.txt"
    if not os.path.exists(urls_file):
        print("未找到 urls.txt，请创建并写入 YouTube 视频链接。")
        exit(1)

    with open(urls_file, "r", encoding="utf-8") as f:
        video_urls = [line.strip() for line in f if line.strip()]

    if not video_urls:
        print("urls.txt 中没有可用的视频链接。")
        exit(1)

    # 你的 cookie.txt 文件路径（可以用浏览器导出）
    cookie_file = "youtube_cookies.txt"

    # 设置更高的并发线程数，增加下载速度
    batch_download(video_urls, cookie_file=cookie_file, max_workers=10)
