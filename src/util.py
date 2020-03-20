"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-3-11 11:52:44
Description: some helper functions
"""

import json
from collections import Counter

from LanguageSummary import LanguageSummary
import heapq

from TwitterData import TwitterData

SEPARATOR = "=" * 5


TIME_FORMAT = "%H:%M:%S.%f"


def preprocess_data(data: str):
    """
    :param data:
    :return: data with end ',' truncated otherwise return None
    """
    if data.startswith('{'):
        if data.endswith('},\n'):
            return data[:-2]
        elif data.endswith('}\n'):
            return data[:-1]
    print("invalid line:", data, end="")
    return None


def processing_data(preprocessed_line: str, hash_tag_count, language_summary_dict):
    twitter_data = TwitterData(preprocessed_line)

    for hash_tag in twitter_data.hash_tags:
        hash_tag_count[hash_tag] += 1

    try:
        language_summary_dict[twitter_data.language_code].summarize(twitter_data)
    except KeyError:
        language_summary_dict[twitter_data.language_code] = LanguageSummary(twitter_data.language_code, "unknown")
        language_summary_dict[twitter_data.language_code].summarize(twitter_data)


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


def dump_hash_tag_output(hash_tag_count: Counter, n=10):
    hash_tag_count_list = list(hash_tag_count.items())
    top_n_hash_tags_list = heapq.nlargest(n, hash_tag_count_list, key=lambda x: x[1])
    if top_n_hash_tags_list:
        _, nth_hash_tag_count = top_n_hash_tags_list[-1]
        top_n_hash_tags_list = sorted(list(filter(lambda x: x[1] >= nth_hash_tag_count, hash_tag_count_list)), key=lambda x: x[1], reverse=True)

    print(SEPARATOR, "top {} most commonly used hashtags".format(len(top_n_hash_tags_list)), SEPARATOR)
    for i, (hash_tag, hash_tag_count) in enumerate(top_n_hash_tags_list, start=1):
        try:
            print("{:2d}. {: <25}, {:,}".format(i, hash_tag, hash_tag_count))
        except UnicodeEncodeError:
            print("UnicodeEncodeError")
    print()


def dump_country_code_output(merged_language_summary_list: list, n=10):
    non_zero_merged_language_summary_list = list(filter(lambda x: x.count > 0, merged_language_summary_list))
    top_n_languages = heapq.nlargest(n, non_zero_merged_language_summary_list, key=lambda x: x.count)
    if top_n_languages:
        nth_language_count = top_n_languages[-1].count
        top_n_languages = sorted(list(filter(lambda x: x.count >= nth_language_count, non_zero_merged_language_summary_list)), key=lambda x: x.count, reverse=True)
    print(SEPARATOR, "top {} most commonly tweeted languages".format(len(top_n_languages)), SEPARATOR)
    for i, language_summary in enumerate(top_n_languages, start=1):
        print("{:2d}. {}".format(i, language_summary))
    print()
    # print(sorted(non_zero_merged_language_summary_list, key=lambda x: x.count, reverse=True))


def dump_time(comm_rank, title, time_period):
    print(SEPARATOR, "processor #{} does {} for {}(micro s)".format(comm_rank, title, time_period.microseconds), SEPARATOR)
    print()
