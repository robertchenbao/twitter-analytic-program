from gender_predictor import GenderPredictor

from src.bot_process import bot_app
from src.preprocess_tweet import data_clean
# from src.classifier import classification

import pandas as pd
from datetime import datetime
# from src.utils import select_data, select_raw_data, select_model
from gender_predictor import GenderPredictor
import os
import sys
import pickle


def select_model(file_name):
    DIR = os.path.dirname('/Users/robertbao/Documents/2019_IF/')
    MODEL_DIR = os.path.join(DIR, "models")
    return os.path.join(MODEL_DIR, file_name)


def select_data(file_name):
    DATA_DIR = os.path.dirname('/Users/robertbao/Documents/2019_SF/')
    HA = os.path.join(DATA_DIR, "data")
    return os.path.join(HA, file_name)


def classification(df, clf):
    if clf == 'sgd':
        model_choice = select_model('tf_idf_SGD.pickle')
    elif clf == 'mnb':
        model_choice = select_model('tf_idf_MNB.pickle')
    elif clf == 'bnb':
        model_choice = select_model('tf_idf_BNB.pickle')
    else:
        model_choice = select_model('tf_idf_Logistic.pickle')

    with open(select_model('tf_idf.pickle'), 'rb') as file:
        vec = pickle.load(file)
    with open(model_choice, 'rb') as file:
        clif = pickle.load(file)
    X_new = vec.transform(df['text'])
    df['sentiment'] = clif.predict(X_new)
    return df


def gender_clf(data):
    with open(select_model('gender-classifier-2.pickle'), 'rb') as file:
        gp = pickle.load(file)
    data.loc[df['name'].astype(str).str.split().str.len() == 2, 'first name'] = \
        data['name'].astype(str).str.split().str[0]
    data = data.dropna()
    data['gender'] = data['first name'].astype(pd.Series).apply(lambda x: gp.classify(x))
    quantity_df = df.groupby('gender').size().reset_index(name='quantity')
    return quantity_df


def report(df):
    gp = GenderPredictor()
    gp.train_and_test()
    df.loc[df['name'].astype(str).str.split().str.len() == 2, 'first name'] = df['name'].astype(str).str.split().str[0]
    df = df.dropna()
    df['gender'] = df['first name'].astype(str).apply(lambda x: gp.classify(x))
    quantity_df = df.groupby('gender').size().reset_index(name='quantity')
    print(type(quantity_df))
    print(quantity_df)


if __name__ == '__main__':
    fn = "/Users/robertbao/Downloads/tesla_20000.csv"
    startTime = datetime.now()
    df = pd.read_csv(fn, encoding='UTF-8')
    df = df.drop_duplicates()
    df = df.dropna()

    df = (df
          .pipe(bot_app)
          .pipe(data_clean)
          .pipe(classification, clf=select_model('tf_idf_Logistic.pickle'))
          .pipe(gender_clf)
          # .pipe(report)
          )
    print(datetime.now() - startTime)
