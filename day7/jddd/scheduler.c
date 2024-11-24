#include <stdio.h>
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


