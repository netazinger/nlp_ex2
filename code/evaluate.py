#!/usr/bin/env python
import sys
import os

from consts import WordAndTag, Model
import math

from parse_data import read_gold_and_train_file
EVAL_LINE_FORMAT = "{sent_num} {seg_accuracy} {sent_accuracy}\n"
EVAL_MACO_AVG_FORMAT = "macro-avg {seg_accuracy_all} {sent_accuracy_all}"


def calc_word_accuracy_for_sentence(sentence, sentence_gold):
    if len(sentence) != len(sentence_gold):
        raise RuntimeError("sentences are not in same length")
    num_of_true_tagging = 0
    for i in range(len(sentence)):
        num_of_true_tagging += 1 if sentence[i] == sentence_gold[i] else 0
    return float(num_of_true_tagging) / len(sentence)


def calc_sentence_accuracy_for_sentence(sentence, sentence_gold):
    return int(math.floor(calc_word_accuracy_for_sentence(sentence, sentence_gold)))


def calc_word_accuracy_for_corpus(test, gold):
    if len(test) != len(gold):
        raise RuntimeError("not in same length")

    res = 0
    for i in range(len(test)):
        res += calc_word_accuracy_for_sentence(test[i], gold[i]) * len(test[i])
    return float(res) / sum(map(len, test))


def calc_sentence_accuracy_for_corpus(test, gold):
    if len(test) != len(gold):
        raise RuntimeError("not in same length")
    return sum([calc_sentence_accuracy_for_sentence(test[i], gold[i]) for i in range(len(test))]) / float(len(test))


def evaluate(tagged_file_path, model, gold_file_path, smoothing=False):

    if model not in Model.ALL_MODELS:
        raise RuntimeError("model %s is not supported. only support : %s" % (model, Model.ALL_MODELS))

    parsed_tagged_file = read_gold_and_train_file(tagged_file_path)
    parsed_gold_file = read_gold_and_train_file(gold_file_path)

    if len(parsed_tagged_file) != len(parsed_gold_file):
        raise RuntimeError("not in same length")

    _, file_name = os.path.split(tagged_file_path)
    file_name, file_extension = os.path.splitext(file_name)

    file = open(file_name + ".eval", "w")
    for i in range(len(parsed_tagged_file)):
        seg_accuracy = calc_word_accuracy_for_sentence(parsed_tagged_file[i], parsed_gold_file[i])
        sent_accuracy = calc_sentence_accuracy_for_sentence(parsed_tagged_file[i], parsed_gold_file[i])
        file.write(EVAL_LINE_FORMAT.format(sent_num=i + 1, seg_accuracy=seg_accuracy, sent_accuracy=sent_accuracy))

    seg_accuracy_all = calc_word_accuracy_for_corpus(parsed_tagged_file, parsed_gold_file)
    sent_accuracy_all = calc_sentence_accuracy_for_corpus(parsed_tagged_file, parsed_gold_file)
    file.write(EVAL_MACO_AVG_FORMAT.format(seg_accuracy_all=seg_accuracy_all, sent_accuracy_all=sent_accuracy_all))
    file.close()


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
