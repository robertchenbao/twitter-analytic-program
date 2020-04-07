# This is the backend code for the entire United states.
# The goal is building a pipeline with all the functions in the project.

from src.bot_process import bot_app
from src.preprocess_tweet import data_clean
from src.location import location
import os
import pandas as pd
import pickle

pd.set_option('display.max_columns', None)


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


# Create a pipeline that applies the functions
def pipeline(data, clf):
    return (data
            .pipe(bot_app)
            .pipe(data_clean)
            .pipe(classification, clf=clf)
            .pipe(location)
            )


def print_pipeline(data, clf):
    print(data
          .pipe(data.drop_duplicates)
          .pipe(data.dropna)
          .pipe(bot_app)
          .pipe(data_clean)
          .pipe(classification, clf=clf)
          .pipe(location)
          )


if __name__ == '__main__':
    df = pd.read_csv("/Users/robertbao/Documents/2019_IF/data/tesla_lg.csv")
    print_pipeline(df, "whatever")
