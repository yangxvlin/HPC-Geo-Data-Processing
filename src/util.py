"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-3-11 11:52:44
Description: some helper functions
"""

import json

from TwitterData import TwitterData

""" separator used for pretty printing """
SEPARATOR = "=" * 5


def preprocess_data(data: str):
    """
    :param data: raw string data
    :return: data with end ',' truncated otherwise return None
    """
    if data.startswith('{'):
        if data.endswith('},\n'):
            return data[:-2]
        elif data.endswith('}\n'):
            return data[:-1]
    print("invalid line:", data, end="")
    return None


def processing_data(preprocessed_line: str, hash_tag_count, language_code_count):
    """
    :param preprocessed_line: raw data after pre-processing
    :param hash_tag_count: {hash_tag, int} object
    :param language_code_count: {country_code: int} object
    """
    twitter_data = TwitterData(preprocessed_line)
    language_code_count[twitter_data.language_code] += 1

    for hash_tag in twitter_data.hash_tags:
        hash_tag = hash_tag.lower()

        hash_tag_count[hash_tag] += 1


def read_language_code_dict(file_path: str):
    """
    :param file_path: country code file path
    :return: {country_code: country_name} dict
    """

    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def read_data_line_by_line(file_path: str):
    """
    lazy line by line reader
    :param file_path: twitter data file path
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield line


def dump_hash_tag_output(hash_tag_count: list):
    """
    :param hash_tag_count: {hash_tag, int} object
    """
    top_n_hash_tags_list = hash_tag_count
    print(SEPARATOR, "top {} most commonly used hashtags".format(len(top_n_hash_tags_list)), SEPARATOR)
    for i, (hash_tag, hash_tag_count) in enumerate(top_n_hash_tags_list, start=1):
        try:
            print("{:2d}. {: <25}, {:,}".format(i, hash_tag, hash_tag_count))
        except UnicodeEncodeError:
            print("UnicodeEncodeError")
    print()


def dump_country_code_output(reduced_language_code_count: list, language_code_dict: dict):
    """
    :param reduced_language_code_count: {country_code: int} object
    :param language_code_dict: {country_code: country_name} object
    """
    top_n_languages = reduced_language_code_count
    print(SEPARATOR, "top {} most commonly tweeted languages".format(len(top_n_languages)), SEPARATOR)
    for i, (language_code, count) in enumerate(top_n_languages, start=1):
        print("{:2d}. {: <10} ({: >3}), {:,}".format(i, language_code_dict[language_code], language_code, count))
    print()


def dump_time(comm_rank, title, time_period):
    """
    :param comm_rank: the rank of processor
    :param title: the content of printing
    :param time_period: the period of time to be displayed
    """
    print(SEPARATOR, "processor #{} does {} for {}(s)".format(comm_rank, title, time_period), SEPARATOR)
    print()


def read_n_lines(twitter_data_path: str):
    """
    :param twitter_data_path: twitter data file path
    :return: read number of lines of data
    """
    with open(twitter_data_path, 'r', encoding='utf-8') as file:
        first_line = file.readline()
        assert first_line.endswith(",\"rows\":[\n")
        first_line = first_line[:-10] + "}"
        json_first_line = json.loads(first_line)
        return json_first_line["total_rows"] - json_first_line["offset"]


def merge_list(x: list, y: list, n=10):
    """
    :param x: sorted list x
    :param y: sorted list y
    :param n: merged list size
    :return: [(hash_tag, count)] list with size n
    """
    merged = []

    while len(merged) < n and (len(x) > 0 or len(y) > 0):
        x_max = None
        y_max = None

        if len(x) > 0:
            x_max = x[0]
        if len(y) > 0:
            y_max = y[0]

        if not x_max and y_max:
            merged.append(y_max)
            y = y[1:]
        elif x_max and not y_max:
            merged.append(x_max)
            x = x[1:]
        elif x_max and y_max:
            if x_max[1] >= y_max[1]:
                merged.append(x_max)
                x = x[1:]
            else:
                merged.append(y_max)
                y = y[1:]

    return merged


def dump_num_processor(comm_size):
    """
    :param comm_size: number of processor
    """
    print(SEPARATOR*2, "runs with {} processors".format(comm_size), SEPARATOR*2)
    print()
