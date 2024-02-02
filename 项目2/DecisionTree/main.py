import pandas as pd
import numpy as np
import math

def cal_entropy(feature,db):
    entropy = 0
    last_column = db.columns[-1]
    same_rows = db[db[last_column] == db[last_column].iloc[0]]

    counts_0 = db[feature].value_counts()
    counts_1 = same_rows[feature].value_counts()
    sum = db.shape[0]

    for i in counts_0.index:
        if i not in counts_1.index:
            entropy -= 0
        else:
           pi = counts_1[i]/counts_0[i]
           if pi == 1:
                entropy -= 0
           else:
               entropy -= (counts_0[i] / sum) * (pi * math.log(pi, 2) + (1 - pi) * math.log((1 - pi), 2))
    return entropy

def decision_tree(db):
    tree = {}
    info = {}
    values = {}

    # 判断是否到达叶子节点
    if db[db.columns[-1]].nunique() == 1:
        return db[db.columns[-1]].iloc[0]

    # 计算每个特征的期望信息
    for x in db.columns[1:-1]:
        entro = cal_entropy(x,db)
        info[x] = entro
        values[x] = db[x].value_counts().index

    # 选出信息增益最大的特征，即期望信息最小
    key = min(info, key=lambda k: info[k])
    childtree = {}
    for x in values[key]:
        childtree[x] = decision_tree(db[db[key] == x].drop(columns=key))
    tree.setdefault(key, childtree)
    return tree

def predict(test_db,decision_tree):
    if decision_tree == None:
        print("Bad decision_tree!!")
    else:
        key,value = next(iter(decision_tree.items()))
        child = value[test_db[key]]
        if isinstance(child,dict):
            return predict(test_db,child)
        else:
            return child

class RandomForest:
    def __init__(self, num_trees=10):
        self.num_trees = num_trees
        self.trees = []

    def fit(self, db):
        for i in range(self.num_trees):
            # 随机抽样数据和特征
            sample_indices = np.random.choice(len(db), size=int(len(db)/2), replace=False)
            sampled_data = db.iloc[sample_indices]

            # 创建决策树并进行训练
            tree = decision_tree(sampled_data)
            self.trees.append(tree)

    def predict(self, X):
        # 预测时通过所有决策树进行投票
        predictions = [predict(X,tree) for tree in self.trees]
        # 对每个样本取投票结果的众数
        return [max(set(prediction), key=prediction.count) for prediction in zip(*predictions)]


if __name__ == "__main__":
    # path to the training data
    db = pd.read_excel('data.xlsx')
    # for x in db.columns[1:-1]:
    #     print(x)
    # print(cal_entropy('年龄',db))
    tree = decision_tree(db)
    # print(tree)
    # print(predict({'ID':'18','年龄':'青年','有工作':'否','有自己的房子':'否','信贷情况':'一般'},tree))
    # print(predict({'ID':'38','年龄':'中年','有工作':'是','有自己的房子':'否','信贷情况':'好'},tree))
    # print(predict({'ID':'21','年龄':'老年','有工作':'否','有自己的房子':'是','信贷情况':'一般'},tree))
    random_forest = RandomForest(num_trees=3)
    random_forest.fit(db)
    print(random_forest.trees[0])
    print(random_forest.trees[1])
    print(random_forest.trees[2])
    prediction1 = random_forest.predict({'ID':'18','年龄':'青年','有工作':'是','有自己的房子':'是','信贷情况':'一般'})
    prediction2 = random_forest.predict({'ID':'38','年龄':'中年','有工作':'是','有自己的房子':'否','信贷情况':'好'})
    prediction3 = random_forest.predict({'ID':'21','年龄':'老年','有工作':'否','有自己的房子':'是','信贷情况':'一般'})
    print(prediction1)
    print(prediction2)
    print(prediction3)