from collections import defaultdict

from consts import WordAndTag

END_OF_SENTENCE = '\n'
END_OF_WORD = '\n'


def read_test_file(file_path):
    """
    :param file_path: the file path
    :type str

    :return: a parse test file
    :rtype: list of list of words
    """
    file = open(file_path, 'r')

    sentences = list()
    sentence = list()

    for l in file.readlines():
        if l == END_OF_SENTENCE:
            if sentence != END_OF_SENTENCE:
                sentences.append(sentence)
            sentence = []
        else:
            sentence.append(l.replace(END_OF_WORD, ''))
    return sentences


def read_gold_and_train_file(file_path):
    """
    :param file_path: the file path
    :type str

    :return: a parse test file
    :rtype: list of list of words
    """
    file = open(file_path, 'r')

    sentences = list()
    sentence = list()

    for l in file.readlines():
        if l == END_OF_SENTENCE:
            if sentence != END_OF_SENTENCE:
                sentences.append(sentence)
            sentence = []
        else:
            sentence_parts = l.split('\t')
            word_and_tag = WordAndTag(*map(lambda w: w.replace(END_OF_WORD, ''), sentence_parts))
            sentence.append(word_and_tag)
    return sentences


def read_lex_file(file_path):
    file = open(file_path, 'r')
    seg_to_tag_to_prob = defaultdict(dict)

    for l in file.readlines():
        line_part = l.replace("\n", "").split("\t")
        seg = line_part[0]
        for i in range(1, len(line_part), 2):
            print seg, line_part[i], i
            tag = line_part[i]
            prob = line_part[i + 1]
            seg_to_tag_to_prob[seg][tag] = prob
    return seg_to_tag_to_prob