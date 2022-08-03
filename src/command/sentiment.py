import nltk
nltk.download(['stopwords', 'punkt'])

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize
from string import punctuation
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score, ShuffleSplit
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
from collections import Counter
import os

from src.util.logging import log_info

_DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "data.csv"))

class Sentiment:
    def __init__(self):
        log_info("loading sentiment model...")
        self._load()
    
    def preprocessing(self, data: list[str]):
        # transform into lowercase
        data = [item.lower() for item in data]
        # clear punctuation
        table = str.maketrans('', '', punctuation)
        data = [item.translate(table) for item in data]
        data = [re.sub(r'\d+', 'num', item) for item in data]
        # clear stopword
        stopword = set(stopwords.words('english') + ['\x03', '.com', 'cryptograph', 'ambcrypto', 'u.today', 'coingape', 'the dialy hodl'])
        data = [[word for word in item.split() if word not in stopword] for item in data]
        # stemming
        stemmer = PorterStemmer()
        data = [' '.join([stemmer.stem(word) for word in item]) for item in data]
        return np.array(data)
    
    def _load(self):
        log_info("sentiment model (preprocessing)...")
        df = pd.read_csv(_DATA_PATH)
        x = df['sentence'].to_numpy()
        y = df['sentiment'].to_numpy()
        x = self.preprocessing(x)

        log_info("sentiment model (validating)...")
        self.model = Pipeline([
            ('vect', TfidfVectorizer()),
            ('clf', LogisticRegression(max_iter=2000, solver='liblinear', C=2.154434690031882))
        ])
        cv = ShuffleSplit(n_splits=10, test_size=.2, random_state=42)
        scores = cross_val_score(self.model, x, y, cv=cv, scoring='accuracy')
        scores = list(scores)
        cv_ind = scores.index(max(scores))

        log_info("sentiment model (training)...")
        train, test = list(cv.split(x))[cv_ind]
        x_train, x_test, y_train, y_test = x[train], x[test], y[train], y[test]
        self.model.fit(x_train, y_train)
        y_pred = self.model.predict(x_test)
        log_info("sentiment model (done)...")
        log_info(f"Accuracy Score Of Sentiment Model: {accuracy_score(y_test, y_pred):.4f}")
        
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
        return sentiment, round(polarity, 4)
    
    def article_predict(self, data: str):
        sentences = sent_tokenize(data)
        prep = self.preprocessing(sentences)
        predicted = self.model.predict(prep)
        scores = Counter(predicted)
        return self.majority_score(scores)

