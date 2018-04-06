from consts import EOS, BOS
from collections import Counter
import math


def split_to_grams(l, n):
    for i in range(0, len(l) - n + 1):
        yield tuple(l[i:i + n])


def calc_gram_result(parse_train_file, gram_level=1):
    # get segment only
    parse_words = []
    for sentance in parse_train_file:
        parse_words.append([word_and_tag.word for word_and_tag in sentance])

    # pendding the data
    padded_data = []
    bos_padding = [BOS] * (gram_level - 1)
    eos_padding = [EOS] * (gram_level - 1)
    for sentance in parse_words:
        padded_data.append(bos_padding + sentance + eos_padding)

    # calc gram
    gram_list = []
    for sentance in padded_data:
        gram_list.extend(split_to_grams(sentance, gram_level))

    # count gram
    sorted_counter_gram_list = sorted([(gram, count)  for gram, count in Counter(gram_list).iteritems()], key=lambda x: x[1])

    # calc prob
    num_of_gram = len(gram_list)
    gram_prob_by_order = [(gram, math.log(float(count) / num_of_gram)) for gram, count in sorted_counter_gram_list]

    return  {
        "gram_level": gram_level,
        "num_of_gram": len(gram_list),
        "gram_prob_by_order": gram_prob_by_order
    }



def write_gram_file(parse_train_file, output_file_path, gram_level=2):
    gram_result_list = []
    for gram_level in range(1, gram_level + 1):
        gram_result_list.append(calc_gram_result(parse_train_file, gram_level=gram_level))

    file = open(output_file_path + ".gram","w")
    file.write("\data\\\n")
    for gram_result in gram_result_list:
        file.write("ngram %s = %s\n" % (gram_result['gram_level'], gram_result['num_of_gram']))
    file.write("\n")

    for gram_result in gram_result_list:
        file.write("\%s-grams\\\n" % gram_result['gram_level'])
        for gram_and_prob in gram_result['gram_prob_by_order']:
            file.write("%s\t%s\n" % (gram_and_prob[1], " ".join(gram_and_prob[0])))
        file.write("\n")
    file.close()


