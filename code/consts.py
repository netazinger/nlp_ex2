from collections import namedtuple


WordAndTag = namedtuple("WordAndTag", ["word", "tag"])

def print_word_and_tag(word_and_tag):
    return "{word} {tag}".format(word_and_tag.word, word_and_tag.tag)


class Model():
    BASELINE = 'baseline'
    BI_GRAM = 'bi-gram'
    TRI_GRAM = 'tri-gram'

    ALL_MODELS = {BASELINE, BI_GRAM, TRI_GRAM}

UNKNOWN_TAG = "NNP"
UNKNOWN_SEG = "UNKNOWN_SEG"


EOS = "EOS"
BOS = "BOS"