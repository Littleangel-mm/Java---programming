# mysql 笔记

## mysql的安装

因为它全是英文，不方便我们理解，比如自定义安装  
我就找了半天，真是对计算机一窍不通
musql的安装，可以去它的官网  
https://www.mysql.com/cn/downloads/  
找一个合适的的版本，但是这个不是我记录的重点  
我要跳过它



## mysql语言
查表建表  
<font color= #871F78>
CREATE TABLE teacher(  
    teacherid BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '教师ID',  
    tname VARCHAR(200) COMMENT '教师名称',  
    age INT COMMENT '年龄'  
) COMMENT '教师表'; 
</font> 




增加数据  
<font color= #871F78>
INSERT into teacher VALUES(10001,'王老师',34);  
INSERT into teacher VALUES(DEFAULT,'黄老师',58);  
INSERT into teacher VALUES(DEFAULT,'李老师',97);
</font> 


查表  
<font color= #871F78>
SELECT * from teacher;
</font> 



修改表  
<font color= #871F78>
UPDATE teacher 
SET teacherid = 3, 
    tname = '张三', 
    age = 33
WHERE teacherid = 3;
</font>


删除表   
<font color= #871F78> 
DELETE from teacher WHERE teacherid=3;  

 SELECT * from teacher;
 </font>

## Java连接数据库
我的重点是如何使用Java来连接数据库  
实现增删修改  
翻看了很多大佬的视频和博客，他们告诉我，用的是JDBC，它是个啥东西  
一个mysql驱动  我们可以在官网上面找到它 如图
![](http://xtstuc.dyfl.top/xtsimage/sql1.jpg)
![](http://xtstuc.dyfl.top/xtsimage/sql2.jpg)
![](http://xtstuc.dyfl.top/xtsimage/sql3.png)
![](http://xtstuc.dyfl.top/xtsimage/sql4.png)
![](http://xtstuc.dyfl.top/xtsimage/sql5.png)
![](http://xtstuc.dyfl.top/xtsimage/sql6.png)

下载好后解压,在项目文件夹里面新建立一个文件夹 lib  
将mysql-connector-j-8.1.0.jar放到lib里面
![](http://xtstuc.dyfl.top/xtsimage/sql10.png)
![](http://xtstuc.dyfl.top/xtsimage/sql9.png)

用IDE打开项目文件，选中lib文件夹，左键点击，选择添加到库
![](http://xtstuc.dyfl.top/xtsimage/sql11.png)
就可以通过它使Java可以连接到数据库了  
我已经写完了  
看看运行效果吧
![](http://xtstuc.dyfl.top/xtsimage/sql7.png)
![](http://xtstuc.dyfl.top/xtsimage/sql8.png)














































