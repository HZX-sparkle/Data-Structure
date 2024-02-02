# frequent pattern mining by Apriori

# whether this set is a frequent pattern， meanwhile, calculate the sup of this set
def is_frequent(db: dict, itemset: tuple, min_sup: int):
    count = 0
    for y in db.values():
        if set(y) & set(itemset) == set(itemset):
            count += 1
    if count >= min_sup:
        return True, count
    else:
        return False, count


# generate (k+1)-lists from k-lists
def apriori_gen(k_lists: tuple):
    new_lists = []
    k = len(k_lists[0])
    for i in range(len(k_lists) - 1):
        list1 = k_lists[i]
        for j in k_lists[i + 1:]:
            list2 = j
            # if these two lists have k-1 same items, they're linkable
            common_elements = set(list1) & set(list2)
            if len(common_elements) == k - 1:
                new_list = tuple(set(list1) | set(list2))
                has_same = False
                for x in new_lists:
                    if set(new_list) == set(x):
                        has_same = True
                        break
                if has_same == False:
                    new_lists.append(new_list)
    # print(new_lists)
    return new_lists


# main steps of apriori
def apriori(db: dict, min_sup: int):

    # get the original data
    TDB = dict.values(db)

    for x in TDB:
        if not isinstance(x,list):
            print("Wrong value type!")
            exit(1)

    # make a dict "fp" to store all the frequent patterns and their sup
    # at first, it's empty
    fp = {}

    # generate the first lists
    print("Round 1")
    list1 = []
    for x in TDB:
        list1 = list(set(list1) | set(x))
    for i in range(len(list1)):
        tuple0 = (list1[i],)
        list1[i] = tuple0

    # cut the list that is not frequent and update the dict
    dict1 = {}
    list2 = list1.copy()
    for x in list1:
        judge, sup = is_frequent(db, x, min_sup)
        if judge == False:
            list2.remove(x)
        else:
            print("({})".format(' '.join(x)), end=' ')
            dict1.setdefault(x, sup)
    list1 = list2

    # check if there is any frequent patterns, or we steps out
    if dict1 != {}:
        fp.update(dict1)
        print()
    else:
        print("there is no frequent patterns at all!")
        return fp, 0

    # if we indeed have 1-frequent patterns, we continue
    k = 2
    while (True):
        print("Round", k)
        list1 = apriori_gen(tuple(list1))
        k_dict = {}
        list2 = list1.copy()
        for x in list1:
            judge, sup = is_frequent(db, x, min_sup)
            if judge == False:
                list2.remove(x)
            else:
                print("({})".format(' '.join(x)), end=' ')
                k_dict.setdefault(x, sup)
        list1 = list2
        if k_dict != {}:
            fp.update(k_dict)
            k += 1
            print()
        else:
            print("nothing")
            break

    return fp, k - 1


# get the mfi in frequent patterns
def mfi(itemsets: dict, degree: int):
    mfi = {}

    # slice the itemsets by its degree
    itemsets_slice = {}
    for i in range(degree, 0, -1):
        list_i = []
        for x in itemsets.keys():
            if len(x) == i:
                list_i.append(x)
        dict_i = {i: tuple(list_i)}
        itemsets_slice.update(dict_i)

    # select the mfi in itemsets
    for k, v in itemsets_slice.items():
        if k == degree:
            dict0 = {v: itemsets[x] for x in v}
            mfi.update(dict0)
        else:
            for i in v:
                for j in itemsets_slice[k + 1]:
                    is_mfi = True
                    if set(i).issubset(j):
                        is_mfi = False
                        break
                if is_mfi:
                    mfi.update({i: itemsets[i]})

    return mfi


def myprint(order_result, k):
    if len(order_result)<k:
        print("The length is not enough!")
        return
    i = 0
    for x in order_result:
        if i < k:
            print("{}:{}".format(x[0], x[1]))
            i += 1
        else:
            break


if __name__ == "__main__":
    # what you need to do is :
    # 输入事务集，给定支持度
    # 输出所有的频繁模式，并按支持度降序排列
    # 输出极大频繁模式，并按支持度排序
    # 输出支持度最大的前k个频繁模式
    db = {
        "T1": ["l1", "l2", "l3"],
        "T2": ["l2", "l3", "l4"],
        "T3": ["l4", "l5"],
        "T4": ["l1", "l2", "l4"],
        "T5": ["l1", "l2", "l3", "l5"],
        "T6": ["l1", "l2", "l3", "l4"]
    }

    min_sup = 2

    if db=={}:
        print("Empty!")
        exit(1)

    result, degree = apriori(db, min_sup)

    # sort the frequent patterns by its sup
    order_result = sorted(result.items(), key=lambda x: x[1], reverse=True)
    print()
    print("Ordered frequent patterns:")
    for x in order_result:
        print("{}:{}".format(x[0], x[1]))

    # get the MFI and sort
    mfi = mfi(result, degree)
    order_mfi = sorted(mfi.items(), key=lambda x: x[1])
    print()
    print("Ordered MFI:")
    for x in order_mfi:
        print("{}:{}".format(x[0], x[1]))

    # print the first k frequent patterns that has the highest sup
    print()
    k = 3
    print("First {} highest frequent patterns:".format(k))
    myprint(order_result, k)

else:
    pass
