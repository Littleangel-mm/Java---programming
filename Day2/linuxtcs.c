#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <termios.h>
#include <fcntl.h>

// 定义方向
#define UP 1
#define DOWN 2
#define LEFT 3
#define RIGHT 4

// 蛇身节点结构
typedef struct Snake {
    int x;
    int y;
    struct Snake *next;
} Snake;

// 全局变量
int direction = RIGHT;       // 当前移动方向
int score = 0;               // 得分
Snake *head = NULL;          // 蛇头指针
Snake *food = NULL;          // 食物指针
int gameOver = 0;            // 游戏结束标志

// 函数声明
void clearScreen();
void setCursor(int x, int y);
void initializeGame();
void drawMap();
void drawSnake();
void moveSnake();
void createFood();
int checkCollision();
void endGame();
int kbhit();
void processInput();

// 清屏函数
void clearScreen() {
    printf("\033[2J");
    printf("\033[0;0H");
}

// 设置光标位置
void setCursor(int x, int y) {
    printf("\033[%d;%dH", y, x);
}

// 初始化游戏
void initializeGame() {
    clearScreen();
    drawMap();

    // 初始化蛇
    head = (Snake *)malloc(sizeof(Snake));
    head->x = 10;
    head->y = 10;
    head->next = NULL;

    // 创建初始蛇身
    Snake *tail = head;
    int i; // 在循环外声明
    for (i = 1; i < 5; i++) {
        Snake *node = (Snake *)malloc(sizeof(Snake));
        node->x = 10 - 2 * i;
        node->y = 10;
        node->next = NULL;
        tail->next = node;
        tail = node;
    }

    drawSnake();
    createFood();
}


// 绘制地图
void drawMap() {
    int i; // 在循环外声明
    for (i = 0; i < 30; i++) {
        setCursor(i * 2, 0);
        printf("■");
        setCursor(i * 2, 20);
        printf("■");
    }
    for (i = 1; i < 20; i++) {
        setCursor(0, i);
        printf("■");
        setCursor(58, i);
        printf("■");
    }
}

// 绘制蛇
void drawSnake() {
    Snake *current = head;
    while (current) {
        setCursor(current->x, current->y);
        printf("■");
        current = current->next;
    }
}

// 创建食物
void createFood() {
    food = (Snake *)malloc(sizeof(Snake));
    srand(time(NULL));

    // 随机生成食物坐标
    do {
        food->x = (rand() % 28 + 1) * 2; // 保证为偶数，与蛇对齐
        food->y = rand() % 19 + 1;

        // 确保食物不会生成在蛇身上
        Snake *current = head;
        int collision = 0;
        while (current) {
            if (current->x == food->x && current->y == food->y) {
                collision = 1;
                break;
            }
            current = current->next;
        }
        if (!collision) break;

    } while (1);

    setCursor(food->x, food->y);
    printf("◆");
}

// 移动蛇
void moveSnake() {
    // 创建新的蛇头
    Snake *newHead = (Snake *)malloc(sizeof(Snake));
    newHead->x = head->x;
    newHead->y = head->y;

    switch (direction) {
        case UP:
            newHead->y -= 1;
            break;
        case DOWN:
            newHead->y += 1;
            break;
        case LEFT:
            newHead->x -= 2;
            break;
        case RIGHT:
            newHead->x += 2;
            break;
    }

    // 将新的头部插入到链表头
    newHead->next = head;
    head = newHead;

    // 判断是否吃到食物
    if (head->x == food->x && head->y == food->y) {
        free(food);
        createFood();
        score += 10;
    } else {
        // 删除蛇尾
        Snake *current = head;
        while (current->next->next) {
            current = current->next;
        }
        setCursor(current->next->x, current->next->y);
        printf(" ");
        free(current->next);
        current->next = NULL;
    }

    // 绘制新的蛇头
    setCursor(head->x, head->y);
    printf("■");
}

// 检测碰撞
int checkCollision() {
    // 撞墙检测
    if (head->x <= 0 || head->x >= 58 || head->y <= 0 || head->y >= 20) {
        return 1;
    }

    // 撞到自己检测
    Snake *current = head->next;
    while (current) {
        if (head->x == current->x && head->y == current->y) {
            return 1;
        }
        current = current->next;
    }

    return 0;
}

// 游戏结束
void endGame() {
    clearScreen();
    printf("游戏结束！\n");
    printf("你的得分：%d\n", score);
    exit(0);
}

// 检查键盘输入
int kbhit() {
    struct termios oldt, newt;
    int ch;
    tcgetattr(STDIN_FILENO, &oldt);
    newt = oldt;
    newt.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);
    fcntl(STDIN_FILENO, F_SETFL, O_NONBLOCK);
    ch = getchar();
    tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
    fcntl(STDIN_FILENO, F_SETFL, 0);

    if (ch != EOF) {
        ungetc(ch, stdin);
        return 1;
    }
    return 0;
}

// 处理用户输入
void processInput() {
    if (kbhit()) {
        char ch = getchar();
        if (ch == 'w' && direction != DOWN) direction = UP;
        if (ch == 's' && direction != UP) direction = DOWN;
        if (ch == 'a' && direction != RIGHT) direction = LEFT;
        if (ch == 'd' && direction != LEFT) direction = RIGHT;
        if (ch == 'q') gameOver = 1; // 退出游戏
    }
}

// 主函数
int main() {
    initializeGame();

    while (!gameOver) {
        processInput();
        moveSnake();
        if (checkCollision()) gameOver = 1;
        usleep(200000); // 控制蛇移动速度
    }

    endGame();
    return 0;
}
