END_OF_SENTENS = '\n'
END_OF_WORD = '\n'

def read_test_file(file_path):
    """
    :param file_path: the file path
    :type str

    :return: a parse test file
    :rtype: list of list of words
    """
    file = open(file_path, 'r')

    sentenses = list()
    sentens = list()
    # import ipdb; ipdb.set_trace() # NO_COMMIT
    for l in file.readlines():
        if l == END_OF_SENTENS:
            if sentens != END_OF_SENTENS:
                sentenses.append(sentens)
            sentens = []
        else:
            sentens.append(l)
    return sentenses