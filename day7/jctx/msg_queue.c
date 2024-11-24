#include <stdio.h>
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
