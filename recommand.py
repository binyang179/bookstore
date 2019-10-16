# -*- coding:utf-8 -*-
"""
个性化推荐方案
"""


def build_martix(user_orders):
    """
    根据用户购买的订单信息，构建推荐矩阵
    :param user_orders: 用户购买矩阵
    :return:
    """
    item_count = dict()
    item_item_count = dict()
    for user_items in user_orders.values():
        for item in user_items:
            # 统计每个商品出现的个数
            if item_count.get(item):
                item_count[item] = 1 + item_count[item]
            else:
                item_count[item] = 1
            # 统计每个商品与其他商品的数量关系
            if not item_item_count.get(item):
                item_item_count[item] = dict()
            for sub_item in user_items:
                if item == sub_item:
                    continue
                if item_item_count[item].get(sub_item):
                    item_item_count[item][sub_item] += 1
                else:
                    item_item_count[item][sub_item] = 1
    # 重新计算每个元素之间的关系
    for key in item_item_count.keys():
        key_count = item_count[key]
        for sub_item in item_item_count[key].keys():
            sub_key_count = item_count[sub_item]
            item_item_count[key][sub_item] = item_item_count[key][sub_item] / (key_count + sub_key_count)
    return item_item_count


def recommend(user_items, recommend_matrix, n=10):
    """
    根据用户的购买历史，进行用户推荐
    :param user_items:
    :param n:
    :return:
    """
    rank = []
    for item in user_items:
        for key, _ in sorted(recommend_matrix[item].items(), key=lambda x: x[1], reverse=True)[0:n]:
            if key in user_items or key in rank:
                continue
            rank.append(key)
    return rank
