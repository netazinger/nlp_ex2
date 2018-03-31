#!/usr/bin/env python
import sys

from consts import WordAndTag, Model


def train(model, train_file_path, smoothing=False):

    if model not in Model.ALL_MODELS:
        raise RuntimeError("model %s is not supported. only support : %s" % (model, Model.ALL_MODELS))


def main():
    if 4 != len(sys.argv):
        print "wrong number of args. we got %s, but we support 3" % len(sys.argv)
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
