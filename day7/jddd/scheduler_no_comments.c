#include <stdio.h>
#include <stdlib.h>

#define getpch(type) (type *)malloc(sizeof(type))

struct pcb {
} *ready = NULL, *p;

typedef struct pcb PCB;

void sort() {
    PCB *first, *second;
    int insert = 0;

    if (ready == NULL || (p->nice > ready->nice)) {
        p->link = ready;
        ready = p;
    } else {
        first = ready;
        second = first->link;

        while (second != NULL) {
            if (p->nice > second->nice) {
                p->link = second;
                first->link = p;
                second = NULL;
                insert = 1;
            } else {
                first = first->link;
                second = second->link;
            }
        }
        if (insert == 0) {
            first->link = p;
        }
    }
}

void input() {
    int i, num;

    printf("\n???????????: ");
    scanf("%d", &num);

    for (i = 0; i < num; i++) {
        printf("\n??? No.%d:\n", i);
        p = getpch(PCB);

        printf("?????: ");
        scanf("%s", p->name);

        printf("???????: ");
        scanf("%d", &p->nice);

        printf("????????: ");
        scanf("%d", &p->ntime);

        p->rtime = 0;
        p->state = 'W';
        p->link = NULL;

    }
}

int space() {
    int count = 0;
    PCB *pr = ready;

    while (pr != NULL) {
        count++;
        pr = pr->link;
    }

    return count;
}

void disp(PCB *pr) {
    printf("%s\t%c\t%d\t%d\t%d\n", pr->name, pr->state, pr->nice, pr->ntime, pr->rtime);
}

void check() {
    PCB *pr;

    printf("\n****??????????: %s\n", p->name);
    disp(p);

    pr = ready;
    if (pr != NULL) {
        printf("\n****?????????:\n");
    } else {
        printf("\n***?????????: ?\n");
    }

    while (pr != NULL) {
        disp(pr);
        pr = pr->link;
    }
}

void destroy() {
    printf("?? [%s] ???.\n", p->name);
    free(p);
}

void running() {
    (p->rtime)++;

    if (p->rtime == p->ntime) {
    } else {
    }
}

int main() {
    int len, step = 0;
    char ch;

    len = space();

    while ((len != 0) && (ready != NULL)) {
        step++;
        printf("\nThe execute number: %d\n", step);



        printf("\n??????...");
        getchar();
    }

    printf("\n\n??????????!\n");
    return 0;
}
