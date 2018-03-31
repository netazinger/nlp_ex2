#!/usr/bin/env python
import sys

from consts import WordAndTag, Model


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
