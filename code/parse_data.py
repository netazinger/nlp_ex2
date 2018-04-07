from collections import defaultdict

from consts import WordAndTag, NUM_OF_GRAM, GRAM_PROB_DICT

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
            tag = line_part[i]
            prob = float(line_part[i + 1])
            seg_to_tag_to_prob[seg][tag] = prob
    return seg_to_tag_to_prob


def parse_num_of_gram_line(line):
    line_part = line.replace("\n", "").split(" = ")
    return int(line_part[0].split(" ")[1]), int(line_part[1])


def parse_gram_mark(line):
    if "-grams" in line:
        return int(line.split("-")[0][1:])
    else:
        return None


def read_gram_file(file_path):
    file = open(file_path, 'r')
    file_lines = file.readlines()

    # read n gram size
    assert "\data\\" in file_lines[0]
    gram_level_to_gram_data = defaultdict(dict)

    i = 1
    while file_lines[i] != "\n":
        gram_level, num_of_gram = parse_num_of_gram_line(file_lines[i])
        gram_level_to_gram_data[gram_level][NUM_OF_GRAM] = num_of_gram
        i += 1
    i += 1
    while i < len(file_lines):
        line = file_lines[i]
        if parse_gram_mark(line):
            gram_level = parse_gram_mark(line)
            gram_prob_dict = dict()
        elif line == '\n':
            gram_level_to_gram_data[gram_level][GRAM_PROB_DICT] = gram_prob_dict
        else:
            line_parts = line.replace("\n", "").split('\t')
            gram_prob_dict[tuple(line_parts[1:])] = float(line_parts[0])
        i += 1
    return gram_level_to_gram_data
