# This program pre-process the tweets with Regular Expressions (Regex).
# Currently, it can not find stop words.
# Version: 1.0. Basic functions is fine.
# Version: 2.0. Added fast stop words removal.

import re
import pandas as pd
import os
from nltk.corpus import stopwords

pd.set_option('display.max_columns', None)


def select_data(file_name):
    DATA_DIR = os.path.dirname('/Users/robertbao/Documents/2019_SF/')
    HA = os.path.join(DATA_DIR, "data")
    return os.path.join(HA, file_name)


def preprocess_word(word):
    word = word.strip('\'"?!,.():;')  # Remove punctuation
    # Convert more than 2 letter repetitions to 2 letter
    # funnnnny --> funny
    word = re.sub(r'(.)\1+', r'\1\1', word)
    # Remove - & '
    word = re.sub(r'(-|\')', '', word)
    return word


def is_valid_word(word):
    # Check if word begins with an alphabet
    return re.search(r'^[a-zA-Z][a-z0-9A-Z\._]*$', word) is not None


def preprocess_tweet(tweet):
    processed_tweet = []
    # Convert to lower case
    tweet = tweet.lower()
    # Replaces URLs with the word URL
    # tweet = re.sub(r'((www\.[\S]+)|(https?://[\S]+))', ' URL ', tweet)
    tweet = re.sub(r'((www\.[\S]+)|(https?://[\S]+))', '', tweet)
    # Replace @handle with the word USER_MENTION
    # tweet = re.sub(r'@[\S]+', 'USER_MENTION', tweet)
    tweet = re.sub(r'@[\S]+', '', tweet)
    # Replaces #hashtag with hashtag
    tweet = re.sub(r'#(\S+)', r' \1 ', tweet)

    # # Remove RT (retweet)
    # tweet = re.sub(r'\brt\b', '', tweet)

    # Replace 2+ dots with space
    tweet = re.sub(r'\.{2,}', ' ', tweet)
    # Strip space, " and ' from tweet
    tweet = tweet.strip(' "\'')
    # Replace multiple spaces with a single space
    tweet = re.sub(r'\s+', ' ', tweet)
    words = tweet.split()

    for word in words:
        word = preprocess_word(word)
        if is_valid_word(word):
            processed_tweet.append(word)

    return ' '.join(processed_tweet)


# This method pre-process the tweets
def data_clean(input_data):
    # df = pd.DataFrame(input_data)
    input_data['text'] = input_data['text'].apply(preprocess_tweet)
    return input_data


if __name__ == "__main__":
    df = pd.read_csv(os.path.join(select_data('raw/tesla_00d.csv')))
    df['text'] = df['text'].apply(preprocess_tweet)
    # print(df['name'].tail(100))
    df.to_csv("result/tesla_00d_1.csv", index=False)
