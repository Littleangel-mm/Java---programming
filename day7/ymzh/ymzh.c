#include <stdio.h>
#include <stdlib.h>

#define Max 100
#define Min 20

static int distribute_block;  // 系统分配给主存的块数
static int total_pages;       // 程序的页面总数

// OPT 算法
void opt(int *s, int *b) {
    int i, j, k, max, temp, count = 0;
    int sum[Min];
    for (j = 1; j <= total_pages; j++) {
        // 遍历所有页面，检查是否存在于内存块中
        for (i = 1; i <= distribute_block; i++) {
            if (s[j] == b[i]) break;
        }
        if (i <= distribute_block) continue;  // 页面已在内存中，无需置换

        count++;  // 需要进行页面置换
        // 寻找需要被替换的页面
        for (i = 1; i <= distribute_block; i++) {
            // 检查该页面在未来的使用情况
            for (k = j + 1; k <= total_pages; k++) {
                if (b[i] == s[k]) {
                    sum[i] = k - j;  // 找到页面在未来的位置
                    break;
                }
            }
            if (k > total_pages) sum[i] = 0;  // 页面不再被访问
        }
        // 选择最长时间后不会再使用的页面进行替换
        max = 0;
        for (i = 1; i <= distribute_block; i++) {
            if (sum[i] == 0) {
                max = i;
                break;
            }
            if (sum[i] > sum[max]) {
                max = i;
            }
        }
        b[max] = s[j];  // 替换页面
        // 输出内存块状态
        for (i = 1; i <= distribute_block; i++) {
            printf("%d\t", b[i]);
        }
        printf("\n");
    }
    printf("--------------opt 算法----------------\n");
    printf("页面置换的次数为 %d\n", count);
    printf("缺页中断率为 %.2f\n", (double)count / total_pages);
    printf("------------------------------------\n\n");
}

// FIFO 算法
void fifo(int *s, int *b) {
    int i, j, max, count = 0;
    int sum[Min] = {0};
    for (j = 1; j <= total_pages; j++) {
        // 检查页面是否已经在内存中
        for (i = 1; i <= distribute_block; i++) {
            if (s[j] == b[i]) break;
        }
        if (i <= distribute_block) continue;  // 页面已在内存中

        count++;  // 页面置换
        // 找到一个最早进入内存的页面进行替换
        max = 0;
        for (i = 1; i <= distribute_block; i++) {
            if (sum[i] == 0) {
                max = i;
                break;
            }
            if (sum[i] > sum[max]) {
                max = i;
            }
        }
        b[max] = s[j];  // 替换页面
        // 输出内存块状态
        for (i = 1; i <= distribute_block; i++) {
            printf("%d\t", b[i]);
        }
        printf("\n");
    }
    printf("--------------fifo 算法----------------\n");
    printf("页面置换的次数为 %d\n", count);
    printf("缺页中断率为 %.2f\n", (double)count / total_pages);
    printf("------------------------------------\n\n");
}

// LRU 算法
void lru(int *s, int *b) {
    int i, j, k, max, temp, count = 0;
    int sum[Min];
    for (j = 1; j <= total_pages; j++) {
        for (i = 1; i <= distribute_block; i++) {
            if (s[j] == b[i]) break;
        }
        if (i <= distribute_block) continue;  // 页面已在内存中，无需置换

        count++;  // 页面置换
        // 记录页面的使用情况
        for (i = 1; i <= distribute_block; i++) {
            sum[i] = j - i;  // 页面与当前页面的距离
        }
        // 找到最近最少使用的页面
        max = 0;
        for (i = 1; i <= distribute_block; i++) {
            if (sum[i] > sum[max]) {
                max = i;
            }
        }
        b[max] = s[j];  // 替换页面
        // 输出内存块状态
        for (i = 1; i <= distribute_block; i++) {
            printf("%d\t", b[i]);
        }
        printf("\n");
    }
    printf("--------------lru 算法----------------\n");
    printf("页面置换的次数为 %d\n", count);
    printf("缺页中断率为 %.2f\n", (double)count / total_pages);
    printf("------------------------------------\n\n");
}

int main() {
    int Sum[Max], block[Min];
    int x;
    int i;

    printf("请输入系统分配给主存的块: ");
    scanf("%d", &distribute_block);
    printf("请输入程序的页面总数: ");
    scanf("%d", &total_pages);
    printf("请输入程序的 %d 个内容所在的页面: ", total_pages);
    for (i = 1; i <= total_pages; i++) {
        scanf("%d", &Sum[i]);
    }

    printf("// 初始化块的存储页面，负数表示暂时未存储\n");
    printf("请输入块存储的 %d 个页面: ", distribute_block);
    for (i = 1; i <= distribute_block; i++) {
        scanf("%d", &block[i]);
    }

    do {
        printf("1. opt 算法  2. fifo 算法  3. lru 算法  4. 结束进程\n");
        scanf("%d", &x);
        switch (x) {
            case 1:
                opt(Sum, block);
                break;
            case 2:
                fifo(Sum, block);
                break;
            case 3:
                lru(Sum, block);
                break;
            default:
                break;
        }
    } while (x != 4);

    return 0;
}
