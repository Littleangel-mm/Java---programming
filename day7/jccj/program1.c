#include <stdio.h>
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
