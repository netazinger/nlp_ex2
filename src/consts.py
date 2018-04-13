from collections import namedtuple
import math


WordAndTag = namedtuple("WordAndTag", ["word", "tag"])

def print_word_and_tag(word_and_tag):
    return "{word} {tag}".format(word_and_tag.word, word_and_tag.tag)


def prob_post_processing(prob, do_log=True):
    if do_log:
        return math.log(prob) if prob else None
    return prob

class Model():
    BASELINE = 'baseline'
    BI_GRAM = 'bi-gram'
    TRI_GRAM = 'tri-gram'

    ALL_MODELS = {BASELINE, BI_GRAM, TRI_GRAM}

LOG_PROB_OF_ZERO = -1000
UNKNOWN_TAG = "NNP"
UNKNOWN_SEG = "UNKNOWN_SEG"

NUM_OF_GRAM = 'num_of_gram'
GRAM_PROB_DICT = 'gram_prob_dict'

EOS = "EOS"
BOS = "BOS"
