import sys
import os
import math
from collections import Counter, defaultdict
import operator

sys.path.append(os.path.abspath(os.path.join(__file__, "../..")))

from consts import prob_post_processing, EOS, BOS, GRAM_PROB_DICT, WordAndTag
from ex2.ex2 import get_segment_to_tags


def split_to_grams(l, n):
    for i in range(0, len(l) - n + 1):
        yield tuple(l[i:i + n])


def calc_lex_result(parse_train_file):
    # flatten list
    flat_train_list = [word_and_tag for sentance in parse_train_file for word_and_tag in sentance]

    # get all tags
    all_tags = [word_and_tag.tag for word_and_tag in flat_train_list]
    all_seg = {word_and_tag.word for word_and_tag in flat_train_list}

    # couunt tags, and seg and tag
    tag_counter = Counter(all_tags)
    word_tag_counter = Counter(flat_train_list)
    all_tags = set(all_tags)

    seg_to_tag_to_prob = defaultdict(dict)
    for seg in all_seg:
        for tag in all_tags:
            word_tag_count = float(word_tag_counter[(seg, tag)])
            if word_tag_count:
                seg_to_tag_to_prob[seg][tag] = prob_post_processing(word_tag_count / tag_counter[tag])
    return seg_to_tag_to_prob


def write_lex_file(parse_train_file, output_file_path):
    seg_to_tag_to_prob = calc_lex_result(parse_train_file)
    file = open(output_file_path + ".lex", "w")
    for segment, tag_to_prob in seg_to_tag_to_prob.iteritems():
        file.write(segment)
        for tag in sorted(tag_to_prob.keys()):
            file.write("\t%s\t%s" % (tag, tag_to_prob[tag]))
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

    uni_gram_list_length = len(set(uni_gram_list))
    uni_gram_to_prob = {uni_gram: math.log(float(count) / uni_gram_list_length) for uni_gram, count in uni_gram_count.iteritems()}

    bi_gram_list_length = len(set(bi_gram_list))

    uni_gram_count[(BOS,)] = len(parse_train_file)
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
            file.write("%s\t%s\n" % (gram_and_prob[1], "\t".join(gram_and_prob[0])))
        file.write("\n")
    file.close()


def viterbi_sentence(sentence, gram_prob_dict, seg_to_tag_to_prob, tags, gram_level=2):
    padded_sentence = [BOS] * (gram_level - 1) + sentence + [EOS] * (gram_level - 1)\

    matrix = [[0] * len(tags) for i in range(len(sentence))]
    sentence_tag = []

    seg = sentence[0]
    for tag_index in range(len(tags)):
        matrix[0][tag_index] = seg_to_tag_to_prob[seg][tags[tag_index]]
    max_index, max_value = max(enumerate(matrix[0]), key=operator.itemgetter(1))
    sentence_tag.append(tags[max_index])

    for i in range(gram_level - 1,  len(sentence)):
        seg = sentence[i]

        for tag_index in range(len(tags)):
            tag = tags[0]
            gram_prob = gram_prob_dict[(tag, sentence_tag[i - 1])]

            matrix[i][tag_index] += seg_to_tag_to_prob[seg][tags[0]] + gram_prob
        max_index, max_value = max(enumerate(matrix[i]), key=operator.itemgetter(1))
        sentence_tag.append(tags[max_index])

    return sentence_tag


def viterbi(parse_test, gram_result, seg_to_tag_to_prob, gram_level=2):
    gram_prob_dict = gram_result[GRAM_PROB_DICT]
    tags = list({tags[0] for tags in gram_prob_dict})
    tagged_data = []

    for sentence in parse_test:
        sentence_tag = viterbi_sentence(sentence, gram_prob_dict, seg_to_tag_to_prob, tags, gram_level=2)
        tagged_data.append([WordAndTag(sentence[i], sentence_tag[i]) for i in range(len(sentence))])
    return tagged_data





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


