"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-3-11 11:52:44
Description: some helper functions
"""

import json
from LanguageSummary import LanguageSummary
import heapq


def preprocess_data(data: str):
    """
    :param data:
    :return: data with end ',' truncated otherwise return None
    """
    if data.endswith('},\n'):
        return data[:-2]
    elif data.endswith('}\n'):
        return data[:-1]
    print("invalid line:", data, end="")
    return None


def read_language_code(file_path: str):
    language_dict = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        for language_code in json_data:
            language = LanguageSummary(language_code, json_data[language_code])
            language_dict[language_code] = language

    return language_dict


def read_data_line_by_line(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield line


def top_n_hash_tags(language_summary_list: list, n=10):
    top_n_hash_tags_list = []
    for language_summary in language_summary_list:
        top_n_hash_tags_list = heapq.nlargest(n, top_n_hash_tags_list + list(language_summary.hash_tag_counters.items()), key=lambda hash_tag_count: hash_tag_count[1])
    return top_n_hash_tags_list


def dump_output(merged_language_summary_list: list):
    top_n_hash_tags_list = top_n_hash_tags(merged_language_summary_list)
    print("=" * 5, "top {} most commonly used hashtags".format(len(top_n_hash_tags_list)), "=" * 5)
    for i, (hash_tag, hash_tag_count) in enumerate(top_n_hash_tags_list, start=1):
        try:
            print("{:2d}. {}, {:,}".format(i, hash_tag, hash_tag_count))
        except UnicodeEncodeError:
            print("UnicodeEncodeError")
    print()

    # TODO need to test if some of top 10 language has 0 count?
    top_n_languages = heapq.nlargest(10, merged_language_summary_list, key=lambda x: x.count)
    print("=" * 5, "top {} most commonly tweeted languages".format(len(top_n_languages)), "=" * 5)
    for i, language_summary in enumerate(top_n_languages, start=1):
        print("{:2d}. {}".format(i, language_summary))
