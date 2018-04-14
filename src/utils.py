import sys
import os
from collections import Counter, defaultdict

from parse_data import read_gold_and_train_file
from decode import write_tagged_file


def calc_confusion_matrix(tagged_tested, gold):
    confusion_matrix_dict = defaultdict(lambda:defaultdict(int))
    flat_gold = [word_and_tag for sentance in gold for word_and_tag in sentance]
    flat_tagged_tested = [word_and_tag for sentance in tagged_tested for word_and_tag in sentance]

    assert len(flat_gold) == len(flat_tagged_tested)
    for i in range(len(flat_gold)):
        confusion_matrix_dict[flat_gold[i].tag][flat_tagged_tested[i].tag] += 1
    return confusion_matrix_dict


def find_max_confusion_matrix(confusion_matrix_dict, num_of_max=3):
    sorted_tags = sorted(confusion_matrix_dict.keys())
    flatten_metrix = []
    for tag_1 in sorted_tags:
        for tag_2 in sorted_tags:
            if tag_1 != tag_2:
                flatten_metrix.append((tag_1, tag_2, confusion_matrix_dict[tag_1][tag_2]))
    return sorted(flatten_metrix, key=lambda x: -x[2])[:num_of_max]


def save_confusion_matrix(confusion_matrix_dict, file_name):
    sorted_tags = sorted(confusion_matrix_dict.keys())
    file = open(file_name + ".confusion_matrix.csv", "w")
    file.write("," + ",".join(sorted_tags) + '\n')
    for row_tag in sorted_tags:
        file.write(row_tag)
        for cal_tag in sorted_tags:
            file.write(",%s" % confusion_matrix_dict[row_tag][cal_tag] )
        file.write("\n")

    file.close()


def chunks(seq, num_of_sublist):
    seq_len = len(seq)
    if seq_len < num_of_sublist:
        yield seq
    else:
        split_size = 1.0 / num_of_sublist * seq_len
        for i in range(num_of_sublist):
            yield seq[int(round(i * split_size)):int(round((i + 1) * split_size))]


def split_train_file(train_file, chunk_size=10):
    parsed_train_file = read_gold_and_train_file(train_file)
    train_chuncks = list(chunks(parsed_train_file, chunk_size))
    if not os.path.isdir("train"):
        os.mkdir("train")
    for i in range(len(train_chuncks)):
        train_to_write = []
        for chunk in train_chuncks[:(i + 1)]:
            train_to_write += chunk
        write_tagged_file(train_to_write, "train/train_%s" % (i + 1), ".train")





