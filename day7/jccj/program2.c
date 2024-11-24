#include <stdio.h>
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
