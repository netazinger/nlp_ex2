#!/usr/bin/env python
import sys

from consts import WordAndTag, Model
import math

def calc_word_accuracy_for_sentence(sentence, sentence_gold):
    if len(sentence) != len(sentence_gold):
        raise RuntimeError("sentences are not in same length")
    num_of_true_tagging = 0
    for i in range(sentence):
        num_of_true_tagging += 1 if sentence[i] == sentence_gold[i] else 0
    return num_of_true_tagging / len(sentence)


def calc_sentence_accuracy_for_sentence(sentence, sentence_gold):
    return int(math.floor(calc_word_accuracy_for_sentence(sentence, sentence_gold)))


def cal_word_accuracy_for_corpus(test, gold):
    if len(test) != len(gold):
        raise RuntimeError("not in same length")

    res = 0
    for i in range(test):
        res += calc_word_accuracy_for_sentence(test[i], gold[i]) * len(test[i])
    return res / sum(map(len, test))

def calc_sentence_accuracy_for_corpus(test, gold):
    if len(test) != len(gold):
        raise RuntimeError("not in same length")
    return sum([calc_sentence_accuracy_for_sentence(test[i], gold[i]) for i in range(test)]) / len(test)


def evaluate(tagged_file_path, model, gold_file_path, smoothing=False):

    if model not in Model.ALL_MODELS:
        raise RuntimeError("model %s is not supported. only support : %s" % (model, Model.ALL_MODELS))


def main():
    if 5 != len(sys.argv):
        print "wrong number of args. we got %s, but we support 4" % len(sys.argv)
        return

    tagged_file_path = sys.argv[1]
    gold_file_path  = sys.argv[2]
    model = sys.argv[3]
    smoothing = sys.argv[4] == 'y'

    print "Evaluate script is running !!!!!"
    print 'model: ', model
    print 'train_file_path: ', gold_file_path
    print 'smoothing: ', smoothing
    evaluate(tagged_file_path=tagged_file_path, model=model, gold_file_path=gold_file_path, smoothing=smoothing)

    print "Evaluate script done !!!!!"


if __name__ == '__main__':
    main()
