from collections import namedtuple


WordAndTag = namedtuple("WordAndTag", ["word", "tag"])



class Model():
    BASELINE = 'baseline'
    BI_GRAM = 'bi-gram'
    TRI_GRAM = 'tri-gram'

    ALL_MODELS = {BASELINE, BI_GRAM, TRI_GRAM}
