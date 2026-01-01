#单个视频爬取 普通版本
import requests
import re
import json
import os

def crawl_bilibili_video(url, cookie=None):
    """
    爬取B站视频
    :param url: B站视频网址
    :param cookie: 登录后的Cookie（可选，用于获取更高清晰度）
    """
    # 创建保存视频和音频的目录
    if not os.path.exists('video'):
        os.makedirs('video')
    if not os.path.exists('audio'):
        os.makedirs('audio')
    
    # 设置请求头
    headers = {
        "Referer": url,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    
    # 如果提供了Cookie，则添加到请求头中
    if cookie:
        headers["Cookie"] = cookie
    
    try:
        # 发送请求获取网页内容
        print("正在获取网页内容...")
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        html = response.text
        
        # 解析数据: 提取视频标题
        title_match = re.findall('title="(.*?)"', html)
        if title_match:
            title = title_match[0]
            # 清理文件名中的非法字符
            title = re.sub(r'[\\/:*?"<>|]', '', title)
            print(f"视频标题: {title}")
        else:
            title = "未命名视频"
            print("未找到视频标题，使用默认名称")
        
        # 提取视频信息
        info_match = re.findall('window.__playinfo__=(.*?)</script>', html)
        if info_match:
            info = info_match[0]
            # info -> json字符串转成json字典
            json_data = json.loads(info)
            
            # 提取视频链接
            video_url = json_data['data']['dash']['video'][0]['baseUrl']
            print(f"视频链接: {video_url}")
            
            # 提取音频链接
            audio_url = json_data['data']['dash']['audio'][0]['baseUrl']
            print(f"音频链接: {audio_url}")
            
            # 下载视频
            print("正在下载视频...")
            video_content = requests.get(url=video_url, headers=headers).content
            video_path = os.path.join('video', f'{title}.mp4')
            with open(video_path, mode='wb') as v:
                v.write(video_content)
            print(f"视频已保存至: {video_path}")
            
            # 下载音频
            print("正在下载音频...")
            audio_content = requests.get(url=audio_url, headers=headers).content
            audio_path = os.path.join('audio', f'{title}.mp3')
            with open(audio_path, mode='wb') as a:
                a.write(audio_content)
            print(f"音频已保存至: {audio_path}")
            
            print("下载完成！视频和音频已分别保存在不同的文件夹中。")
            return True
        else:
            print("未找到视频信息，请检查网址是否正确或Cookie是否有效")
            return False
    except Exception as e:
        print(f"下载过程中出现错误: {e}")
        return False

if __name__ == "__main__":
    # 示例视频URL（请替换为你想要下载的视频URL）
    url = 'https://www.bilibili.com/video/BV1WLW1zVEqf/?spm_id_from=333.1007.top_right_bar_window_history.content.click&vd_source=49b03b18d881c15637eb6648c7c57262'
    
    # 如果需要更高清晰度，可以提供登录后的Cookie
    # 注意：请使用你自己的Cookie，以下仅为示例
    cookie =  "buvid3=576D4A28-5A7E-1D14-59FF-E23A6C79E49141762infoc; b_nut=1743749241; _uuid=D429A593-C2B3-D821-7DC10-24A45BC5F710A42687infoc; buvid_fp=9c2185edad9ef88994e0cef01f836cab; enable_web_push=DISABLE; enable_feed_channel=ENABLE; rpdid=|(u))um)|Y)R0J'u~RJ~Rmk~R; DedeUserID=345292099; DedeUserID__ckMd5=3ab1d97e73bf8881; header_theme_version=OPEN; theme-tip-show=SHOWED; theme-avatar-tip-show=SHOWED; CURRENT_QUALITY=80; theme-switch-show=SHOWED; home_feed_column=5; buvid4=3F19E4D6-C445-215D-3360-CB8A76B40BD242423-025040406-UuZBElLLk/hJyk63zz0LdQ%3D%3D; browser_resolution=1912-962; ogv_device_support_hdr=0; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjIyNTYxNzMsImlhdCI6MTc2MTk5NjkxMywicGx0IjotMX0.o9t50fKML4cpNdPF3ZVSv_4dXQ7VvceDXcoC_P0u_Xw; bili_ticket_expires=1762256113; SESSDATA=c58c6f1c%2C1777612170%2Cef24e%2Ab2CjCHu5YHu4lncYiJedC84kZ--RmtnzyhLxvQGF2NSwOJ_yXHGvbixF2Qs7ocVRIvCtwSVjlXcXllX1RUYk9va2tIN1lpNzdKUTVKbVhqNm5GYkNMclZqTllJMDN1WXZJTzB4R09KaUc5REQ3LTZiRWN6TW1fS2dHTXpUR2FQMGUtYl9CNDVtYWxBIIEC; bili_jct=6020069d4eca3490add392ec8e95f4ec; bp_t_offset_345292099=1130528928104972288; b_lsid=BEDDA53E_19A4838DEF2; CURRENT_FNVAL=4048; sid=hbc7xpg1; bmg_af_switch=1; bmg_src_def_domain=i0.hdslb.com" # "buvid3=...; SESSDATA=...; bili_jct=..."
    
    print("B站视频爬虫程序启动...")
    print(f"目标网址: {url}")
    
    success = crawl_bilibili_video(url, cookie)
    
    if success:
        print("视频爬取成功！")
    else:
        print("视频爬取失败，请检查网络连接、网址有效性或Cookie设置")


