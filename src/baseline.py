import sys
import os

from collections import defaultdict
from collections import Counter

from consts import WordAndTag, UNKNOWN_TAG, Model

def get_segment_to_tags(taged_data_set):
    segment_to_tags = defaultdict(list)

    for sentence in taged_data_set:
        if type(sentence) == list:
            for word_and_tag in sentence:
                segment_to_tags[word_and_tag.word].append(word_and_tag.tag)
        if type(sentence) == WordAndTag:
            segment_to_tags[sentence.word].append(sentence.tag)

    return segment_to_tags


def find_most_common_tag_for_segment(segment_to_tags, unknown_tag=None):
    unknown_tag = unknown_tag or UNKNOWN_TAG
    segment_to_tag = defaultdict(lambda: unknown_tag)
    for segment, tags in segment_to_tags.iteritems():
        segment_to_tag[segment] = Counter(tags).most_common(1)[0][0]
    return segment_to_tag


def tag_file(parsed_file_to_tag, segment_to_tag):
    tagged_file = []
    for sentence in parsed_file_to_tag:
        tagged_file.append([WordAndTag(word=word, tag=segment_to_tag[word]) for word in sentence])
    return tagged_file


def write_train_baseline(parsed_train, original_file_name):
    segment_to_tags = get_segment_to_tags(parsed_train)
    segment_to_tag = find_most_common_tag_for_segment(segment_to_tags)
    file = open(original_file_name + "." + Model.BASELINE, "w")
    for segment, tag in segment_to_tag.iteritems():
        file.write("%s %s\n" % (segment, tag))
    file.close()


def parse_train_baseline_tag(baseline_tag):
    return WordAndTag(*map(lambda x: x.replace('\n', ''), baseline_tag.split(" ")))


def read_train_baseline(file_name_path, unknown_tag=None):
    unknown_tag = unknown_tag or UNKNOWN_TAG
    with open(file_name_path) as f:
        content = f.readlines()

    segment_to_tag = defaultdict(lambda: unknown_tag)
    for word_and_tag in map(parse_train_baseline_tag, content):
        segment_to_tag[word_and_tag.word] = word_and_tag.tag
    return segment_to_tag








