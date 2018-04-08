import math
import pickle
import doctest
import numpy as np

from collections import OrderedDict
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer


def data_unpickle(path):
    with open(path, "rb") as reader:
        feature_data = pickle.load(reader)
    return feature_data


def data_pickle(path, data):
    with open(path, "wb") as writer:
        pickle.dump(data, writer)


class TrueTransformer:

    def __init__(self, vectorizer_type="tf-idf"):
        self.vectorizer_type = vectorizer_type

    def filter_feature_data(self, feature_data, true_feature_set):
        filtered_feature_data = {}
        for ke in feature_data.keys():
            filtered_feature_data[ke] = [item for item in feature_data[ke] if item[0] in true_feature_set]
        return filtered_feature_data

    def fit_transform(self, feature_data, position_func, join_func, alpha, beta, order):
        self.fit(feature_data)
        return self.transform(feature_data, position_func, join_func, alpha, beta, order)

    def fit(self, feature_data):
        # order
        self._max_list_len = max([len(v) for v in feature_data.values()])

        # freq
        if self.vectorizer_type == "tf-idf":
            self._vectorizer = TfidfVectorizer(max_df=1.0, min_df=0.0, use_idf=True, tokenizer=lambda text: text.split())
        elif self.vectorizer_type == "count":
            self._vectorizer = CountVectorizer(binary=False, tokenizer=lambda text: text.split())
        elif self.vectorizer_type == "binary":
            self._vectorizer = CountVectorizer(binary=True, tokenizer=lambda text: text.split())
        else:
            raise Exception()

        text_feature_data = {}
        for k in feature_data.keys():
            text_feature_data[k] = " ".join([str(item[0]) for item in feature_data[k]])
        # print([value for value in text_feature_data.values()])
        self._vectorizer.fit([value for value in text_feature_data.values()])
        self._features_in_order = self._vectorizer.get_feature_names()

    def transform(self, feature_data, position_func, join_func, alpha, beta, order=True):
        feature_lists = dict()
        for inum, k in enumerate(feature_data.keys()):
            
            if inum % 100 == 0:
                print(inum)

            # freq
            freq_f_l = self._vectorizer.transform(
                [" ".join([str(item[0]) for item in feature_data[k]])]).toarray().reshape(
                (len(self._features_in_order),))

            if order:
                # order
                tmp_feature_in_order_dict = dict(zip(list(map(lambda item: int(item), self._features_in_order)),
                                                 range(len(self._features_in_order))))
                pos_f_l = [0 for i in range(len(self._features_in_order))]
                for j in range(len(feature_data[k])):
                        pos_f_l[tmp_feature_in_order_dict[feature_data[k][j][0]]] += position_func(j, self._max_list_len)
                pos_f_l = np.array(pos_f_l)
                pos_f_l = pos_f_l/np.linalg.norm(pos_f_l)


                # join
                f_l = join_func(alpha * pos_f_l, beta * freq_f_l)
            else:
                f_l = freq_f_l


            feature_lists[k] = f_l
        return feature_lists


if __name__ == "__main__":
    # doctest.testmod()

    trueTransformer = TrueTransformer()

    true_feature_set = {16, 8, 182, 9}

    feature_data = {1238: [(5, 3), (16, 7), (8, 12), (511111, 21), (5, 56)],
                                                        2254: [(5, 11), (8, 12)],
                                                        3578: [(9, 11)],
                                                        7654: [(5, 1), (9, 1)],
                                                        2931: [(6, 2), (8, 1)]}

    print(feature_data)

    filtered_feature_data = trueTransformer.filter_feature_data(feature_data, true_feature_set)

    true_feature_lists = trueTransformer.fit_transform(feature_data,
                                    lambda x, y: math.log(1 + y / (x + 1)), lambda x, y: x * y, 1, 1, order=False)

    print(trueTransformer._features_in_order)
    for k in true_feature_lists.keys():
        print(true_feature_lists[k])


    # import pandas
    # table = pandas.DataFrame(true_feature_lists, index=trueTransformer._features_in_order).transpose()
    # print(table)
    #
    # arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    # df = pandas.DataFrame.from_records(data=arr, index=['a', 'b', 'c'], columns=['aa', 'bb', 'cc'])
    # print(df)

