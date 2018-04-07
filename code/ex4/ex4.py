from collections import defaultdict


def calc_confusion_matrix(tagged_tested, gold):
    confusion_matrix_dict = defaultdict(lambda:defaultdict(int))
    flat_gold =          [word_and_tag for sentance in gold for word_and_tag in sentance]
    flat_tagged_tested = [word_and_tag for sentance in tagged_tested for word_and_tag in sentance]
    all_tags = {word_and_tag.tag for word_and_tag in flat_gold} | {word_and_tag.tag for word_and_tag in flat_tagged_tested}

    assert len(flat_gold) == len(flat_tagged_tested)
    for i in range(len(flat_gold)):
        confusion_matrix_dict[flat_gold[i].tag][flat_tagged_tested[i].tag] += 1
    return confusion_matrix_dict


def save_confusion_matrix(confusion_matrix_dict, file_name):
    sorted_tags = sorted(confusion_matrix_dict.keys())
    file = open(file_name + ".confusion_matrix.csv", "w")
    file.write("," + ",".join(sorted_tags) + '\n')
    for row_tag in sorted_tags:
        file.write(row_tag)
        for cal_tag in sorted_tags:
            file.write(",%s" % confusion_matrix_dict[row_tag][cal_tag] )
        file.write("\n")

    file.close()

