"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-3-18 18:49:24
Description: 
"""

from TwitterData import TwitterData


class LanguageSummary:
    def __init__(self, language_code: str, name: str):
        self.language_code = language_code
        self.name = name
        self.count = 0

    def summarize(self, twitter_data: TwitterData):
        assert twitter_data.language_code == self.language_code
        self.count += 1

    def __repr__(self):
        return "{: <10} ({: >3}), {:,}".format(self.name, self.language_code, self.count)

    def __cmp__(self, other):
        if self.count > other.count:
            return 1
        elif self.count < other.count:
            return -1
        else:
            return 0

    def __add__(self, other):
        assert self.language_code == other.language_code
        self.count += other.count
        return self

    def __hash__(self):
        return hash(self.language_code)

    @staticmethod
    def merge_language_list(x: dict, y: dict):
        res = x.copy()

        for language_code in set(list(x.keys()) + list(y.keys())):
            if language_code not in x:
                res[language_code] = y[language_code]
            else:
                if language_code in y:
                    res[language_code] += y[language_code]
        return res
