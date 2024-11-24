# 操作系统实验

## 实验一 熟悉linux
实验一要求我们尝试linux的各种基础命令  
这是我的实验结果  
在linux的终端输入    
<font color=pink>history</font>  
就可以查看历史操作的指令  
![](http://xtstuc.dyfl.top/xtsimage/sy1.1.png)
![](http://xtstuc.dyfl.top/xtsimage/sy1.2.png)





## 实验二：Linux下C程序编写  
首先我们查看自己的Linux下有没有c语言的编译环境  
在终端输入    
<font color=pink>gcc  --version</font>  
<font color=pink>whereis gcc</font>  
查看版本信息和路径  
![](http://xtstuc.dyfl.top/xtsimage/sy2.5.png)  

如果没有我们需要自己安装一下
### <font color=red>centos下安装gcc</font>

sudo yum install gcc      &emsp;&emsp;&emsp;#CentOS/RedHat 系统  
<!-- sudo apt-get install gcc  &emsp;&emsp;&emsp;#Ubuntu/Debian 系统   -->

<font color=yellow>编译 </font>  
gcc <源文件.c> -o <重命名>  

gcc tcs.c -o tcs -lm  

<font color=yellow>运行  </font>  
./<文件名>  
./tcs  

<font color=yellow>编写</font>  
cd ~ 回到目录  
我创建了一个新的文件夹，test用来存放实验代码  
<font color=pink>mkdir test</font>  
进入目录  
<font color=pink>cd test</font>  
建立一个C文件  
<font color=pink>touch tcs.c</font>  
然后进入这个文件  
<font color=pink>vi tcs.c</font>  
就可以开始编写了  
我写的一个贪吃蛇  
通过w,s,a,d来控制方向  
ESC退出，源码我会放到我的GitHub  
https://github.com/Littleangel-mm/Java---programming/blob/main/Day2/linuxtcs.c  
运行的截图如下
![](http://xtstuc.dyfl.top/xtsimage/sy2.3.png)
进入正题，我去看了实验手册，我发现我做错了  
 编写简单的C程序，功能为在屏幕上输出“Hellogcc!"。利用该程序练习使用gcc编译
器的E、S、c、o、g选项，观察不同阶段所生成的文件，即*.c、*.i、*.s、*.o文件和可执行文件
我在test里面新建立了一个文件夹linuxxt  
<font color=pink>cd linuxxt</font>  
<font color=pink>touch hellogcc.c</font>  
输入源码  
```#include <stdio.h>

int main() {
    printf("Hellogcc!\n");
    return 0;
}
```
预处理阶段（生成 .i 文件）  
<font color=pink>gcc -E hellogcc.c -o hellogcc.i</font>  
编译阶段（生成 .s 汇编代码文件）  
<font color=pink>gcc -S hellogcc.c -o hellogcc.s</font>  
汇编阶段（生成 .o 目标文件）  
<font color=pink>gcc -c hellogcc.c -o hellogcc.o
</font>  
链接阶段（生成可执行文件）  
<font color=pink>gcc hellogcc.o -o hellogcc
</font>  
执行生成的可执行文件  
<font color=pink>./hellogcc
</font>  
调试选项： 如果需要生成包含调试信息的可执行文件，可以使用 -g 选项  
<font color=pink>gcc -g hellogcc.c -o hellogcc
</font>  
运行效果
![](http://xtstuc.dyfl.top/xtsimage/sy2.7.png)

## 多文件 C 程序及 Makefile 的实现
在liunxxt的路径下，新建立了一个文件夹duowj  
<font color=pink>cd duowj</font>
首先建立一个头文件 greeting.h  
<font color=pink>touch duowj</font>  
在里面输入  
```#ifndef _GREETING_H
#define _GREETING_H

void greeting(char *name);

#endif
```
再建立函数文件 greeting.c  
<font color=pink>touch greeting.c</font>  
输入以下测试代码  
```#include <stdio.h>
#include "greeting.h"

void greeting(char *name) {
    printf("Hello, %s!\n", name);
}
```
接着是主函数文件 myapp.c  
<font color=pink>touch myapp.c</font>   
输入以下测试代码
```#include <stdio.h>
#include "greeting.h"

#define N 10

int main() {
    char name[N];
    printf("Your name, please: ");
    scanf("%s", name);
    greeting(name);
    return 0;
}
```
然后就是makefile的编写
新建一个文件明眸为makefile  
<font color=pink>touch makeflie</font>  
在makefile输入以下测试的依赖关系  
```# 编译器及其选项
CC = gcc
CFLAGS = -Wall -g

# 目标文件和最终程序
OBJS = myapp.o greeting.o
TARGET = myapp

# 目标规则
all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(OBJS)

myapp.o: myapp.c greeting.h
	$(CC) $(CFLAGS) -c myapp.c

greeting.o: greeting.c greeting.h
	$(CC) $(CFLAGS) -c greeting.c

clean:
	rm -f $(OBJS) $(TARGET)
```

编译程序  
<font color=pink>make</font>  
运行程序  
<font color=pink>./myapp
</font>   
运行效果如图
![](http://xtstuc.dyfl.top/xtsimage/sy2.8.png)

清理生成的文件  
<font color=pink>make clean
</font>  
这将删除目标文件和可执行文件  
至此 实验二完成

## 实验三：进程的创建
回到我的/root/testc/linuxxt  
这个路径下，我要在这里创建一个新的文件夹jccj  
然后创建两个C文件program1和program2  
<font color=pink>touch program1</font>  
<font color=pink>touch program1</font>  
 <font color=red>program1 测试代码</font>
 ```#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdlib.h>

int main() {
    pid_t childpid; // 子进程的PID
    int retval;     // 子进程的返回值
    int status;     // 父进程接收到的子进程状态

    // 创建一个新进程
    childpid = fork();

    if (childpid >= 0) { // fork() 成功
        if (childpid == 0) { // 当前是子进程
            printf("CHILD: I am the child process!\n");
            printf("CHILD: Here's my PID: %d\n", getpid());
            printf("CHILD: My parent's PID is: %d\n", getppid());
            printf("CHILD: The value of fork() return is: %d\n", childpid);

            // 子进程执行
            printf("CHILD: Sleep for 1 second...\n");
            sleep(1);
            printf("CHILD: Enter an exit value (0~255): ");
            scanf("%d", &retval); // 输入子进程退出码
            printf("CHILD: Goodbye!\n");
            exit(retval); // 子进程退出，返回输入值
        } else { // 当前是父进程
            printf("PARENT: I am the parent process!\n");
            printf("PARENT: Here's my PID: %d\n", getpid());
            printf("PARENT: The value of my child's PID is: %d\n", childpid);
            printf("PARENT: I will now wait for my child to exit.\n");

            // 父进程等待子进程结束
            wait(&status);
            printf("PARENT: Child's exit code is: %d\n", WEXITSTATUS(status));
            printf("PARENT: Goodbye!\n");
            exit(0);
        }
    } else { // fork() 失败
        perror("fork error!");
        exit(1);
    }
}
```
<font color=red>program2 测试代码</font>
```#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdlib.h>

int main() {
    pid_t childpid;

    // 创建一个新进程
    childpid = fork();

    if (childpid >= 0) { // fork() 成功
        if (childpid == 0) { // 当前是子进程
            printf("CHILD: I am the child process! Executing 'ls'.\n");
            printf("CHILD: Here's my PID: %d\n", getpid());
            execlp("ls", "ls", "-l", NULL); // 使用 execlp 执行 ls -l 命令

            // 如果 exec 执行失败
            perror("execlp error");
            exit(1);
        } else { // 当前是父进程
            printf("PARENT: I am the parent process!\n");
            printf("PARENT: Here's my PID: %d\n", getpid());
            printf("PARENT: Waiting for my child process to finish.\n");

            // 父进程等待子进程结束
            wait(NULL);
            printf("PARENT: Child process finished. Goodbye!\n");
            exit(0);
        }
    } else { // fork() 失败
        perror("fork error!");
        exit(1);
    }
}
```
 然后我们使用编译功能  
<font color=pink>gcc program1.c -o program1</font>    
<font color=pink>gcc program2.c -o program2</font>  
接下来运行结果如下
![](http://xtstuc.dyfl.top/xtsimage/sy3.1.png)
![](http://xtstuc.dyfl.top/xtsimage/sy3.2.png)
![](http://xtstuc.dyfl.top/xtsimage/sy3.3.png)

至此 实验三完成  

##  实验四进程调度
我还是要回到我的linuxxt路径下，在这里建立新的文件夹jddd  
<font color=pink>mkdir jddd</font>  
<font color=pink>cd jddd</font>  
<font color=pink>touch scheduler</font>     
<font color=pink>vi scheduler</font>  
输入测试代码
```#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 定义进程控制块结构体
struct pcb {
    char name[10];        // 进程名
    char state;           // 进程状态 ('W'：就绪，'R'：运行)
    int nice;             // 优先级
    int ntime;            // 需要运行的时间
    int rtime;            // 已经运行的时间
    struct pcb* link;     // 链接下一个进程
};

// 全局变量
struct pcb* ready = NULL; // 就绪队列头指针
struct pcb* p = NULL;     // 当前运行的进程

typedef struct pcb PCB;

// 函数声明
void sort();             // 对就绪队列排序
void input();            // 输入进程信息
int queue_size();        // 获取队列大小
void disp(PCB* pr);      // 显示单个进程信息
void check();            // 显示当前运行进程和就绪队列状态
void destroy();          // 撤销进程
void running();          // 运行一个时间片

// 就绪队列排序函数，优先级从高到低
void sort() {
    if (ready == NULL || (p->nice > ready->nice)) {
        // 插入队首
        p->link = ready;
        ready = p;
        return;
    }

    PCB* first = ready;
    PCB* second = first->link;
    while (second != NULL) {
        if (p->nice > second->nice) {
            // 插入到 first 和 second 之间
            first->link = p;
            p->link = second;
            return;
        }
        first = second;
        second = second->link;
    }
    // 插入队尾
    first->link = p;
    p->link = NULL;
}

// 输入进程信息并建立就绪队列
void input() {
    int num;
    printf("\n请输入被调度的进程数目: ");
    scanf("%d", &num);

    for (int i = 0; i < num; i++) {
        p = (PCB*)malloc(sizeof(PCB));
        if (!p) {
            printf("内存分配失败！\n");
            exit(EXIT_FAILURE);
        }

        printf("\n进程号 No.%d:\n", i + 1);
        printf("输入进程名: ");
        scanf("%s", p->name);
        printf("输入进程优先数: ");
        scanf("%d", &p->nice);
        printf("输入进程运行时间: ");
        scanf("%d", &p->ntime);

        p->rtime = 0;
        p->state = 'W';
        p->link = NULL;

        sort(); // 按优先级插入就绪队列
    }
}

// 统计就绪队列中进程数
int queue_size() {
    int count = 0;
    PCB* pr = ready;
    while (pr != NULL) {
        count++;
        pr = pr->link;
    }
    return count;
}

// 显示单个进程信息
void disp(PCB* pr) {
    if (pr) {
        printf("%s\t%c\t%d\t%d\t%d\n", pr->name, pr->state, pr->nice, pr->ntime, pr->rtime);
    }
}

// 显示当前运行进程和就绪队列状态
void check() {
    printf("\n**** 当前正在运行的进程是: %s ****\n", p->name);
    printf("进程名\t状态\t优先级\t总时间\t已运行时间\n");
    disp(p);

    PCB* pr = ready;
    if (pr != NULL) {
        printf("\n**** 当前就绪队列状态: ****\n");
        while (pr != NULL) {
            disp(pr);
            pr = pr->link;
        }
    } else {
        printf("\n就绪队列为空\n");
    }
}

// 撤销运行完成的进程
void destroy() {
    printf("进程 [%s] 已完成。\n", p->name);
    free(p);
}

// 运行当前进程一个时间片
void running() {
    p->rtime++; // 增加运行时间

    if (p->rtime == p->ntime) {
        destroy(); // 运行完成，撤销进程
    } else {
        p->nice--;     // 降低优先级
        p->state = 'W'; // 设置为就绪状态
        sort();         // 重新插入就绪队列
    }
}

// 主函数
int main() {
    int len, h = 0;
    char ch;

    input(); // 输入进程信息
    len = queue_size();

    while (len != 0 && ready != NULL) {
        h++;
        printf("\n=== 第 %d 次调度 ===\n", h);

        p = ready;         // 取队首进程运行
        ready = ready->link; // 更新就绪队列
        p->link = NULL;
        p->state = 'R';    // 设置为运行状态

        check();  // 显示当前状态
        running(); // 执行一个时间片
        len = queue_size(); // 更新队列长度

        printf("\n按任意键继续...");
        getchar(); // 等待用户输入
    }

    printf("\n\n所有进程已经运行完成！\n");
    return 0;
}
```
编译  
<font color=pink>gcc -std=c99 scheduler.c -o scheduler
</font>  
运行    
<font color=pink>./scheduler
</font>   
输出格式 
```请输入被调度的进程数目: 3

进程号 No.1:
输入进程名: P1
输入进程优先数: 5
输入进程运行时间: 4

进程号 No.2:
输入进程名: P2
输入进程优先数: 10
输入进程运行时间: 3

进程号 No.3:
输入进程名: P3
输入进程优先数: 7
输入进程运行时间: 5
```
结果样式  
```=== 第 1 次调度 ===
**** 当前正在运行的进程是: P2 ****
进程名    状态    优先级    总时间    已运行时间
P2        R       10        3        0

**** 当前就绪队列状态: ****
P3        W       7         5        0
P1        W       5         4        0

按任意键继续...
```
如果想退出，可以按ctrl + C  
运行效果图
![](http://xtstuc.dyfl.top/xtsimage/sy4.1.png)
![](http://xtstuc.dyfl.top/xtsimage/sy4.2.png)
![](http://xtstuc.dyfl.top/xtsimage/sy4.3.png)

至此，实验四完成


## 实验五 进程通信
我还是要回到我的linuxxt路径下，在这里建立新的文件夹jctx  
<font color=pink>mkdir jctx</font>  
<font color=pink>cd jctx</font>  
<font color=pink>vi msg_queue.c</font>  
测试源码如下
```#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <unistd.h>
#include <sys/wait.h>

// 定义消息结构
struct msgbuf {
    long mtype;          // 消息类型
    char mtext[100];     // 消息内容
};

int main() {
    int msgid;
    key_t key;
    struct msgbuf sndbuf, rcvbuf;
    pid_t pid;

    // 创建消息队列的键值
    key = ftok("progfile", 65);
    if (key == -1) {
        perror("ftok failed");
        exit(EXIT_FAILURE);
    }

    // 创建消息队列
    msgid = msgget(key, 0666 | IPC_CREAT);
    if (msgid == -1) {
        perror("msgget failed");
        exit(EXIT_FAILURE);
    }

    // 创建子进程
    pid = fork();
    if (pid == -1) {
        perror("fork failed");
        exit(EXIT_FAILURE);
    } else if (pid > 0) {
        // 父进程
        // 写入消息队列
        sndbuf.mtype = 1;  // 设置消息类型
        strcpy(sndbuf.mtext, "今天下午我们要继续做实验!");
        if (msgsnd(msgid, &sndbuf, sizeof(sndbuf.mtext), 0) == -1) {
            perror("msgsnd failed");
            exit(EXIT_FAILURE);
        }
        printf("父进程写入消息队列: %s\n", sndbuf.mtext);

        // 等待子进程应答
        if (msgrcv(msgid, &rcvbuf, sizeof(rcvbuf.mtext), 2, 0) == -1) {
            perror("msgrcv failed");
            exit(EXIT_FAILURE);
        }
        printf("父进程收到子进程的应答: %s\n", rcvbuf.mtext);

        // 等待子进程结束
        waitpid(pid, NULL, 0);

        // 删除消息队列
        if (msgctl(msgid, IPC_RMID, NULL) == -1) {
            perror("msgctl failed");
            exit(EXIT_FAILURE);
        }
        printf("父进程删除消息队列.\n");

    } else {
        // 子进程
        // 读取消息队列
        if (msgrcv(msgid, &rcvbuf, sizeof(rcvbuf.mtext), 1, 0) == -1) {
            perror("msgrcv failed");
            exit(EXIT_FAILURE);
        }
        printf("子进程读取消息队列: %s\n", rcvbuf.mtext);

        // 子进程处理后发送应答消息
        sndbuf.mtype = 2;  // 设置消息类型为2，用于应答
        strcpy(sndbuf.mtext, "收到消息，处理完毕!");
        if (msgsnd(msgid, &sndbuf, sizeof(sndbuf.mtext), 0) == -1) {
            perror("msgsnd failed");
            exit(EXIT_FAILURE);
        }
        printf("子进程发送应答消息: %s\n", sndbuf.mtext);
    }

    return 0;
}
```
编译  
<font color=pink>gcc -o msg_queue msg_queue.c
</font>   
这个需要再建立一个progfile文件  
<font color=pink>touch progfile</font>
 
运行  
<font color=pink>./msg_queue</font>  
输出样式
```父进程写入消息队列: 今天下午我们要继续做实验!
子进程读取消息队列: 今天下午我们要继续做实验!
子进程发送应答消息: 收到消息，处理完毕!
父进程收到子进程的应答: 收到消息，处理完毕!
父进程删除消息队列.
```
看看运行效果
![](http://xtstuc.dyfl.top/xtsimage/sy5.1.png)  
至此实验五完成

## 总结

我的操作系统实验内容已经做得非常详细，覆盖了Linux环境中的基础命令、C程序编写、进程管理以及进程间通信等多个方面。我就是糕手！




























