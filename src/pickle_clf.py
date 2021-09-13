# This program makes pickle files for all sci-kit learn classifiers.

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB, BernoulliNB, GaussianNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.metrics import roc_auc_score
from datetime import datetime
import pickle
import os
from utils import select_train

startTime = datetime.now()

training_data_set = select_train('stanford_training_data.csv')

df = pd.read_csv(training_data_set, encoding='UTF-8')

TfidfVectorizer = TfidfVectorizer(
    use_idf=True,
    strip_accents='ascii',
    tokenizer=None,
)

y = df['sentiment']
X = TfidfVectorizer.fit_transform(df['text'])

# Test Train Split as usual
X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    train_size=0.9,
                                                    random_state=42)

logr_clf = LogisticRegression()
logr_clf.fit(X_train, y_train)
print('The accuracy of LogisticRegression with TfidfVectorizer is:')
print(roc_auc_score(
    y_test,
    logr_clf.predict_proba(X_test)[:, 1]))  # test our model's accuracy
print('---------------------------------------------')

sgd_clf = SGDClassifier(loss='log')
sgd_clf.fit(X_train, y_train)
print('The accuracy of SGDClassifier with TfidfVectorizer is:')
print(roc_auc_score(
    y_test,
    sgd_clf.predict_proba(X_test)[:, 1]))  # test our model's accuracy
print('---------------------------------------------')

# we will train a Multinomial NB classifier
mnb_clf = MultinomialNB()
mnb_clf.fit(X_train, y_train)
print('The accuracy of MultinomialNB with TfidfVectorizer is:')
print(roc_auc_score(
    y_test,
    mnb_clf.predict_proba(X_test)[:, 1]))  # test our model's accuracy
print('---------------------------------------------')

bnb_clf = BernoulliNB()
bnb_clf.fit(X_train, y_train)
print('The accuracy of BernoulliNB with TfidfVectorizer is:')
print(roc_auc_score(
    y_test,
    bnb_clf.predict_proba(X_test)[:, 1]))  # test our model's accuracy
print('---------------------------------------------')

with open('tf_idf.pickle', 'wb') as f:
    pickle.dump(TfidfVectorizer, f)

with open('tf_idf_Logistic.pickle', 'wb') as f:
    pickle.dump(logr_clf, f)

with open('tf_idf_SGD.pickle', 'wb') as f:
    pickle.dump(sgd_clf, f)

with open('tf_idf_MNB.pickle', 'wb') as f:
    pickle.dump(mnb_clf, f)

with open('tf_idf_BNB.pickle', 'wb') as f:
    pickle.dump(bnb_clf, f)

print(datetime.now() - startTime)
