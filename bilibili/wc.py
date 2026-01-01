#视频合成的脚本

import os
import subprocess

def merge_video_audio(video_path, audio_path, output_path):
    """
    使用 FFmpeg 合并视频和音频
    """
    try:
        # FFmpeg 命令
        # -i video_path: 输入视频
        # -i audio_path: 输入音频
        # -c:v copy: 复制视频流（不重新编码，加快处理）
        # -c:a aac: 编码音频为 AAC
        # -shortest: 输出时长与最短输入流匹配（自动处理音频/视频时长差异）
        # -y: 强制覆盖输出文件
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            "-y",
            output_path
        ]
        
        # 执行 FFmpeg 命令
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print(f"成功合成: {output_path}")
        else:
            print(f"合成失败 {video_path} + {audio_path} → {result.stderr}")
            
    except subprocess.CalledProcessError as e:
        print(f"合成失败 {video_path} + {audio_path} → {e.stderr}")
    except FileNotFoundError:
        print("错误：FFmpeg 未安装或未在系统 PATH 中")
    except Exception as e:
        print(f"合成失败 {video_path} + {audio_path} → {e}")

def auto_merge_from_folder(video_folder, audio_folder, output_folder):
    """
    自动匹配同名文件：video/xxx.mp4 + audio/xxx.mp3 → output/xxx_merged.mp4
    """
    # 1. 创建文件夹
    os.makedirs(video_folder, exist_ok=True)
    os.makedirs(audio_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    # 2. 获取文件列表
    video_files = [f for f in os.listdir(video_folder)
                   if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]
    audio_exts = ('.mp3', '.wav', '.m4a', '.aac')
    audio_files = [f for f in os.listdir(audio_folder) if f.lower().endswith(audio_exts)]

    if not video_files:
        print(f"警告：视频文件夹 '{video_folder}' 为空！")
        return
    if not audio_files:
        print(f"警告：音频文件夹 '{audio_folder}' 为空！")
        return

    # 3. 遍历视频，找同名音频（不区分扩展名）
    for video in video_files:
        base_name = os.path.splitext(video)[0]  # 无扩展名
        matched = False

        for audio in audio_files:
            if os.path.splitext(audio)[0] == base_name:
                video_path = os.path.join(video_folder, video)
                audio_path = os.path.join(audio_folder, audio)
                output_path = os.path.join(output_folder, f"{base_name}.mp4")

                # 验证文件存在
                if not os.path.exists(video_path):
                    print(f"错误：视频文件不存在: {video_path}")
                    continue
                if not os.path.exists(audio_path):
                    print(f"错误：音频文件不存在: {audio_path}")
                    continue

                print(f"正在处理: {video} + {audio}")
                merge_video_audio(video_path, audio_path, output_path)
                matched = True
                break

        if not matched:
            print(f"未找到音频: {video}")

# 
if __name__ == "__main__":
    # 设置 UTF-8 编码以支持中文文件名
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

    video_folder = 'video'
    audio_folder = 'audio'
    output_folder = 'output'

    auto_merge_from_folder(video_folder, audio_folder, output_folder)