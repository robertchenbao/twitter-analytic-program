# This program uses the given training data to find Twitter bots in the dataset.
# Then, it exports the model into a pickle file.

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle
import os

from src.utils import select_train

# training_data = pd.read_csv(os.path.join(TRAIN_DIR, ))

data = select_train('training_data_2_csv_UTF.csv')
training_data = pd.read_csv(data)
training_data['listed_count_binary'] = (training_data.listed_count > 20000) == False
bag_of_words_bot = r'bot|b0t|cannabis|tweet me|mishear|follow me|updates every|gorilla|forget'

bots = training_data[training_data.bot == 1]

bots['screen_name_binary'] = (bots.screen_name.str.contains("bot", case=False) == True)
bots['location_binary'] = (bots.location.isnull())
bots['verified_binary'] = (bots.verified is False)


def feature_process(my_data):
    my_data['screen_name'] = my_data.screen_name.str.contains(bag_of_words_bot, case=False, na=False)
    my_data['description'] = my_data.description.str.contains(bag_of_words_bot, case=False, na=False)
    # my_data['status'] = my_data.status.str.contains(bag_of_words_bot, case=False, na=False)
    return my_data


features = ['screen_name', 'description', 'verified', 'followers_count',
            'friends_count', 'statuses_count', 'listed_count', 'bot']

feature_process(training_data)
X = training_data[features].iloc[:, :-1]
y = training_data[features].iloc[:, -1]

dt = DecisionTreeClassifier(criterion='entropy', min_samples_leaf=50, min_samples_split=10)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)
dt = dt.fit(X_train, y_train)
y_pred_train = dt.predict(X_train)
y_pred_test = dt.predict(X_test)
print("Training Accuracy: %.5f" % accuracy_score(y_train, y_pred_train))
print("Test Accuracy: %.5f" % accuracy_score(y_test, y_pred_test))

with open('decision_bot_v2.pickle', 'wb') as f:
    pickle.dump(dt, f)

# if __name__ == "__main__":
#     # Next, I will apply this algorithm to my data. It will make a file with no bots.
#     filename = '/Users/robertbao/Documents/2019 Science Fair/data/raw/tesla_week_1.csv'
#     df = pd.read_csv(filename, error_bad_lines=False, encoding='UTF-8')
#     print(df.head())
#     target = feature_process(df)
#     target = target.reindex(
#         columns=['date', 'text', 'location', 'entities', 'listed_count', 'friends_count', 'followers_count',
#                  'verified', 'name', 'description', 'screen_name', 'statuses_count', 'bot'])
#     target['bot'] = dt.predict(target[features].iloc[:, :-1])
#     print("I am line 1--------------------------")
#
#     print("In the ai data file, there are ", target['bot'].sum(), "bots")
#     print('I am line 2--------------------------')
