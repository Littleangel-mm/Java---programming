#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <windows.h>

// 定义蛇的移动方向
#define U 1
#define D 2
#define L 3
#define R 4

// 定义颜色
#define COLOR_GREEN 2
#define COLOR_RED 12
#define COLOR_YELLOW 14
#define COLOR_BLUE 9

// 蛇身的一个节点
typedef struct SNAKE
{
    int x;
    int y;
    struct SNAKE *next;
} snake;

// 全局变量
int score = 0, add = 10; // 总得分与每次吃食物得分
int status, sleeptime = 200; // 每次运行的时间间隔
snake *head, *food; // 蛇头指针，食物指针
snake *q; // 遍历蛇的时候用到的指针
int endgamestatus = 0; // 游戏结束的情况，1：撞到墙；2：咬到自己；3：主动退出游戏。
int foodColor; // 食物的颜色

// 函数声明
void Pos(int x, int y);
void creatMap();
void initsnake();
int biteself();
void createfood();
void cantcrosswall();
void snakemove();
void pause();
void gamecircle();
void welcometogame();
void endgame();
void gamestart();

// 设置光标位置
void Pos(int x, int y)
{
    COORD pos;
    HANDLE hOutput;
    pos.X = x;
    pos.Y = y;
    hOutput = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleCursorPosition(hOutput, pos);
}

// 设置背景颜色和文本颜色
void SetBackgroundColor(int bg, int text)
{
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleTextAttribute(hConsole, (bg << 4) | text);
}

// 创建地图
void creatMap()
{
    int i;
    SetBackgroundColor(0, 15); // 设置背景为黑色，文字为白色
    for (i = 0; i < 56; i++) // 打印上下边框
    {
        Pos(i + 1, 0); // 上边框
        printf("■");
        Pos(i + 1, 26); // 下边框
        printf("■");
    }

    for (i = 1; i < 26; i++) // 打印左右边框
    {
        Pos(0, i); // 左边框
        printf("■");
        Pos(56, i); // 右边框
        printf("■");
    }
}

// 初始化蛇身
void initsnake()
{
    snake *tail;
    int i;
    tail = (snake *)malloc(sizeof(snake)); // 从蛇尾开始，头插法，以x,y设定开始的位置
    tail->x = 24;
    tail->y = 5;
    tail->next = NULL;
    for (i = 1; i <= 4; i++)
    {
        head = (snake *)malloc(sizeof(snake));
        head->next = tail;
        head->x = 24 + 2 * i;
        head->y = 5;
        tail = head;
    }
    while (tail != NULL) // 从头到尾，输出蛇身
    {
        Pos(tail->x, tail->y);
        SetBackgroundColor(0, 2); // 设置蛇的颜色为绿色
        printf("■");
        tail = tail->next;
    }
}

// 判断是否咬到自己
int biteself()
{
    snake *self;
    self = head->next;
    while (self != NULL)
    {
        if (self->x == head->x && self->y == head->y)
        {
            return 1;
        }
        self = self->next;
    }
    return 0;
}

// 随机生成食物并设置颜色
void createfood()
{
    snake *food_1;
    srand((unsigned)time(NULL));
    food_1 = (snake *)malloc(sizeof(snake));
    while ((food_1->x % 2) != 0) // 保证其为偶数，使得食物能与蛇头对齐
    {
        food_1->x = rand() % 52 + 2;
    }
    food_1->y = rand() % 24 + 1;

    // 随机设置食物颜色
    foodColor = rand() % 3 + 1; // 随机选择颜色（1-3）

    // 确保食物不会和蛇身重合
    q = head;
    while (q != NULL)
    {
        if (q->x == food_1->x && q->y == food_1->y)
        {
            free(food_1);
            createfood(); // 如果食物和蛇身重合，重新创建食物
            return;
        }
        q = q->next;
    }

    // 显示食物
    Pos(food_1->x, food_1->y);
    SetBackgroundColor(0, foodColor == 1 ? COLOR_GREEN : (foodColor == 2 ? COLOR_RED : COLOR_YELLOW));
    printf("■");
    food = food_1;
}

// 不能穿墙
void cantcrosswall()
{
    if (head->x == 0 || head->x == 56 || head->y == 0 || head->y == 26)
    {
        endgamestatus = 1;
        endgame();
    }
}

