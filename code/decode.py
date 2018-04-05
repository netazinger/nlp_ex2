#!/usr/bin/env python
import sys
import os

from consts import WordAndTag, Model
from ex2.ex2 import read_train_baseline, tag_file
from parse_data import read_test_file

def print_word_and_tag(word_and_tag):
    return "{word} {tag}".format(word=word_and_tag.word, tag=word_and_tag.tag)

def write_tagged_file(tagged_file, file_name):
    file = open(file_name + ".tagged","w")
    for tagged_sentance in tagged_file:
        file.write("SEG " + " ".join(map(print_word_and_tag, tagged_sentance)) + '\n')
    file.close()


def decode(model, test_file_path, param_files_path):

    if model not in Model.ALL_MODELS:
        raise RuntimeError("model %s is not supported. only support : %s" % (model, Model.ALL_MODELS))
    parsed_test_file = read_test_file(test_file_path)

    _, file_name = os.path.split(test_file_path)

    for param_file_path in param_files_path:
        if model == Model.BASELINE:
            segment_to_tag = read_train_baseline(param_files_path[0])
            tagged_file = tag_file(parsed_test_file, segment_to_tag)
            write_tagged_file(tagged_file, file_name)


def main():
    if 4 > len(sys.argv):
        print "wrong number of args. we got %s, but we support 3 and above " % len(sys.argv)
        return

    model = sys.argv[1]
    test_file_path  = sys.argv[2]
    param_files_path = sys.argv[3:]

    print "decode script is running !!!!!"
    print 'model: ', model
    print 'test_file_path: ', test_file_path
    print 'param_files_path: ', param_files_path

    decode(model=model, test_file_path=test_file_path, param_files_path=param_files_path)

    print "decode script done !!!!!"


if __name__ == '__main__':
    main()
