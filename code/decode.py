#!/usr/bin/env python
import sys

from consts import WordAndTag, Model


def decode(model, test_file_path, param_files_path):

    if model not in Model.ALL_MODELS:
        raise RuntimeError("model %s is not supported. only support : %s" % (model, Model.ALL_MODELS))


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
