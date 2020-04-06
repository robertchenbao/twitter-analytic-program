import pandas as pd
import pickle
import numpy as np
import os

pd.set_option('display.max_columns', None)


def select_model(file_name):
    DIR = os.path.dirname('/Users/robertbao/Documents/2019_IF/')
    MODEL_DIR = os.path.join(DIR, "models")
    return os.path.join(MODEL_DIR, file_name)


def select_data(file_name):
    DATA_DIR = os.path.dirname('/Users/robertbao/Documents/2019_SF/')
    HA = os.path.join(DATA_DIR, "data")
    return os.path.join(HA, file_name)


def feature_process(my_data):
    bag_of_words_bot = r'bot|b0t|cannabis|tweet me|mishear|follow me|updates every|gorilla|forget'
    my_data['screen_name'] = my_data.screen_name.str.contains(bag_of_words_bot, case=False, na=False)
    # my_data['name'] = my_data.name.str.contains(bag_of_words_bot, case=False, na=False)

    my_data['description'] = my_data.description.str.contains(bag_of_words_bot, case=False, na=False)
    # my_data['status'] = my_data.status.str.contains(bag_of_words_bot, case=False, na=False)
    return my_data


def bot_app(data):
    model = os.path.join(select_model('decision_bot_v2.pickle'))
    with open(model, 'rb') as file:
        dt = pickle.load(file)

    features = ['screen_name', 'description', 'verified', 'followers_count',
                'friends_count', 'statuses_count', 'listed_count']

    df = feature_process(data)
    df = df.reindex(
        columns=['date', 'text', 'location', 'listed_count', 'friends_count', 'followers_count',
                 'verified', 'name', 'description', 'screen_name', 'statuses_count', 'bot'])

    df['bot'] = df['bot'] = dt.predict(df[features])

    # Delete bots
    df['bot'].replace(1, np.nan, inplace=True)

    df = df[pd.notnull(df['bot'])]
    # df.drop(['screen_name', 'name', 'description', 'verified', 'followers_count',
    #              'friends_count', 'statuses_count', 'listed_count'], axis=1)
    df.drop(['description', 'verified', 'followers_count',
             'friends_count', 'statuses_count', 'listed_count'], axis=1)
    return df


if __name__ == "__main__":
    pd.set_option('display.max_columns', None)
    file = 'raw/tesla_00d.csv'
    df = pd.read_csv(os.path.join(select_data(file)))
    bot_df = bot_app(data=df)
    # bot_df.to_csv(select_data('result/tesla_00d_nobot.csv'), index=False)
    print(bot_df.head(20))
