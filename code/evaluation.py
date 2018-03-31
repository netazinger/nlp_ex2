#!/usr/bin/env python

def recall(t_gold, t_test):
    """
    return recall score

    :param t_gold: gold sentence
    :type WordAndTag: set

    :param t_gold: gold sentence
    :type WordAndTag: set

    :return: recall score
    :rtype: float
    """
    return float(len(set(t_gold) & set(t_test))) / len(t_gold)


def macro_avg(t_gold_list, t_test_list):

    if len(t_gold_list) != len(t_test_list):
        raise RuntimeError("gold and test are not in the same size")

    sum_val = 0
    size = 0
    for i in range(len(t_gold_list)):
        sum_val += len(t_gold_list[i] & t_test_list[i])
        size += len(t_gold_list[i])
    return float(sum_val) / size


def precision(t_gold, t_test):
    """
    return precision score

    :param t_gold: gold sentence
    :type WordAndTag: set

    :param t_gold: gold sentence
    :type WordAndTag: set

    :return: precision score
    :rtype: float
    """
    return float(len(set(t_gold) & set(t_test))) / len(t_test)


def f_score(t_gold, t_test):
    """
    return precision score

    :param t_gold: gold sentence
    :type WordAndTag: set

    :param t_gold: gold sentence
    :type WordAndTag: set

    :return: precision score
    :rtype: float
    """
    recall_score = recall(t_gold, t_test)
    precision_score = precision(t_gold, t_test)
    return float(precision_score + recall_score) / 2 * recall_score * precision_score

