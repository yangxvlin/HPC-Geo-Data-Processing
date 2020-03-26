"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-3-11 11:51:27
Description: class for twitter data
"""

import json
import re
from collections import Counter


class TwitterData:
    """ required Dada model for Twitter data to be processed """

    def __init__(self, data: str):
        """
        :param data: twitter string
        """
        json_data = json.loads(data)
        self.language_code = json_data["doc"]["metadata"]["iso_language_code"]

        # method a)
        #   1. search hashtag starts with '#' followed by alphabet or numbers and end with a white space or a punctuation
        #   2. turn it to lower case
        # method b)
        #   use provided entities -> hashtags
        #
        # either method is accepted by:
        #   https://canvas.lms.unimelb.edu.au/courses/17514/discussion_topics/160043 -> suggests hashtag should contain foreign characters
        #       -> https://canvas.lms.unimelb.edu.au/courses/17514/discussion_topics/154594
        # method b is used at here
        json_data_doc = json_data["doc"]
        self.hash_tags = self._hash_tags_to_counter(json_data_doc)
        self._extract_retweeted_quoted(json_data_doc)

    def _extract_retweeted_quoted(self, json_data_doc: dict):
        def push_to_stack(stack_object, json_data_doc_object):
            if "quoted_status" in json_data_doc_object:
                stack_object.append(json_data_doc_object["quoted_status"])

            if "retweeted_status" in json_data_doc_object:
                stack_object.append(json_data_doc_object["retweeted_status"])

        stack = []
        push_to_stack(stack, json_data_doc)

        while stack:
            cur = stack.pop()

            push_to_stack(stack, cur)

            self.hash_tags += self._hash_tags_to_counter(cur)

    def _hash_tags_to_counter(self, json_doc):
        return Counter(map(lambda x: x["text"].lower(), filter(lambda x: self._is_alnum_underscore(x), json_doc["entities"]["hashtags"])))

    @staticmethod
    def _is_alnum_underscore(string: str):
        return bool(re.match('^[a-zA-Z0-9_]+$', string))
