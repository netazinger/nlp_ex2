from consts import  WordAndTag

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
    # import ipdb; ipdb.set_trace() # NO_COMMIT
    for l in file.readlines():
        if l == END_OF_SENTENCE:
            if sentence != END_OF_SENTENCE:
                sentences.append(sentence)
            sentence = []
        else:
            sentence.append(l.replace(END_OF_WORD, ''))
    return sentences



def read_gold_file(file_path):
    """
    :param file_path: the file path
    :type str

    :return: a parse test file
    :rtype: list of list of words
    """
    file = open(file_path, 'r')

    sentences = list()
    sentence = list()
    # import ipdb; ipdb.set_trace() # NO_COMMIT
    for l in file.readlines():
        if l == END_OF_SENTENCE:
            if sentence != END_OF_SENTENCE:
                import ipdb; ipdb.set_trace() # NO_COMMIT
                sentences.append(sentence)
            sentence = []
        else:
            sentence_parts = l.split('\t')
            word_and_tag = WordAndTag(*map(lambda w: w.replace(END_OF_WORD, ''), sentence_parts))
            sentence.append(word_and_tag)
    return sentences