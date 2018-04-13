#!/usr/bin/env python
import os
import sys

from src.baseline import write_train_baseline
from src.consts import Model
from src.viterbi import write_gram_file, write_lex_file
from src.parse_data import read_gold_and_train_file


def train(model, train_file_path, smoothing=False):

    if model not in Model.ALL_MODELS:
        raise RuntimeError("model %s is not supported. only support : %s" % (model, Model.ALL_MODELS))

    parsed_train = read_gold_and_train_file(train_file_path)
    _, file_name = os.path.split(train_file_path)

    if model == Model.BASELINE:
        write_train_baseline(parsed_train, file_name)
    elif model == Model.BI_GRAM:
        write_lex_file(parsed_train, file_name, smooth=smoothing)
        write_gram_file(parsed_train, file_name, smooth=smoothing)
        # write_gram_file(parsed_train, file_name, gram_level=2)
    elif model == Model.TRI_GRAM:
        write_gram_file(parsed_train, file_name, gram_level=3)


def main():
    if 4 != len(sys.argv):
        print "wrong number of args. we got %s, but we support 3" % len(sys.argv) - 1
        return

    model = sys.argv[1]
    train_file_path  = sys.argv[2]
    smoothing = sys.argv[3] == 'y'

    print "Train script is running !!!!!"
    print 'model: ', model
    print 'train_file_path: ', train_file_path
    print 'smoothing: ', smoothing
    train(model=model, train_file_path=train_file_path, smoothing=smoothing)

    print "Train script done !!!!!"


if __name__ == '__main__':
    main()
