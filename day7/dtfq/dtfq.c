#include <stdio.h>
#include <stdbool.h>  // 支持 bool 类型

float minsize = 5;  // 最小空闲区大小
int count1 = 0;     // 已分配作业数
int count2 = 0;     // 空闲区数目
#define M 10  // 空闲区表的最大项数
#define N 10  // 已分配区表的最大项数

// 已分配区表的定义
struct {
    float address;  // 已分分区起始地址
    float length;   // 已分配区长度，单位为字节
    int flag;       // 已分配区表登记栏标志，"0"表示空栏目
} used_table[N];  // 已分配区表，N表示最大作业数量

// 空闲分区表的定义
struct {
    float address;  // 空闲区起始地址
    float length;   // 空闲区长度，单位为字节
    int flag;       // 空闲区表登记栏标志，"1"表示未分配，"0"表示空栏目
} free_table[M];  // 空闲区表，M表示最大空闲区数量

// 函数声明
void initialize(void);  // 初始化两个表
int distribute(int process_name, float need_length);  // 分配内存
int recycle(int process_name);  // 回收内存
void show();  // 显示内存分配情况

// 初始化两个表
void initialize(void) {
    // 初始化已分配表
    int a;
    for (a = 0; a < N; a++) {
        used_table[a].flag = 0;  // 已分配区表项初始化为空
    }

    // 初始化空闲区表
    free_table[0].address = 1000;  // 初始空闲区起始地址
    free_table[0].length = 1024;   // 初始空闲区长度
    free_table[0].flag = 1;        // 标记为未分配
}

// 最优分配算法：动态分区分配
int distribute(int process_name, float need_length) {
    int k = -1;  // 用于定位选择的空闲分区
    int i = 0;
    int count = 0;

    // 遍历空闲区表，寻找最佳空闲区进行分配
    while (i < M) {
        if (free_table[i].flag == 1 && need_length <= free_table[i].length) {
            count++;
            if (count == 1 || free_table[i].length < free_table[k].length) {
                k = i;
            }
        }
        i++;
    }

    // 如果找到合适的空闲区
    if (k != -1) {
        // 判断是否完全分配
        if (free_table[k].length - need_length <= minsize) {
            // 完全分配
            used_table[count1].address = free_table[k].address;
            used_table[count1].length = need_length;
            used_table[count1].flag = process_name;
            free_table[k].length -= need_length;
            free_table[k].address += need_length;
            count1++;
        } else {
            // 切割空闲区进行分配
            float ads = free_table[k].address;
            float len = need_length;
            free_table[k].address += need_length;
            free_table[k].length -= need_length;

            // 将分配的内存登记到已分配区表
            int i = 0;
            while (used_table[i].flag != 0 && i < N) {
                i++;
            }
            if (i < N) {
                used_table[i].address = ads;
                used_table[i].length = len;
                used_table[i].flag = process_name;
                count1++;
            } else {
                printf("已分配区表已满，分配失败！\n");
                return 0;
            }
        }
        return process_name;
    } else {
        printf("内存分配区已满，分配失败！\n");
        return 0;
    }
}

// 回收内存
int recycle(int process_name) {
    int y = 0;
    float recycle_address, recycle_length;

    // 查找要回收的作业
    while (y < N && used_table[y].flag != process_name) {
        y++;
    }

    if (y < N) {
        recycle_address = used_table[y].address;
        recycle_length = used_table[y].length;
        used_table[y].flag = 0;
        count2++;
    } else {
        printf("该作业不存在！\n");
        return 0;
    }

    // 合并空闲区
    int i = 0, j = -1, k = -1;
    while (i < M && (k == -1 || j == -1)) {
        if (free_table[i].flag == 1) {
            if ((free_table[i].address + free_table[i].length) == recycle_address) {
                k = i;  // 上邻接
            }
            if ((recycle_address + recycle_length) == free_table[i].address) {
                j = i;  // 下邻接
            }
        }
        i++;
    }

    // 合并逻辑
    if (k != -1) {
        // 有上邻接
        if (j != -1) {  // 上下邻接都有
            free_table[k].length += free_table[j].length + recycle_length;
            free_table[j].flag = 0;
        } else {
            free_table[k].length += recycle_length;  // 只有上邻接
        }
    } else if (j != -1) {
        // 只有下邻接
        free_table[j].length += recycle_length;
        free_table[j].address = recycle_address;
    } else {
        // 上下都没有邻接
        int x = 0;
        while (free_table[x].flag != 0) {
            x++;
        }
        if (x < M) {
            free_table[x].address = recycle_address;
            free_table[x].length = recycle_length;
            free_table[x].flag = 1;
        } else {
            printf("空闲区已满，回收失败！\n");
            used_table[y].flag = process_name;
            return 0;
        }
    }

    return process_name;
}

// 显示内存分配情况
void show() {
    int i;
    printf("+++++++++++++++++++++++++++++++++++++++\n");
    printf("+++++++ 空闲区 +++++++\n");
    for (i = 0; i < M; i++) {
        if (free_table[i].flag != 0) {
            printf("初始地址： %.2f 长度： %.2f 状态： %d\n", free_table[i].address,
                   free_table[i].length, free_table[i].flag);
        }
    }

    printf("+++++++++++++++++++++++++++++++++++++++\n");
    printf("+++++++ 已分配区 +++++++\n");
    for (i = 0; i < N; i++) {
        if (used_table[i].flag != 0) {
            printf("作业号： %d 初始地址： %.2f 长度： %.2f\n", used_table[i].flag,
                   used_table[i].address, used_table[i].length);
        }
    }
}

// 主函数
int main() {
    int choice;
    bool exitFlag = false;
    int job_name, ID;
    float need_memory;

    printf("动态分区分配方式的模拟\n");
    initialize();  // 初始化

    while (!exitFlag) {
        printf("********************************************\n");
        printf("1: 分配内存\n");
        printf("2: 回收内存\n");
        printf("3: 查看分配\n");
        printf("0: 退出\n");
        printf("********************************************\n");
        printf("请输入您的操作：");
        scanf("%d", &choice);
        switch (choice) {
            case 0:
                exitFlag = true;
                break;
            case 1:
                // 分配内存
                printf("请输入作业号和所需内存：");
                scanf("%d %f", &job_name, &need_memory);
                if (job_name != 0 && need_memory != 0) {
                    distribute(job_name, need_memory);
                } else {
                    printf("作业号和内存大小不能为零！\n");
                }
                break;
            case 2:
                // 回收内存
                printf("请输入您要释放的作业号：");
                scanf("%d", &ID);
                if (ID != 0) {
                    recycle(ID);
                } else {
                    printf("作业号不能为零！\n");
                }
                break;
            case 3:
                // 查看分配情况
                show();
                break;
            default:
                printf("无效的选择，请重新输入。\n");
        }
    }
    return 0;
}
