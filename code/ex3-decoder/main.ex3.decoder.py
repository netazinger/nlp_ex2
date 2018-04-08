import sys
import os
import traceback
sys.path.append(os.path.abspath(os.path.join(__file__, "../..")))
from collections import defaultdict, deque
from consts import EOS, BOS
from parse_data import read_lex_file, read_gram_file

START_SYMBOL = BOS
STOP_SYMBOL = EOS
LOG_PROB_OF_ZERO = -1000


def getAllTags(gramFile, lexFile):
    uniqeTags = set()
    findUniqueTagsFromGram(gramFile, uniqeTags)
    findUniqueTagsFromLex(lexFile, uniqeTags)
    return uniqeTags


def findUniqueTagsFromGram(gramFile, uniqeTags):
    for sentence in gramFile[2]['gram_prob_dict']:
        uniqeTags.add(sentence[0])
        uniqeTags.add(sentence[1])
    return uniqeTags


def findUniqueTagsFromLex(lexFile, uniqeTags):
    for word in lexFile:
        uniqeTags.add(lexFile[word].keys()[0])
    return uniqeTags


class Viterbi:
    def __init__(self, taglist):
        self.taglist = taglist

    def S(self, k):
        if k in (-1, 0):
            return {START_SYMBOL}
        else:
            return self.taglist

    def algoritem(self, input_sentences, q_values, e_values):
        tagged = []
        pi = defaultdict(float)
        bp = {}
        defultSet = dict()

        # Initialization
        pi[(0, START_SYMBOL, START_SYMBOL)] = 0.0
        for line in input_sentences:
            sent_words = line.split()
            n = len(sent_words)
            try:
                # u is the current item , v is all the passable tag before me
                for k in range(0, n + 1):
                    for u in self.S(k - 1):
                        max_score = float('-Inf')
                        max_tag = None
                        # word|Tag prob
                        for v in self.S(k):
                            if(k==2  and u =='VB' and v =='yyQUOT'):
                                m=4
                            wordProb = (e_values.get(sent_words[k - 1],
                                                     defultSet)).get(u)
                            if wordProb != 0 and wordProb != None:
                                # if e_values.get((sent_words[k-1], v), 0) != 0:
                                # π(k,u,v)=maxw∈Sk−2(π(k−1,v)⋅q(u∣v)⋅P(word∣u))
                                score = pi.get((k - 1, v),LOG_PROB_OF_ZERO) + q_values.get((u,v), LOG_PROB_OF_ZERO) + wordProb
                                if score > max_score:
                                    max_score = score
                                    max_tag = v
                        # pi (k,u) -> its mean the state k with tag u point on the max tag from previous state
                        pi[(k, u)] = max_score
                        bp[(k, u)] = max_tag
            except:
                print traceback.format_exc()

            max_score = float('-Inf')
            v_max = None

            tags = deque()
            for u in self.S(n-1):
                for v in self.S(n):
                    wordProb = (e_values.get(sent_words[n - 1], defultSet)).get(v)
                    if wordProb == None:
                        wordProb = 0
                    score = pi.get((n-1, v), LOG_PROB_OF_ZERO) + wordProb +  q_values.get((u,STOP_SYMBOL), LOG_PROB_OF_ZERO)
                    if score > max_score:
                        max_score = score
                        v_max = v
                        u_max = u

            tags.append(u_max)
            tags.append(v_max)
        

            try:
                for i, k in enumerate(range(n, 0, -1)):
                        tag = bp[(k, tags[i])]
                        if(tag!=None):
                            tags.append(tag)
            except:
                print traceback.format_exc()
            tags.reverse()

            tagged_sentence = deque()
            for j in range(0, n):
                tagged_sentence.append(sent_words[j] + '/' + tags[j])
            tagged_sentence.append('\n')
            tagged.append(' '.join(tagged_sentence))
        return tagged


def main():
    lexPath = os.getcwd() + "\\data-training-files\\heb-pos.train.lex"
    gramPath = os.getcwd() + "\\data-training-files\\heb-pos.train.gram"

    gramFile = read_gram_file(gramPath)
    lexFile = read_lex_file(lexPath)
    uniqeTags = getAllTags(gramFile, lexFile)
    _Viterbi = Viterbi(uniqeTags)
    	
    sentence = ["yyQUOT THIH NQMH W BGDWL yyDOT","AIF LA NISH LHSTIR ZAT yyDOT"]
    tags = _Viterbi.algoritem(sentence, gramFile[2]['gram_prob_dict'], lexFile)


if __name__ == '__main__':
    main()