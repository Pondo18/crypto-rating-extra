import re
import emoji
import pandas as pd
from typing import List
import nltk
from nltk import word_tokenize


class Preprocessing:

    @staticmethod
    # broad cleaning of data; also convert abbreviations to normal form (e.g. I'm -> I am) in order to make it more
    # suitable for NLP/ML tasks
    def clean_column(data: object) -> object:
        if data is not None:
            data = data.lower()
            data = re.sub('re:', '', data)
            data = re.sub('-', '', data)
            data = re.sub('_', '', data)
            data = re.sub(r'[^\w\s]', '', data)
            data = re.sub('[[^]]]', '', data)
            data = re.sub(r"'ve", " have ", data)
            data = re.sub(r"can't", "cannot ", data)
            data = re.sub(r"n't", " not ", data)
            data = re.sub(r"I'm", "I am", data)
            data = re.sub(r" m ", " am ", data)
            data = re.sub(r"'re", " are ", data)
            data = re.sub(r"'d", " would ", data)
            data = re.sub(r"'ll", " will ", data)
            data = data.strip()
            data = data.replace("\n", "")
            return data

    @staticmethod
    # convert data as strings in order to make the data more suitable (e.g. remove emojis..)
    def string_convert(data: object) -> object:
        result = [str(word) for word in data]
        result = "".join(result)
        return result

    @staticmethod
    # remove emojis due to its better for further nlp/ml tasks
    def remove_emojis(data: object) -> object:
        string_emojiless = emoji.get_emoji_regexp().sub(u'', data)
        return string_emojiless

    @staticmethod
    # apply lowercase on a whole column within a pd.DataFrame()
    def df_lower(df: pd.DataFrame(), column: int) -> pd.DataFrame():
        return df.iloc[:, column].str.lower()

    @staticmethod
    # apply lowercase on a List[strings]
    def to_lower_case(data: object) -> object:
        lower_case_data: List = [word.lower() for word in data]
        return lower_case_data

    @staticmethod
    # applying tokenization on a whole column within a pd.DataFrame() would be df["selected column"].apply(word_tokenize) -> usage of nltk lib
    # this one is for parsing a string list and receive a tokenized list of strings!! -> use this function if you want to operate with lists
    def tokenization(data: List[str]) -> List[str]:
        tokenized_content: List[str] = [word_tokenize(sentence) for sentence in data]
        return tokenized_content

    @staticmethod
    # utils solution -> contains most import parts of data preprocessing (cleaning, stopwords removal, tokenization, stemming, lemmatization)
    # can be applied on a column (df["test"].apply(lambda x: utils_preprocess_test(x....)))
    def utils_preprocess_text(text: object, flg_stemm: bool = False, flg_lemm: bool = True,
                              lst_stopwords: List[str] = None) -> object:

        ## cleaning (lowercase and remove punctuations and chars)
        text = re.sub(r'[^\w\s]', '', str(text).lower().strip())

        ## tokenize (string -> list)
        lst_text = text.split()

        ## remove stopwords (requires selection)
        if lst_stopwords is not None:
            lst_text = [word for word in lst_text if word not in lst_stopwords]  # if condition to remove stopwords

        ## stemming (convert the word into root word -> not as computing intensive as lemm but results may be worse)
        if flg_stemm:
            ps = nltk.stem.porter.PorterStemmer()
            lst_text = [ps.stem(word) for word in lst_text]

        if flg_lemm:
            lem = nltk.stem.wordnet.WordNetLemmatizer()
            lst_text = [lem.lemmatize(word) for word in lst_text]

        ## list -> string

        text = " ".join(lst_text)
        return text