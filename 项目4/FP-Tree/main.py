from itertools import permutations, combinations
import pandas as pd


# 树的节点定义
class Node:
    def __init__(self, name):
        self.name = name
        self.value = 1
        self.parent = None
        self.child = []

# 频繁模式输出形式
class FSet:
    def __init__(self):
        # 频繁项集
        self.frequent_patterns = set()
        # 支持度
        self.sup = None

# 关联规则输出形式
class ARule:
    def __init__(self):
        # 关联规则
        self.rule = ""
        # 置信度
        self.con = None

class FP_Tree:
    def __init__(self):
        # 项头表和FP-tree
        self.head_table = {}
        self.tree = Node('root')

    # 项头表的建立
    def build_table(self, db:list, min_sup):
        # 第一次扫描，得到频繁1-项集的计数
        for i in db:
            for j in i:
                if j not in self.head_table:
                    self.head_table[j] = [1, []]
                else:
                    self.head_table[j][0] += 1

        # 删去非频繁项, 并以支持度降序排列
        for i in self.head_table:
            if self.head_table[i][0] < min_sup:
                self.head_table.pop(i)
        sorted_head_table = dict(sorted(self.head_table.items(), key=lambda item: item[1][0], reverse= True))
        self.head_table = sorted_head_table

        # 第二次扫描，调整数据集
        for i in range(len(db)):
            for x in db[i].copy():
                if x not in self.head_table:
                    db[i].remove(x)
            db[i] = sorted(db[i], key= lambda x: self.head_table[x][0],reverse=True)
        modified_db = list(filter(None,db))
        db = modified_db

        # 返回项头表和调整后的数据集
        return self.head_table, db

    # FP-tree的建立
    def build_tree(self, db:list):
        for i in db:
            self.update_tree(i, self.tree)

    # 往树中加入新数据
    def update_tree(self, nodes, root):
        if nodes == []:
            return
        else:
            is_child = 0
            for child in root.child:
                if nodes[0] == child.name:
                    child.value += 1
                    is_child = 1
                    self.update_tree(nodes[1:], child)
                    return
            # 如果不是孩子
            if is_child == 0:
                new_child = Node(nodes[0])
                # 创建新节点，加入到tree中，同时更新项头表
                self.head_table[nodes[0]][1].append(new_child)
                new_child.parent = root
                root.child.append(new_child)
                self.update_tree(nodes[1:], new_child)
            return

    # 完成整个FP-tree算法的构造
    def build(self, db:list, min_sup):
        self.build_table(db, min_sup)
        self.build_tree(db)

    # 从生成好的FP-tree中挖掘频繁项集
    def find(self, min_sup):
        # 从项头表底部开始挖掘
        all_frequent_patterns = []
        for key in reversed(self.head_table.keys()):
            print(f"从{key}挖掘频繁项集：")
            # 先加入1-项频繁模式
            fset_1 = FSet()
            fset_1.frequent_patterns = {key}
            fset_1.sup = self.head_table[key][0]
            all_frequent_patterns.append(fset_1)

            # 生成条件模式基
            sub_tree = self.sub_tree(key)
            # 删除小于最小支持度的节点
            modified_tree = {key: value for key, value in sub_tree.items() if value >= min_sup}
            # 选出所有非空子集
            all_subsets = self.subsets_of(modified_tree)
            # 转换成FSet的形式，并加入key
            for i in all_subsets:
                fset = FSet()
                fset.frequent_patterns = {key} | {key for key,value in i}
                fset.sup = min(value for key, value in i)
                all_frequent_patterns.append(fset)
                print(f"{fset.frequent_patterns} : {fset.sup}")
        return all_frequent_patterns

    def subsets_of(self, modified_tree):
        all_subsets = [[]]
        for i in list(modified_tree.items()):
            new_subsets = [subsets + [i] for subsets in all_subsets]
            all_subsets.extend(new_subsets)
        all_subsets.remove([])
        return all_subsets

    # 生成条件模式树
    def sub_tree(self, key):
        sub_tree = {}
        # 记录路径
        path = []
        for i in self.head_table[key][1]:
            path_i = {}
            current = i
            while current.parent is not None:
                path_i[current] = i.value
                current = current.parent
            path.append(path_i)

        # 合并路径
        for i in path:
            for j in i:
                if j.name not in sub_tree:
                    sub_tree[j.name] = i[j]
                else:
                    sub_tree[j.name] += i[j]

        sub_tree.pop(key)

        return sub_tree

    # 关联规则挖掘
    def rule_gen(self, fp, min_con):
        rules = []
        # 随机组合2个频繁模式
        for fset1,fset2 in combinations(fp,2):
            # 不相交
            if fset1.frequent_patterns.isdisjoint(fset2.frequent_patterns):
                # 两者并集也是频繁模式
                for fset3 in fp:
                    if fset3.frequent_patterns == fset2.frequent_patterns|fset1.frequent_patterns:
                        # 产生关联规则并计算置信度
                        rule_1 = ARule()
                        rule_1.rule = f"{fset1.frequent_patterns} => {fset2.frequent_patterns}"
                        rule_1.con = fset3.sup / fset1.sup
                        if rule_1.con >= min_con:
                            rules.append(rule_1)

                        rule_2 = ARule()
                        rule_2.rule = f"{fset2.frequent_patterns} => {fset1.frequent_patterns}"
                        rule_2.con = fset3.sup / fset2.sup
                        if rule_2.con >= min_con:
                            rules.append(rule_2)

        return rules

if __name__ == '__main__':
    # db = [
    #     ['F','A','C','E','B'],
    #     ['A','C','G'],
    #     ['E'],
    #     ['E'],
    #     ['A','C','E','G','D'],
    #     ['A','C','E','G'],
    #     ['A','C','E','B','F'],
    #     ['A','C','D'],
    #     ['A','C','E','G'],
    #     ['A', 'C', 'E', 'G'],
    # ]
    #
    # tree = FP_Tree()
    # tree.build(db,2)
    # fsets = tree.find(2)
    # rules = tree.rule_gen(fsets,0.7)
    # for rule in rules:
    #     print(f"{rule.rule}: {rule.con}")
    db = []
    file = pd.read_excel('test.xlsx')
    for itemset in file["Itemset"]:
        # print(itemset)
        db.append(list(itemset.strip('{}').replace(' ', '').split(',')))
    tree = FP_Tree()
    tree.build(db,2)
    fsets = tree.find(2)
    rules = tree.rule_gen(fsets,0.7)
    # 导入结果到output中
    with open('output.txt', 'w') as file:
        file.write("频繁模式：\n")
        for fset in fsets:
            file.write(f"{fset.frequent_patterns} : {fset.sup} \n")
        file.write("关联规则：\n")
        for rule in rules:
            file.write(f"{rule.rule} : {rule.con} \n")

