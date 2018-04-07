from evaluation import recall, f_score, macro_avg
from parse_data import read_test_file, read_gold_and_train_file, read_lex_file, read_gram_file
from consts import NUM_OF_GRAM, GRAM_PROB_DICT
from decode import write_tagged_file

from ex4.ex4 import calc_confusion_matrix, save_confusion_matrix, split_train_file

from ex3.ex3 import viterbi

print f_score({1,2}, {1})

ff = [{(1, 1), (1, 2)}, {(1, 1), (1, 2)}]
gg = [{(1, 1), (1, 2)}, {(1, 5), (1, 4)}]
print macro_avg(ff, gg)

# file_path = '/Users/netazinger/Documents/universaty/nlp/ex2/nlp_ex2/data-files/heb-pos.test'
# print len(read_test_file(file_path))
#


file_path = '/Users/netazinger/Documents/universaty/nlp/ex2/nlp_ex2/code/heb-pos.train.lex'
seg_to_tag_to_prob = read_lex_file(file_path)
print seg_to_tag_to_prob['BIRWT']

file_path = '/Users/netazinger/Documents/universaty/nlp/ex2/nlp_ex2/code/heb-pos.train.gram'
gram_level_to_gram_data = read_gram_file(file_path)
assert 1 in gram_level_to_gram_data
assert gram_level_to_gram_data[1][NUM_OF_GRAM] == 127884
assert gram_level_to_gram_data[1][GRAM_PROB_DICT][("NN", )] == -1.69021593151
assert 2 in gram_level_to_gram_data
assert gram_level_to_gram_data[2][NUM_OF_GRAM] == 132884
assert gram_level_to_gram_data[2][GRAM_PROB_DICT][('yyDOT', 'EOS')] == -0.00040766409044


file_path = '/Users/netazinger/Documents/universaty/nlp/ex2/nlp_ex2/data-files/heb-pos.test'
parse_test = read_test_file(file_path)
tagged_file = viterbi(parse_test, gram_level_to_gram_data[2], seg_to_tag_to_prob, gram_level=2)
write_tagged_file(tagged_file, "bi")


# file_path = '/Users/netazinger/Documents/universaty/nlp/ex2/nlp_ex2/data-files/heb-pos.gold'
# gold =  read_gold_and_train_file(file_path)
# file_path = '/Users/netazinger/Documents/universaty/nlp/ex2/nlp_ex2/code/heb-pos.tagged'
# tagged_tested = read_gold_and_train_file(file_path)
# confusion_matrix = calc_confusion_matrix(tagged_tested, gold)
# save_confusion_matrix(confusion_matrix, "basline")


# split_train_file("/Users/netazinger/Documents/universaty/nlp/ex2/nlp_ex2/data-files/heb-pos.train")





print "RUN SUCC!!!!"