import string
from nltk.stem.snowball import SnowballStemmer
from pymystem3 import Mystem

class FeatureExtractor:
    def __init__(self, res_skill_dictionary):
        #self.rustemmer = SnowballStemmer("russian")
        #self.enstemmer = SnowballStemmer("english")
        self.stemmer = Mystem()
        
        self.english_letters = set("qwertyuiopasdfghjklzxcvbnm")
        self.russian_letters = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
        self.numbers = set("01234567890")
        self.dict_words = set()
        
        # self.side_chars = set(",.;:/- \n\t")
        self.side_chars = set(string.punctuation + " \n\t")


        # concatenate keys and normalize words
        self.temp_skill_dictionary = {}
        for k1 in res_skill_dictionary:
            self.temp_skill_dictionary[k1] = {}
            for k2 in res_skill_dictionary[k1]:
                self.temp_skill_dictionary[k1]["".join(k2.split())] = [self.preprocess_dict_text(text) for text in res_skill_dictionary[k1][k2]]

    def preprocess_dict_text(self, text):
        preprocessed_words = [self.preprocess_dict_word(word) for word in text.split()]
        self.dict_words = self.dict_words.union(set(preprocessed_words))
        return " ".join(preprocessed_words)

    def preprocess_dict_word(self, word):
        word = word.lower()
        word_letters = set(word)
        if len(word_letters.intersection(self.numbers)) == 0 and len(word_letters.intersection(self.side_chars)) == 0:
            if len(word_letters.intersection(self.english_letters)) > 0 and len(word_letters.intersection(self.russian_letters)) == 0:
                #return self.enstemmer.stem(word)
                return word
            if len(word_letters.intersection(self.russian_letters)) > 0 and len(word_letters.intersection(self.english_letters)) == 0:
                #return self.rustemmer.stem(word)
                return self.stemmer.lemmatize(word)[0]
        return word

    def preprocess_resume_text(self, text):
        return " ".join([self.preprocess_resume_word(word) for word in text.split()])

    def preprocess_resume_word(self, word):
        word = word.lower()
        if word in self.dict_words:
            return word
        if self.preprocess_dict_word(word) in self.dict_words:
            return self.preprocess_dict_word(word)
        if word[0] in self.side_chars and word[1:] in self.dict_words:
            return word[1:]
        if word[-1] in self.side_chars and word[:-1] in self.dict_words:
            return word[:-1]
        if word[0] in self.side_chars and self.preprocess_dict_word(word[1:]) in self.dict_words:
            return self.preprocess_dict_word(word[1:])
        if word[-1] in self.side_chars and self.preprocess_dict_word(word[:-1]) in self.dict_words:
            return self.preprocess_dict_word(word[:-1])
        if word[0] in self.side_chars and word[-1] in self.side_chars:
            if word[1:-1] in self.dict_words:
                return word[1:-1]
            if self.preprocess_dict_word(word[1: -1]) in self.dict_words:
                return self.preprocess_dict_word(word[1:-1])
        return word

    def extract_features(self, text):
        preprocessed_text = self.preprocess_resume_text(text)
        features = []
        meetings = {}
        for k1 in self.temp_skill_dictionary.keys():
            for k2 in self.temp_skill_dictionary[k1].keys():
                for item in self.temp_skill_dictionary[k1][k2]:
                    ind = 0
                    while ind < len(preprocessed_text) - 1 and ind != -1:
                        ind = preprocessed_text.find(item, ind + 1)
                        if ind != -1 and (ind - 1 == -1 or preprocessed_text[ind - 1] in self.side_chars) and (
                                    ind + len(item) == len(preprocessed_text) or preprocessed_text[ind + len(item)] in self.side_chars):
                            if ind in meetings:
                                meetings[ind].append((k2, item))
                            else:
                                meetings[ind] = [(k2, item)]
        for indk in meetings:
            meetings[indk] = list(set(meetings[indk]))
            max_len_k2 = sorted([(k2, item, len(item)) for k2, item in meetings[indk]], key=lambda x: x[1], reverse=True)[0][0]
            features.append((max_len_k2, indk))
        return features


