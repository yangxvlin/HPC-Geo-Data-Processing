"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-3-11 11:51:27
Description: class for twitter data
"""

import json
import re
from string import punctuation, whitespace


STOP_SIGN = punctuation + whitespace


class TwitterData:
    """ required Dada model for Twitter data to be processed """

    def __init__(self, data: str):
        """
        :param data: twitter string
        """
        json_data = json.loads(data)
        self.language_code = json_data["doc"]["metadata"]["iso_language_code"]
        # 1. search hashtag starts with '#' followed by alphabet or numbers and end with a white space or a punctuation
        # 2. turn it to lower case
        # self.hash_tags = tuple(map(lambda x: x[:-1].lower(), re.findall("#[^\s{}]+[\s{}]".format(punctuation, punctuation), json_data["doc"]["text"])))
        # self.hash_tags = tuple(map(lambda x: x[:-1].lower(), re.findall("#[a-zA-Z0-9]+[\s{}]".format(punctuation), json_data["doc"]["text"])))

        self.hash_tags = []
        hash_tag_string = json_data["doc"]["text"].split('#')
        for tag in hash_tag_string[1:]:
            string = ""
            for character in tag:
                if character not in STOP_SIGN:
                    string += character
                else:
                    break
            if len(string) > 0:
                self.hash_tags.append("#" + string.lower())
