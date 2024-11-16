# ffmpeg 简单的命令

安装ffmpeg--官网下载  
https://ffmpeg.org/  
找到合适的版本 解压 改名


配置环境变量  
找到存放的路径
![](http://xtstuc.dyfl.top/xtsimage/D2.png)

在高级设置里面找到path 将路径添加进去
![](http://xtstuc.dyfl.top/xtsimage/D1.png)  
点击确定保存


打开win + r 打开cmd
输入 ffmpeg -version 出现如图安装成功
![](http://xtstuc.dyfl.top/xtsimage/D3.png)



提取视频所有的帧  
ffmpeg -i episode_01_1.mp4 -r 25 -qscale:v 2 out/%04d.jpg

合成视频
<!-- ffmpeg -i %04d.png -c:v libX264 -vf fps=25 -pix_fmt yuv420p out.mp4

ffmpeg -i %04d.ascii.png -c:v libx264 -vf fps=25 -pix_fmt yuv420p out.mp4 -->

ffmpeg -i %04d.ascii.png -c:v libx264 -vf fps=25 -pix_fmt yuv420p out.mp4


使用方法  
新建终端
python assers3.py image output  
等待一段时间即可，效果图  
![](http://xtstuc.dyfl.top/xtsimage/D4.png)

在使用ffmpeg的时候，可能会出现合成的MP4视频无法播放  
也许是编码器的原因 output文件夹会生成所有字符序列图    
 可以用PR或blenser在合一次
 这样就实现了字符画的制作

 当然其实PR 和ffmpeg都自带字符画转化功能  
 本次代码就图一乐




