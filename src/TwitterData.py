"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-3-11 11:51:27
Description: class for twitter data
"""

import json
import re


class TwitterData:
    """ required Dada model for Twitter data to be processed """

    def __init__(self, data: str):
        """
        :param data: twitter string
        """
        json_data = json.loads(data)
        self.language_code = json_data["doc"]["metadata"]["iso_language_code"]
        self.hash_tags = re.findall("#[a-zA-Z0-9_]+", json_data["doc"]["text"])
