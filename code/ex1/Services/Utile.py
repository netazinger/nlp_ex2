UNK = None


class CalculationResult:
    def __init__(self, unique_words, corpus_length):
        self.unique_words = unique_words
        self.corpus_length = corpus_length


class SegmentCalculator:
    def __init__(self, sentences):
        self.sentences = sentences

    def findUnigramLanguageModel(self, isSegmentTag=False):
        unigram_frequencies = dict()
        corpus_length = 0
        typeRequest = 0 if isSegmentTag == False else 1
        for sentence in self.sentences:
            try:
                if (len(sentence) - 1 >= typeRequest):
                    word = sentence[typeRequest]
                    unigram_frequencies[word] = unigram_frequencies.get(
                        word, 0) + 1
                    if word != UNK and word != "" and word.find("#") == -1:
                        corpus_length += 1
            except IndexError:
                print 'calculation error occuer'

        return CalculationResult(len(unigram_frequencies), corpus_length)
