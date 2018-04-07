import sys
import os
import math
from collections import Counter, defaultdict

sys.path.append(os.path.abspath(os.path.join(__file__, "../..")))

from consts import prob_post_processing, EOS, BOS
from ex2.ex2 import get_segment_to_tags


def split_to_grams(l, n):
    for i in range(0, len(l) - n + 1):
        yield tuple(l[i:i + n])


def calc_lex_result(parse_train_file):
    # flatten list
    flat_train_list = [word_and_tag for sentance in parse_train_file for word_and_tag in sentance]

    # get all tags
    all_tags = [word_and_tag.tag for word_and_tag in flat_train_list]

    # count tags, and seg and tag
    tag_counter = Counter(all_tags)
    word_tag_counter = Counter(flat_train_list)

    # calc p(w_i | t_i)
    prob_of_word_if_known_tag = {
        word_and_tag: prob_post_processing(float(word_tag_counter[word_and_tag]) / tag_counter[word_and_tag.tag])
        for word_and_tag in flat_train_list
    }

    segment_to_tags = get_segment_to_tags(parse_train_file)
    segment_to_tags_and_prob = defaultdict(list)

    for segment, tags in segment_to_tags.iteritems():
        for tag in tags:
            prob = prob_of_word_if_known_tag[(segment, tag)]
            segment_to_tags_and_prob[segment].append((tag, prob))

    return segment_to_tags_and_prob


def write_lex_file(parse_train_file, output_file_path):
    segment_to_tags_and_prob = calc_lex_result(parse_train_file)
    file = open(output_file_path + ".lex","w")
    for segment, tags_prob_list in segment_to_tags_and_prob.iteritems():
        file.write(segment)
        for tag, prob in tags_prob_list:
            file.write("\t%s\t%s" % (tag, prob))
        file.write("\n")
    file.close()


def calc_gram_result(parse_train_file, gram_level=1):
    # get segment only
    parse_words = []
    for sentance in parse_train_file:
        parse_words.append([word_and_tag.tag for word_and_tag in sentance])

    # pendding the data
    padded_data = []
    bos_padding = [BOS] * (1)
    eos_padding = [EOS] * (1)
    for sentance in parse_words:
        padded_data.append(bos_padding + sentance + eos_padding)

    # calc gram
    uni_gram_list = []

    for sentance in parse_words:
        uni_gram_list.extend(split_to_grams(sentance, 1))

    bi_gram_list = []
    for sentance in padded_data:
        bi_gram_list.extend(split_to_grams(sentance, 2))

    uni_gram_count = Counter(uni_gram_list)
    bi_gram_count = Counter(bi_gram_list)

    uni_gram_list_length = len(uni_gram_list)
    uni_gram_to_prob = {uni_gram: math.log(float(count) / uni_gram_list_length) for uni_gram, count in uni_gram_count.iteritems()}

    bi_gram_list_length = len(bi_gram_list)

    uni_gram_count[(BOS,)] = len(parse_train_file)
    for bi_gram, count in bi_gram_count.iteritems():
        # if uni_gram_count[(bi_gram[0],)] == 0:
        #     import ipdb; ipdb.set_trace() # NO_COMMIT
        x = math.log(float(count) / uni_gram_count[(bi_gram[0],)])
    bi_gram_to_prob = {bi_gram: math.log(float(count) / uni_gram_count[(bi_gram[0],)]) for bi_gram, count in bi_gram_count.iteritems()}

    uni_gram_prob_by_order = sorted([(gram, prob) for gram, prob in uni_gram_to_prob.iteritems()], key=lambda x: x[1])
    bi_gram_prob_by_order = sorted([(gram, prob) for gram, prob in bi_gram_to_prob.iteritems()], key=lambda x: x[1])

    return {
        "num_of_uni_gram": uni_gram_list_length,
        "num_of_bi_gram": bi_gram_list_length,
        "uni_gram_prob_by_order": uni_gram_prob_by_order,
        "bi_gram_prob_by_order": bi_gram_prob_by_order
    }

def write_gram_file(parse_train_file, output_file_path):
    gram_result = calc_gram_result(parse_train_file, gram_level=1)

    file = open(output_file_path + ".gram","w")
    file.write("\data\\\n")
    file.write("ngram %s = %s\n" % (1, gram_result['num_of_uni_gram']))
    file.write("ngram %s = %s\n" % (2, gram_result['num_of_bi_gram']))
    # for gram_result in gram_result_list:
    #     file.write("ngram %s = %s\n" % (gram_result['gram_level'], gram_result['num_of_gram']))
    file.write("\n")

    for gram_level, gram_prob_by_order in [(1, gram_result['uni_gram_prob_by_order']), (2, gram_result['bi_gram_prob_by_order'])]:
        file.write("\%s-grams\\\n" % gram_level)
        for gram_and_prob in gram_prob_by_order:
            file.write("%s\t%s\n" % (gram_and_prob[1], " ".join(gram_and_prob[0])))
        file.write("\n")
    file.close()


#
# def calc_gram_result(parse_train_file, gram_level=1):
#     calc_gram_result_2(parse_train_file, gram_level)
#     # get segment only
#     parse_words = []
#     for sentance in parse_train_file:
#         parse_words.append([word_and_tag.tag for word_and_tag in sentance])
#
#     # pendding the data
#     padded_data = []
#     bos_padding = [BOS] * (gram_level - 1)
#     eos_padding = [EOS] * (gram_level - 1)
#     for sentance in parse_words:
#         padded_data.append(bos_padding + sentance + eos_padding)
#
#     # calc gram
#     gram_list = []
#     for sentance in padded_data:
#         gram_list.extend(split_to_grams(sentance, gram_level))
#
#     # count gram
#     sorted_counter_gram_list = sorted([(gram, count) for gram, count in Counter(gram_list).iteritems()], key=lambda x: x[1])
#
#     # calc prob
#     num_of_gram = len(gram_list)
#     gram_prob_by_order = [(gram, math.log(float(count) / num_of_gram)) for gram, count in sorted_counter_gram_list]
#
#     return  {
#         "gram_level": gram_level,
#         "num_of_gram": len(gram_list),
#         "gram_prob_by_order": gram_prob_by_order
#     }
#
#
#
# def write_gram_file(parse_train_file, output_file_path, gram_level=2):
#     gram_result_list = []
#     for gram_level in range(1, gram_level + 1):
#         gram_result_list.append(calc_gram_result(parse_train_file, gram_level=gram_level))
#
#     file = open(output_file_path + ".gram","w")
#     file.write("\data\\\n")
#     for gram_result in gram_result_list:
#         file.write("ngram %s = %s\n" % (gram_result['gram_level'], gram_result['num_of_gram']))
#     file.write("\n")
#
#     for gram_result in gram_result_list:
#         file.write("\%s-grams\\\n" % gram_result['gram_level'])
#         for gram_and_prob in gram_result['gram_prob_by_order']:
#             file.write("%s\t%s\n" % (gram_and_prob[1], " ".join(gram_and_prob[0])))
#         file.write("\n")
#     file.close()


