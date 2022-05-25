from nltk.tokenize import sent_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import pandas as pd
from string import punctuation
import re
from collections import Counter
import nltk
nltk.download(['punkt', 'stopwords'])


class FinancialSentiment:
    def __init__(self, data_path: str) -> None:
        self.data = pd.read_csv(data_path)
        self.x = self.data['sentence'].to_numpy()
        self.y = self.data['sentiment'].to_numpy()

        self.__loading()

    # Loading |>
    def __loading(self):
        # Preprocessing
        pre_x = self.preprocessing(self.x)

        # Count Vector
        self.count_vect = CountVectorizer()
        self.count_vect.fit(pre_x)
        count_x = self.count_vect.transform(pre_x)
        print(f"Count Vector...")

        # Tfidf
        self.tfidf = TfidfTransformer()
        self.tfidf.fit(count_x)
        tfidf_x = self.tfidf.transform(count_x)
        print(f"Tfidf...")

        # Train LogisticRegression
        self.model = LogisticRegression(verbose=0, max_iter=200)
        self.model.fit(tfidf_x, self.y)
        print(f"Successful!")

    # Preprocessing |>
    def preprocessing(self, sentences: list):
        # lowercase
        sentences = [sentence.lower() for sentence in sentences]

        # clear puncuation
        table = str.maketrans('', '', punctuation)
        sentences = [sentence.translate(table) for sentence in sentences]
        sentences = [re.sub(r'\d+', 'num', sentence) for sentence in sentences]

        # clear stopwords
        stopword = set(stopwords.words(
            'english') + ['\x03', '.com', 'cryptograph', 'ambcrypto', 'u.today', 'coingape', 'the dialy hodl'])
        sentences = [[word for word in sentence.split() if word not in stopword]
                     for sentence in sentences]

        # stemming
        stemmer = PorterStemmer()
        sentences = [' '.join([stemmer.stem(word) for word in sentence])
                     for sentence in sentences]
        return sentences

    # Transform |>
    def transform(self, sentences: list):
        count_x = self.count_vect.transform(sentences)
        tfidf_x = self.tfidf.transform(count_x)
        return tfidf_x

    # Preprocessing & Transform |>
    def preprocessing_transform(self, sentences: list):
        return self.transform(self.preprocessing(sentences))

    def pre_predict_sentence(self, sentence: str):
        tfidf_x = self.preprocessing_transform([sentence])
        pred = self.model.predict(tfidf_x)[0]
        return pred

    def pre_predict_sentences(self, sentences: list):
        tfidf_x = self.preprocessing_transform(sentences)
        pred = self.model.predict(tfidf_x)
        return pred

    def pre_predict_article(self, article: str):
        sentences = sent_tokenize(article)
        tfidf_x = self.preprocessing_transform(sentences)
        pred = self.model.predict(tfidf_x)
        return pred

    # Predict |>
    def predict(self, article: str):
        sentences = sent_tokenize(article)
        tfidf_x = self.preprocessing_transform(sentences)
        pred = self.model.predict(tfidf_x)
        scores = Counter(pred)
        return self.majority_score(scores)

    # Majority Score |>
    def majority_score(self, scores: Counter):
        sentiment = ''
        sent_score = 0
        size = 0

        for key in scores.keys():
            size += scores[key]
            if sent_score < scores[key]:
                sent_score = scores[key]
                sentiment = key

        polarity = ((1 * scores['positive']) +
                    (-1 * scores['negative'])) / size
        return sentiment, polarity
