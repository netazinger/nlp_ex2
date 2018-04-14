import sys
import os
import math
from collections import Counter, defaultdict
import operator



from consts import prob_post_processing, EOS, BOS, GRAM_PROB_DICT, WordAndTag



def split_to_grams(l, n):
    for i in range(0, len(l) - n + 1):
        yield tuple(l[i:i + n])


def calc_prob(count_bi_gram, count_uni_gram, corp_size=0, smooth=False, delta=.00001):
    if not smooth:
        corp_size = 0
        delta = 0
    return prob_post_processing(float(count_bi_gram + delta) / (count_uni_gram + delta * corp_size))


def calc_lex_result(parse_train_file, smooth=False):
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

    # from baseline import get_segment_to_tags, find_most_common_tag_for_segment
    # segment_to_tags = get_segment_to_tags(parsed_train)
    # segment_to_tag = find_most_common_tag_for_segment(segment_to_tags)

    for seg in all_seg:
        for tag in all_tags:
            word_tag_count = float(word_tag_counter[(seg, tag)])
            # if smooth and word_tag_count == 0:
            #     word_tag_count = float(tag_counter[tag]) / len(all_tags)
            prob = calc_prob(word_tag_count,  tag_counter[tag], corp_size=len(all_tags), smooth=smooth)
            if prob is not None:
                seg_to_tag_to_prob[seg][tag] = prob

    # if smooth:
    #     words = [word_and_tag.word for word_and_tag in flat_train_lis]
    #
    #     for tag in all_tags:
    #
    #         seg_to_tag_to_prob["NNP"][tag] = calc_prob(0,  tag_counter[tag], corp_size=len(all_tags), smooth=smooth)
    return seg_to_tag_to_prob


def write_lex_file(parse_train_file, output_file_path, smooth=False):
    seg_to_tag_to_prob = calc_lex_result(parse_train_file, smooth=smooth)
    file = open(output_file_path + ".lex", "w")
    for segment, tag_to_prob in seg_to_tag_to_prob.iteritems():
        file.write(segment)
        for tag in sorted(tag_to_prob.keys()):
            file.write("\t%s\t%s" % (tag, tag_to_prob[tag]))
        file.write("\n")
    file.close()


def calc_gram_result(parse_train_file, gram_level=1, smooth=False):
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

    for sentance in padded_data:
        uni_gram_list.extend(split_to_grams(sentance, 1))

    bi_gram_list = []
    for sentance in padded_data:
        bi_gram_list.extend(split_to_grams(sentance, 2))

    uni_gram_count = Counter(uni_gram_list)
    bi_gram_count = Counter(bi_gram_list)

    uni_gram_list_length = len(uni_gram_list)
    uni_gram_to_prob = {uni_gram: math.log(float(count) / uni_gram_list_length) for uni_gram, count in uni_gram_count.iteritems()}
    uni_gram_to_prob_no_log = {uni_gram: float(count) / uni_gram_list_length for uni_gram, count in uni_gram_count.iteritems()}

    bi_gram_list_length = len(set(bi_gram_list))
    uni_tag = uni_gram_count.keys()

    bi_gram_to_prob = {}
    if smooth:
        for gram1 in uni_tag:
            for gram2 in uni_tag:
                count = bi_gram_count[gram1 + gram2]
                bi_gram_to_prob[gram1 + gram2] = calc_prob(count,  uni_gram_count[gram1], corp_size=uni_gram_list_length, smooth=smooth)
    else:
        bi_gram_to_prob = {bi_gram:calc_prob(count,  uni_gram_count[(bi_gram[0],)], corp_size=uni_gram_list_length, smooth=smooth) for bi_gram, count in bi_gram_count.iteritems()}

    uni_gram_prob_by_order = sorted([(gram, prob) for gram, prob in uni_gram_to_prob.iteritems()], key=lambda x: x[1])
    bi_gram_prob_by_order = sorted([(gram, prob) for gram, prob in bi_gram_to_prob.iteritems()], key=lambda x: x[1])

    return {
        "num_of_uni_gram": len(set(uni_gram_list)),
        "num_of_bi_gram": bi_gram_list_length,
        "uni_gram_prob_by_order": uni_gram_prob_by_order,
        "bi_gram_prob_by_order": bi_gram_prob_by_order
    }

def write_gram_file(parse_train_file, output_file_path, smooth=False):
    gram_result = calc_gram_result(parse_train_file, gram_level=1, smooth=smooth)

    file = open(output_file_path + ".gram","w")
    file.write("\data\\\n")
    file.write("ngram %s = %s\n" % (1, gram_result['num_of_uni_gram']))
    file.write("ngram %s = %s\n" % (2, gram_result['num_of_bi_gram']))
    file.write("\n")

    for gram_level, gram_prob_by_order in [(1, gram_result['uni_gram_prob_by_order']), (2, gram_result['bi_gram_prob_by_order'])]:
        file.write("\%s-grams\\\n" % gram_level)
        for gram_and_prob in gram_prob_by_order:
            file.write("%s\t%s\n" % (gram_and_prob[1], "\t".join(gram_and_prob[0])))
        file.write("\n")
    file.close()


def viterbi_sentence(sentence, gram_prob_dict, seg_to_tag_to_prob, tags, gram_level=2, uni_gram_prob_dict=None):
    padded_sentence = [BOS] * (gram_level - 1) + sentence + [EOS] * (gram_level - 1)

    matrix = [[-1000] * len(tags) for i in range(len(sentence))]
    sentence_tag = []
    seg = sentence[0]
    for tag_index in range(len(tags)):
        tag = tags[tag_index]
        matrix[0][tag_index] = gram_prob_dict[(BOS, tag)] + seg_to_tag_to_prob[seg][tag]

    for i in range(gram_level - 1,  len(sentence)):
        seg = sentence[i]
        for tag_index in range(len(tags)):
            v_s = []
            if seg in seg_to_tag_to_prob:
                for tag_index_1 in range(len(tags)):
                    v_s_prob = gram_prob_dict[(tags[tag_index_1], tag)] + seg_to_tag_to_prob[seg][tags[tag_index]] # + matrix[i - 1][tag_index_1]
                    v_s.append(v_s_prob)
                max_index, max_value = max(enumerate(v_s), key=operator.itemgetter(1))
                matrix[i][tag_index] = max_value
            else:
                matrix[i][tag_index] = 0 if tags[tag_index] == "NNP" else -100


    for i in range(len(sentence)):
        max_index, max_value = max(enumerate(matrix[i]), key=operator.itemgetter(1))
        sentence_tag.append(tags[max_index])


    return sentence_tag


def viterbi(parse_test, gram_result, seg_to_tag_to_prob, gram_level=2):
    gram_prob_dict = gram_result[2][GRAM_PROB_DICT]
    tags = list({tags[0] for tags in gram_prob_dict})
    tagged_data = []


    for sentence in parse_test:
        sentence_tag = viterbi_sentence(sentence, gram_prob_dict, seg_to_tag_to_prob, tags, gram_level=2, uni_gram_prob_dict = gram_result[1][GRAM_PROB_DICT])
        tagged_data.append([WordAndTag(sentence[i], sentence_tag[i]) for i in range(len(sentence))])
    return tagged_data
