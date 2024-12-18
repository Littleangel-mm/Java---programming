#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>
#include <errno.h>
#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>

#define SEMKEY (key_t)0x200

typedef union _senum {
    int val;
    struct semid_ds *buf;
    ushort *array;
} semun;

int semid;
int count = 0;  // 读者计数
FILE *fp, *fp1, *fp2;

struct sembuf prmutex = {0, -1, 0}, pwmutex = {1, -1, 0}, ps = {2, -1, 0}; // P操作
struct sembuf vrmutex = {0, 1, 0}, vwmutex = {1, 1, 0}, vs = {2, 1, 0};   // V操作

int initsem() {
    semun x;
    x.val = 1;

    // 信号量初始化
    if ((semid = semget(SEMKEY, 3, 0600 | IPC_CREAT | IPC_EXCL)) == -1) {
        if (errno == EEXIST) {
            semid = semget(SEMKEY, 3, 0);
        }
    }

    // 设置各个信号量的值
    if (semctl(semid, 0, SETVAL, x) == -1) {
        perror("semctl failed for prmutex\n");
        return -1;
    }

    if (semctl(semid, 1, SETVAL, x) == -1) {
        perror("semctl failed for pwmutex\n");
        return -1;
    }

    if (semctl(semid, 2, SETVAL, x) == -1) {
        perror("semctl failed for ps\n");
        return -1;
    }

    return semid;
}

int main() {
    int i, j, k;
    int a[30];  // 存储数据

    semid = initsem();  // 初始化信号量

    // 启动第一个读者进程
    if (fork() == 0) {
        // reader 进程
        semop(semid, &prmutex, 1);  // 读操作 P 操作
        if (count == 0) semop(semid, &pwmutex, 1);  // 堵塞写进程
        count = count + 1;  // 增加读者数
        printf("Reader 1 - count = %d\n", count);
        semop(semid, &vrmutex, 1);  // 释放读锁

        for (i = 0; i < 30; i++) {
            printf("reader 1 %d\n", a[i]);
            sleep(1);
        }

        semop(semid, &prmutex, 1);  // 再次加锁
        count = count - 1;  // 减少读者数
        printf("Reader 1 - count = %d\n", count);
        if (count == 0) semop(semid, &vwmutex, 1);  // 唤醒写进程
        semop(semid, &vrmutex, 1);  // 释放读锁
        exit(0);
    }
    
    // 启动写进程
    if (fork() == 0) {
        // writer 进程
        semop(semid, &pwmutex, 1);  // P 操作，锁定写进程
        printf("I am the writer:\n");
        for (k = 0; k < 30; k++) {
            a[k] = 3 * k;  // 写操作
        }
        printf("Write finish!!!!\n");
        semop(semid, &vwmutex, 1);  // V 操作，释放写锁
        exit(0);
    }

    // 启动第二个读者进程
    if (fork() == 0) {
        // reader 2 进程
        semop(semid, &prmutex, 1);  // 读操作 P 操作
        count = 2;  // 设置为2个读者
        printf("Reader 2 - count = %d\n", count);
        semop(semid, &vrmutex, 1);  // 释放读锁

        for (j = 0; j < 30; j++) {
            printf("reader 2 %d\n", a[j]);
            sleep(1);
        }

        semop(semid, &prmutex, 1);  // 再次加锁
        count = count - 1;  // 减少读者数
        printf("Reader 2 - count = %d\n", count);
        if (count == 0) semop(semid, &vwmutex, 1);  // 唤醒写进程
        semop(semid, &vrmutex, 1);  // 释放读锁
        exit(0);
    }

    // 等待所有进程结束
    wait(NULL);
    wait(NULL);
    wait(NULL);

    return 0;
}
