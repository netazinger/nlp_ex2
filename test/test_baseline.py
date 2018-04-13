import os
import sys

sys.path.append(os.path.abspath(os.path.join(__file__, "../..")))

from collections import defaultdict
from consts import WordAndTag, UNKNOWN_TAG
from src.baseline import get_segment_to_tags, find_most_common_tag_for_segment, tag_file

def test_get_segment_to_tags():
    taged_data_set = [
        WordAndTag(word="vizul", tag="1"),
        WordAndTag(word="shula", tag="1"),
        WordAndTag(word="shula", tag="2"),
        WordAndTag(word="vizul", tag="1"),
        WordAndTag(word="vizul", tag="3"),
        WordAndTag(word="cat", tag="6"),
    ]

    assert get_segment_to_tags(taged_data_set) == {
        "vizul": ["1", "1", "3"],
        "shula": ["1", "2"],
        "cat": ["6"],
    }


def test_find_most_common_tag_for_segment():
    input = {
        "vizul": ["1", "1", "3"],
        "shula": ["1", "2"],
        "cat": ["6"],
    }
    output = find_most_common_tag_for_segment(input)
    assert output == {
        "vizul": "1",
        "shula": "1",
        "cat": "6",
    }
    assert output["bla"] == UNKNOWN_TAG


def test_tag_file():
    segment_to_tag = defaultdict(lambda: UNKNOWN_TAG)
    segment_to_tag.update({
        "vizul": "1",
        "shula": "1",
        "cat": "6",
    })
    parsed_file_to_tag = [
        ["vizul", "shula", "cat"],
        ["vizul", "vizul", "vizul"],
        ["vizul", "ttt", "cat"],
    ]
    output = tag_file(parsed_file_to_tag, segment_to_tag)
    assert output == [
        [WordAndTag(word="vizul", tag="1"), WordAndTag(word="shula", tag="1"),  WordAndTag(word="cat", tag="6")],
        [WordAndTag(word="vizul", tag="1"), WordAndTag(word="vizul", tag="1"), WordAndTag(word="vizul", tag="1")],
        [WordAndTag(word="vizul", tag="1"),  WordAndTag(word="ttt", tag=UNKNOWN_TAG),  WordAndTag(word="cat", tag="6")],
    ]

test_get_segment_to_tags()
test_find_most_common_tag_for_segment()
test_tag_file()
