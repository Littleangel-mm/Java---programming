# 编译器及其选项
CC = gcc
CFLAGS = -Wall -g

# 目标文件和最终程序
OBJS = myapp.o greeting.o
TARGET = myapp

# 目标规则
all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(OBJS)

myapp.o: myapp.c greeting.h
	$(CC) $(CFLAGS) -c myapp.c

greeting.o: greeting.c greeting.h
	$(CC) $(CFLAGS) -c greeting.c

clean:
	rm -f $(OBJS) $(TARGET)
