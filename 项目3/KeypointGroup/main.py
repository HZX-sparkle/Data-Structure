import copy
import random
import matplotlib.pyplot as plt

# 采用邻接表表示网络
class Graph:
    def __init__(self):
        self.adj_list = {}

    # 在表中加入新的边或孤立的点
    def add_edge(self, node1, node2=None):
        if node1 not in self.adj_list:
            self.adj_list[node1] = []

        if node2 is not None:
            if node2 not in self.adj_list:
                self.adj_list[node2] = []
            if node2 not in self.adj_list[node1]:
                self.adj_list[node1].append(node2)
            if node1 not in self.adj_list[node2]:
                self.adj_list[node2].append(node1)

    # 在表中删除边或点
    def del_edge(self, node1, node2=None):
        if node2 is not None:
            self.adj_list[node2].remove(node1)
            self.adj_list[node1].remove(node2)
        else:
            for node in self.adj_list[node1]:
                self.adj_list[node].remove(node1)
            self.adj_list.pop(node1, None)


    # 计算某个节点的度
    def deg(self, node):
        if node not in self.adj_list:
            raise ValueError("No such node!!")
        degree = len(self.adj_list[node])
        return degree

    # 计算该图中度的期望
    def exp_deg(self):
        sum_degree = sum(self.deg(node) for node in self.adj_list)
        sum_node = len(self.adj_list)
        if sum_node == 0:
            raise ZeroDivisionError("No node in your graph!!")
        return sum_degree/sum_node

# 按度选择策略
def deg_rank(graph:Graph, n):
    # 记录重要节点
    k = []
    g = copy.deepcopy(graph)
    if n > len(g.adj_list):
        raise ValueError("Too big n!")
    # for i in range(n):
    #     key_node = max(g.adj_list, key=lambda k: g.deg(k))
    #     k.append(key_node)
    #     g.del_edge(key_node)
    # return k
    key_node = sorted(g.adj_list, key=lambda k: g.deg(k), reverse=True)
    return key_node[0:n]

# 基于投票策略
def vote_rank(graph:Graph, n):
    # 记录重要节点
    k = []
    # 记录每个节点的投票能力和投票分数
    v = {}
    g = copy.deepcopy(graph)
    # 投票更新时的幅度f
    f = 1/g.exp_deg()
    if n > len(g.adj_list):
        raise ValueError("Too big n!")
    # 初始化v, 投票能力默认为1, 投票分数默认为deg
    for key in g.adj_list:
        v[key] = [1, g.deg(key)]

    for i in range(n):
        # 选出投票分数最多的节点加入k
        key_node = max(v, key = lambda k:v[k][1])
        k.append(key_node)
        # 投票能力更新, 选中节点的邻居节点
        v[key_node] = [0,0]
        for neighbor in g.adj_list[key_node]:
            v_new = max(v[neighbor][0]- f, 0)
            delta = v[neighbor][0]- v_new
            v[neighbor][0] = v_new
            # 重新投票
            for next_neighbor in g.adj_list[neighbor]:
                if next_neighbor != key_node:
                    v[next_neighbor][1] = max(v[next_neighbor][1]-delta, 0)
        g.del_edge(key_node)

    return k

def read_from(file_path):
    with open(file_path, 'r') as file:

        graph = Graph()
        # 读取第一行, 获取行数和列数
        first_line= file.readline().strip().replace('%%', '').split()
        num_nodes, num_edges = map(int,first_line)

        # 读取后续行, 获得边
        for line in file:
            node1, node2= map(int, line.strip().split(","))
            # node1, node2= map(int, line.strip().split())
            graph.add_edge(node1, node2)

        return graph

# 评价方法：SIR模型
def SIR_model(graph, seeds, rounds, alpha, beta=1):
    # 初始感染者设为seeds, 即传入的重要节点, 康复率默认为1
    s = set(graph.adj_list.keys()) - set(seeds)
    i = set(seeds)
    r = set()
    cnt = 0

    # 扩散过程
    for _ in range(rounds):
        cnt += 1
        for x in i.copy():
            # 感染
            for y in graph.adj_list[x]:
                if random.uniform(0,1)< alpha and y in s:
                    s.discard(y)
                    i.add(y)
            # 康复
            if random.uniform(0,1) < beta:
                i.discard(x)
                r.add(x)

        # 判断是否进入稳态
        if len(i)<= 0.01:
            # print(f"在第{cnt}轮后，进入稳态")
            break

    # 感染规模：康复者数量
    return len(r)


