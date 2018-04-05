import sys
import os

from collections import defaultdict
from collections import Counter

from consts import WordAndTag, UNKNOWN_TAG

sys.path.append(os.path.abspath(os.path.join(__file__, "../..")))
# os.path.abspath(os.path.join(__file__, os.pardir))

def get_segment_to_tags(taged_data_set):
    segment_to_tags = defaultdict(list)

    for sentence in taged_data_set:
        if type(sentence) == list:
            for word_and_tag in sentence:
                segment_to_tags[word_and_tag.word].append(word_and_tag.tag)
        if type(sentence) == WordAndTag:
            segment_to_tags[sentence.word].append(sentence.tag)

    return segment_to_tags


def find_most_common_tag_for_segment(segment_to_tags,unknown_tag=None):
    unknown_tag = unknown_tag or UNKNOWN_TAG
    segment_to_tag = defaultdict(lambda: unknown_tag)
    for segment, tags in segment_to_tags.iteritems():
        segment_to_tag[segment] = Counter(tags).most_common(1)[0][0]
    return segment_to_tag


def tag_file(parsed_file_to_tag, segment_to_tag):
    taged_file = []
    for sentence in parsed_file_to_tag:
        taged_file.append([WordAndTag(word=word, tag=segment_to_tag[word]) for word in sentence])
    return taged_file



