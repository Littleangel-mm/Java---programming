import os
import glob
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import argparse

# 设置样本缩放率
sample_rate = 0.4

def ascii_art(file, output_folder, image_index):
    try:
        # 打开图像文件
        im = Image.open(file)

        # 计算字母纵横比
        font = ImageFont.load_default()
        aspect_ratio = font.getsize("x")[0] / font.getsize("x")[1]
        
        # 调整图像大小
        new_im_size = np.array(
            [im.size[0] * sample_rate, im.size[1] * sample_rate * aspect_ratio]
        ).astype(int)

        # 降低图像采样率
        im = im.resize(new_im_size)

        # 保留图像副本以进行颜色采样
        im_color = np.array(im)

        # 转换为灰度图像
        im = im.convert("L")

        # 转换为 numpy 数组进行图像处理
        im = np.array(im)

        # 按升序定义将形成最终 ASCII 的所有符号
        symbols = np.array(list(" .-vM"))

        # 将图像的最小和最大值标准化到符号索引范围
        im = (im - im.min()) / (im.max() - im.min()) * (symbols.size - 1)

        # 生成 ASCII 艺术
        ascii = symbols[im.astype(int)]

        # 创建用于绘制 ASCII 文本的输出图像
        letter_size = font.getsize("x")
        im_out_size = new_im_size * letter_size
        bg_color = "black"
        im_out = Image.new("RGB", tuple(im_out_size), bg_color)
        draw = ImageDraw.Draw(im_out)

        # 绘制文本
        y = 0
        for i, line in enumerate(ascii):
            for j, ch in enumerate(line):
                color = tuple(im_color[i, j])  # 从原始图像中取样颜色
                draw.text((letter_size[0] * j, y), ch[0], fill=color, font=font)
            y += letter_size[1]  # 增加 y 值以绘制下一行

        # 使用图像索引生成输出文件名（例如，0001.ascii.png）
        output_file = os.path.join(output_folder, f"{image_index:04d}.ascii.png")
        
        # 保存输出文件
        im_out.save(output_file)
        print(f"Saved {output_file}")
    except Exception as e:
        print(f"Error processing {file}: {e}")

def process_folder(folder_path, output_folder):
    # 使用 glob 获取文件夹中的所有图像文件
    image_files = glob.glob(os.path.join(folder_path, "*.jpg")) + \
                  glob.glob(os.path.join(folder_path, "*.jpeg")) + \
                  glob.glob(os.path.join(folder_path, "*.png"))

    # 确保输出文件夹存在，如果不存在，会自动创建它
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 处理每个图像文件
    for idx, image_file in enumerate(image_files, start=1):
        ascii_art(image_file, output_folder, idx)

if __name__ == "__main__":
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="Convert images in a folder to ASCII art.")
    parser.add_argument(
        "folder", type=str, help="input folder containing image files",
    )
    parser.add_argument(
        "output", type=str, help="output folder to save ASCII images",
    )
    args = parser.parse_args()

    # 处理文件夹中的图像文件
    process_folder(args.folder, args.output)

