# ffmpeg 简单的命令
提取视频所有的帧
ffmpeg -i episode_01_1.mp4 -r 25 -qscale:v 2 out/%04d.jpg

合成视频
<!-- ffmpeg -i %04d.png -c:v libX264 -vf fps=25 -pix_fmt yuv420p out.mp4

ffmpeg -i %04d.ascii.png -c:v libx264 -vf fps=25 -pix_fmt yuv420p out.mp4 -->

ffmpeg -i %04d.ascii.png -c:v libx264 -vf fps=25 -pix_fmt yuv420p out.mp4


使用方法  
新建终端
python assers3.py image output




