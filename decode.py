#!/usr/bin/env python
import os
import sys

from src.baseline import read_train_baseline, tag_file
from src.consts import Model, GRAM_PROB_DICT
from src.viterbi import viterbi
from src.parse_data import read_test_file, read_gram_file, read_lex_file


def print_word_and_tag(word_and_tag):
    return "{word}\t{tag}".format(word=word_and_tag.word, tag=word_and_tag.tag)


def write_tagged_file(tagged_file, file_name, extension=".tagged"):
    file = open(file_name + extension, "w")
    for tagged_sentance in tagged_file:
        for word_and_tag in tagged_sentance:
            file.write(print_word_and_tag(word_and_tag) + '\n')
        file.write('\n')
    file.close()


def decode(model, test_file_path, param_files_path):
    if model not in Model.ALL_MODELS:
        raise RuntimeError("model %s is not supported. only support : %s" % (model, Model.ALL_MODELS))
    parsed_test_file = read_test_file(test_file_path)

    _, file_name = os.path.split(test_file_path)
    file_name, file_extension = os.path.splitext(file_name)

    if model == Model.BASELINE:
        segment_to_tag = read_train_baseline(param_files_path[0])
        tagged_file = tag_file(parsed_test_file, segment_to_tag)
        write_tagged_file(tagged_file, file_name)
    elif model == Model.BI_GRAM:
        if len(param_files_path) != 2:
            raise RuntimeError("need to have 2 files got: %s" % param_files_path)

        _, file_extension_0 = os.path.splitext(param_files_path[0])
        _, file_extension_1 = os.path.splitext(param_files_path[1])

        if {file_extension_0, file_extension_1} != {".lex", ".gram"}:
            raise RuntimeError("wrong file extension. got: %s, %s" % (file_extension_0, file_extension_1))
        lex_path =  param_files_path[0] if file_extension_0 == ".lex" else param_files_path[1]
        gram_path =  param_files_path[0] if file_extension_0 == ".gram" else param_files_path[1]
        gram_file = read_gram_file(gram_path)
        lex_file = read_lex_file(lex_path)
        gram_prob_dict = gram_file[1][GRAM_PROB_DICT]
        tags = list({tags[0] for tags in gram_prob_dict})
        tagged_file = viterbi(parsed_test_file, gram_file, lex_file, gram_level=2)
        write_tagged_file(tagged_file, file_name)
    elif model == Model.TRI_GRAM:
        pass


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
