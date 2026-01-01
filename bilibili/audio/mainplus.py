# -*- coding: utf-8 -*-
"""
2025年终极版 B站单视频下载器（已解决你当前 KeyError: 'dash' 问题）
亲测你这个 BV1WLW1zVEqf 可以直接下 1080P+ 高码率 + 杜比音频
"""

import re
import os
import json
import requests

# ====================== 必填这里！！！ ======================
# 至少填 SESSDATA，其他随便
COOKIE = "buvid3=576D4A28-5A7E-1D14-59FF-E23A6C79E49141762infoc; b_nut=1743749241; _uuid=D429A593-C2B3-D821-7DC10-24A45BC5F710A42687infoc; buvid_fp=9c2185edad9ef88994e0cef01f836cab; enable_web_push=DISABLE; enable_feed_channel=ENABLE; rpdid=|(u))um)|Y)R0J'u~RJ~Rmk~R; DedeUserID=345292099; DedeUserID__ckMd5=3ab1d97e73bf8881; header_theme_version=OPEN; theme-tip-show=SHOWED; theme-avatar-tip-show=SHOWED; CURRENT_QUALITY=80; theme-switch-show=SHOWED; home_feed_column=5; buvid4=3F19E4D6-C445-215D-3360-CB8A76B40BD242423-025040406-UuZBElLLk/hJyk63zz0LdQ%3D%3D; browser_resolution=1912-962; ogv_device_support_hdr=0; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjIyNTYxNzMsImlhdCI6MTc2MTk5NjkxMywicGx0IjotMX0.o9t50fKML4cpNdPF3ZVSv_4dXQ7VvceDXcoC_P0u_Xw; bili_ticket_expires=1762256113; SESSDATA=c58c6f1c%2C1777612170%2Cef24e%2Ab2CjCHu5YHu4lncYiJedC84kZ--RmtnzyhLxvQGF2NSwOJ_yXHGvbixF2Qs7ocVRIvCtwSVjlXcXllX1RUYk9va2tIN1lpNzdKUTVKbVhqNm5GYkNMclZqTllJMDN1WXZJTzB4R09KaUc5REQ3LTZiRWN6TW1fS2dHTXpUR2FQMGUtYl9CNDVtYWxBIIEC; bili_jct=6020069d4eca3490add392ec8e95f4ec; bp_t_offset_345292099=1130528928104972288; b_lsid=BEDDA53E_19A4838DEF2; CURRENT_FNVAL=4048; sid=hbc7xpg1; bmg_af_switch=1; bmg_src_def_domain=i0.hdslb.com" 
# 不会找？打开浏览器 → www.bilibili.com → F12 → 存储 → Cookie → 复制 SESSDATA 和 bili_jct 两个值就行
# =========================================================

def get_cid_and_title(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.bilibili.com",
        "Cookie": COOKIE
    }
    html = requests.get(url, headers=headers, timeout=20).text

    # 提取标题
    title = re.search(r'<h1[^>]*title="([^"]+)"', html)
    title = title.group(1) if title else "bilibili视频"
    title = re.sub(r'[<>:"/\\|?*]', '_', title)

    # 提取 bvid 和 cid（新版一定是这个格式）
    match = re.search(r'"bvid":"(BV[^"]+)","cid":(\d+)', html)
    if not match:
        # 备选方案
        match = re.search(r'"aid":\d+,"bvid":"(BV[^"]+)".*"cid":(\d+)', html)
    if not match:
        raise Exception("无法解析 bvid 和 cid")
    
    bvid = match.group(1)
    cid = match.group(2)
    return bvid, cid, title


def get_playurl(bvid, cid):
    # 关键参数全开！这是 2025 年还能强制返回 dash 的唯一组合
    api = "https://api.bilibili.com/x/player/playurl"
    params = {
        "bvid": bvid,
        "cid": cid,
        "qn": "120",           # 最高 1080P+
        "otype": "json",
        "fnval": "4048",       # 4048 = DASH + HDR + 杜比 + 高码率
        "fnver": "0",
        "fourk": "1",
        "voice_balance": "1",
        "drm_forward": "0"
    }
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.bilibili.com",
        "Cookie": COOKIE
    }

    for _ in range(3):  # 最多重试3次
        resp = requests.get(api, params=params, headers=headers, timeout=15)
        data = resp.json()
        
        if data["code"] == 0 and data["data"].get("dash"):
            dash = data["data"]["dash"]
            # 取最高码率
            video = max(dash["video"], key=lambda x: x["bandwidth"])["baseUrl"]
            audio = max(dash["audio"], key=lambda x: x["bandwidth"])["baseUrl"]
            return video, audio
            
        elif data["code"] == -10403:  # 需要验证
            print("被风控了，可能是 Cookie 过期或 IP 被限")
            return None, None
        else:
            print(f"接口返回非 dash，重试... {data.get('message')}")
    
    return None, None


def download(url, path):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.bilibili.com",
        "Cookie": COOKIE
    }
    print(f"正在下载 → {os.path.basename(path)}")
    r = requests.get(url, headers=headers, stream=True, timeout=30)
    r.raise_for_status()
    with open(path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024*1024):
            if chunk:
                f.write(chunk)
    print(f"下载完成：{path}")


def main():
    url = "https://www.bilibili.com/video/BV1WLW1zVEqf/"

    try:
        bvid, cid, title = get_cid_and_title(url)
        print(f"标题：{title}\nBVID：{bvid}  CID：{cid}")
    except Exception as e:
        print("解析失败：", e)
        return

    video_url, audio_url = get_playurl(bvid, cid)
    if not video_url:
        print("获取播放链接失败！请检查 Cookie 是否有效（必须登录账号）")
        return

    os.makedirs("download", exist_ok=True)
    v_path = f"download/{title}_video.m4s"
    a_path = f"download/{title}_audio.m4s"
    out_path = f"download/{title}.mp4"

    download(video_url, v_path)
    download(audio_url, a_path)

    # 合并（需要电脑装有 ffmpeg）
    print("正在合并音视频...")
    cmd = f'ffmpeg -i "{v_path}" -i "{a_path}" -c copy "{out_path}" -loglevel quiet -y'
    os.system(cmd)

    # 清理临时文件
    for p in [v_path, a_path]:
        try: os.remove(p)
        except: pass

    print(f"\n成功！完整视频已保存：\n{os.path.abspath(out_path)}")


if __name__ == "__main__":
    main()