// 蛇前进，上U，下D，左L，右R
void snakemove()
{
    snake *nexthead;
    cantcrosswall(); // 判断是否撞墙

    nexthead = (snake *)malloc(sizeof(snake));

    // 根据当前方向计算新头部的位置
    if (status == U)
    {
        nexthead->x = head->x;
        nexthead->y = head->y - 1;
    }
    else if (status == D)
    {
        nexthead->x = head->x;
        nexthead->y = head->y + 1;
    }
    else if (status == L)
    {
        nexthead->x = head->x - 2;
        nexthead->y = head->y;
    }
    else if (status == R)
    {
        nexthead->x = head->x + 2;
        nexthead->y = head->y;
    }

    if (nexthead->x == food->x && nexthead->y == food->y) // 如果下一个有食物
    {
        nexthead->next = head;
        head = nexthead;

        // 设置蛇头为食物的颜色
        SetBackgroundColor(0, foodColor == 1 ? COLOR_GREEN : (foodColor == 2 ? COLOR_RED : COLOR_YELLOW));

        q = head;
        while (q != NULL)
        {
            Pos(q->x, q->y);
            printf("■");
            q = q->next;
        }
        score += add;
        createfood(); // 生成新食物
    }
    else // 如果没有食物
    {
        nexthead->next = head;
        head = nexthead;
        q = head;

        // 仅更新蛇身，确保尾部被清空
        while (q->next->next != NULL)
        {
            Pos(q->x, q->y);
            SetBackgroundColor(0, foodColor == 1 ? COLOR_GREEN : (foodColor == 2 ? COLOR_RED : COLOR_YELLOW));
            printf("■");
            q = q->next;
        }

        // 清空旧的蛇尾位置
        Pos(q->next->x, q->next->y);
        SetBackgroundColor(0, 0); // 设置背景为黑色，清空蛇尾
        printf(" ");

        // 释放旧的蛇尾节点
        snake *temp = q->next;
        q->next = NULL;
        free(temp);
    }

    // 检查是否咬到自己
    if (biteself() == 1)
    {
        endgamestatus = 2;
        endgame();
    }
}

// 暂停
void pause()
{
    while (1)
    {
        Sleep(300);
        if (GetAsyncKeyState(VK_SPACE))
        {
            break;
        }
    }
}

// 控制游戏
void gamecircle()
{
    SetBackgroundColor(0, 15); // 设置背景为黑色，文本为白色
    Pos(64, 15);
    printf("不能穿墙，不能咬到自己\n");
    Pos(64, 16);
    printf("用↑.↓.←.→分别控制蛇的移动.");
    Pos(64, 17);
    printf("F1 为加速，F2 为减速\n");
    Pos(64, 18);
    printf("ESC ：退出游戏.space：暂停游戏.");
    Pos(64, 20);
    printf("c语言研究中心 www.dotcpp.com");

    status = R;
    while (1)
    {
        Pos(64, 10);
        printf("得分：%d ", score);
        Pos(64, 11);
        printf("每个食物得分：%d分", add);

        if (GetAsyncKeyState(VK_UP) && status != D)
        {
            status = U;
        }
        else if (GetAsyncKeyState(VK_DOWN) && status != U)
        {
            status = D;
        }
        else if (GetAsyncKeyState(VK_LEFT) && status != R)
        {
            status = L;
        }
        else if (GetAsyncKeyState(VK_RIGHT) && status != L)
        {
            status = R;
        }
        else if (GetAsyncKeyState(VK_SPACE))
        {
            pause(); // 暂停
        }
        else if (GetAsyncKeyState(VK_ESCAPE))
        {
            endgamestatus = 3;
            break; // 退出游戏
        }
        else if (GetAsyncKeyState(VK_F1)) // 加速
        {
            if (sleeptime >= 50)
            {
                sleeptime -= 30;
                add += 2;
            }
        }
        else if (GetAsyncKeyState(VK_F2)) // 减速
        {
            if (sleeptime < 350)
            {
                sleeptime += 30;
                add -= 2;
            }
        }

        Sleep(sleeptime);
        snakemove(); // 执行蛇移动
    }
}

// 欢迎界面
void welcometogame()
{
    SetBackgroundColor(0, 15); // 设置背景为黑色，文本为白色
    printf("欢迎来到贪吃蛇游戏!\n");
    printf("按任意键开始游戏...\n");
    getchar();
}

// 游戏结束
void endgame()
{
    SetBackgroundColor(0, 15); // 设置背景为黑色，文本为白色
    Pos(30, 13);
    if (endgamestatus == 1)
        printf("你撞到墙壁了！游戏结束！");
    if (endgamestatus == 2)
        printf("你咬到自己了！游戏结束！");
    if (endgamestatus == 3)
        printf("你退出了游戏！");
    printf("\n得分：%d\n", score);
    printf("按任意键退出...");
    getchar();
}

// 游戏开始
void gamestart()
{
    system("cls");
    creatMap();
    initsnake();
    createfood();
    gamecircle();
}

// 主函数
int main()
{
    system("mode con cols=60 lines=30");
    welcometogame();
    gamestart();
    return 0;
}

