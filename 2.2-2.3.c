/*
	1.给定一个由100个存储单元组成的初始为空的存储区域，利用这个存储区域顺序存储队列，一整数序列作为输入元素，
	整数n>0表示把元素n添加到队列中；n=-1表示从队列中删去一个元素；n=0表示输入结束。是编写一个算法，实现上述操作，
	要求把队列处理成环形结构，并在发现异常情况时，立即打印错误信息。
*/
#define MAXSIZE 100

int main()
{
	int front = -1;
	int rear = -1;
	int *sq = (int*)malloc(MAXSIZE * sizeof(int));
	while (1)
	{
		int n = 0;
		scanf("%d", &n);
		if (n == 0) break; //输入结束
		else if (n > 0) //添加元素
		{
			//判断是否队满
			if ((rear + 1) % MAXSIZE == front) printf("overflow!\n");
			else
			{
				rear = (rear + 1) % MAXSIZE;
				sq[rear] = n;
			}
		}
		else if (n == -1) //删除元素
		{
			//判断是否队空
			if (front == rear) printf("underflow!\n");
			else
			{
				front = (front + 1) % MAXSIZE;
			}
		}
	}
}

/*
	2. 假设一算术表达式中含有圆括号，方括号和花括号三种类型的符号，试写一个判别表达式中括号是否配对的算法，表达式以#表示结束。
*/

bool isPaired(const char* expression) {
	struct Stack stack;
	initStack(&stack);

	for (int i = 0; expression[i] != '#'; i++) {
		char symbol = expression[i];
		if (symbol == '(' || symbol == '[' || symbol == '{') {
			push(&stack, symbol);
		} else if (symbol == ')' || symbol == ']' || symbol == '}') {
			if (isEmpty(&stack)) {
				return false; // 右括号多于左括号，不配对
			}
			char topSymbol = pop(&stack);
			if ((symbol == ')' && topSymbol != '(') ||
			        (symbol == ']' && topSymbol != '[') ||
			        (symbol == '}' && topSymbol != '{')) {
				return false; // 括号类型不匹配，不配对
			}
		}
	}

	return isEmpty(&stack); // 如果栈为空，说明所有括号都配对
}