if __name__ == '__main__':
    # graph = Graph()
    # graph.add_edge(0, 1)
    # graph.add_edge(0, 2)
    # graph.add_edge(0, 3)
    # graph.add_edge(0, 4)
    # graph.add_edge(0, 5)
    # graph.add_edge(6, 1)
    # graph.add_edge(6, 2)
    # graph.add_edge(6, 3)
    # graph.add_edge(6, 4)
    # graph.add_edge(7, 8)
    # graph.add_edge(7, 9)
    # graph.add_edge(7, 5)
    # print(graph.adj_list)
    graph = read_from('bio-grid-plant-edge.txt')
    print(graph)

    # 感染率
    alpha0 = 0.1
    alpha = []
    # 初始种子节点数
    n0 = 10
    n = []
    # 计算times轮感染规模，取平均值
    times = 1000
    # 限定SIR中最多进行rounds次循环
    rounds = 100
    # 感染率从0.1到0.9
    for i in range(20):
        alpha.append(alpha0)
        alpha0 += 0.04
    # 初始种子节点数从10到310
    for i in range(20):
        n.append(n0)
        n0 += 15

    # 按度选择
    # k1 = deg_rank(graph, n)
    print("按度选择：")
    # print(k1)
    # 感染率变化
    a1 = []
    k1 = deg_rank(graph, 30)
    for i in alpha:
        h1 = 0
        for _ in range(times):
            h1 += SIR_model(graph, k1, rounds, i)
        h1 /= times
        a1.append(h1)
    plt.plot(alpha, a1, marker='o', linestyle='-', color='green')
    plt.xlabel('alpha')
    plt.ylabel('infected')
    plt.title('deg-alpha')
    plt.show()

    # 初始节点数变化
    b1 = []
    for i in n:
        h1 = 0
        k1 = deg_rank(graph, i)
        for _ in range(times):
            h1 += SIR_model(graph, k1, rounds, 0.4)
        h1 /= times
        b1.append(h1)
    plt.plot(n, b1, marker='o', linestyle='-', color='red')
    plt.xlabel('seeds')
    plt.ylabel('infected')
    plt.title('deg-seeds')
    plt.show()
    # print(f"平均感染规模为{h1}")

    print()

    # 按投票选择
    # k2 = vote_rank(graph, n)
    print("按投票选择:")
    # print(k2)
    # 感染率变化
    a2 = []
    k2 = vote_rank(graph, 30)
    for i in alpha:
        h2 = 0
        for _ in range(times):
            h2 += SIR_model(graph, k2, rounds, i)
        h2 /= times
        a2.append(h2)
    plt.plot(alpha, a2, marker='o', linestyle='-', color='green')
    plt.xlabel('alpha')
    plt.ylabel('infected')
    plt.title('vote-alpha')
    plt.show()
    # 初始节点数变化
    b2 = []
    for i in n:
        h2 = 0
        k2 = vote_rank(graph, i)
        for _ in range(times):
            h2 += SIR_model(graph, k2, rounds, 0.4)
        h2 /= times
        b2.append(h2)
    plt.plot(n, b2, marker='o', linestyle='-', color='red')
    plt.xlabel('seeds')
    plt.ylabel('infected')
    plt.title('deg-seeds')
    plt.show()
    # print(f"平均感染规模为{h2}")

    # 感染率对比
    # 绘制折线图
    plt.plot(alpha, a1, marker='o', linestyle='-', color='blue', label='deg')
    plt.plot(alpha, a2, marker='s', linestyle='--', color='green', label='vote')

    # 添加标签和标题
    plt.xlabel('alpha')
    plt.ylabel('infected')
    plt.title('deg vs vote:alpha')
    plt.legend()  # 添加图例

    # 显示图形
    plt.show()

    # 初始节点对比
    # 绘制折线图
    plt.plot(n, b1, marker='o', linestyle='-', color='blue', label='deg')
    plt.plot(n, b2, marker='s', linestyle='--', color='green', label='vote')

    # 添加标签和标题
    plt.xlabel('seeds')
    plt.ylabel('infected')
    plt.title('deg vs vote:seeds')
    plt.legend()  # 添加图例

    # 显示图形
    plt.show()


