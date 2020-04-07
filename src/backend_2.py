# version 2 of the backend
# This is the backend code for the entire United states.
# The goal is building a pipeline with all the functions in the project.

import os
import pandas as pd
import pickle
import numpy as np
import re

pd.set_option('display.max_columns', None)


def select_model(file_name):
    DIR = os.path.dirname('/Users/robertbao/Documents/2019_IF/')
    MODEL_DIR = os.path.join(DIR, "models")
    return os.path.join(MODEL_DIR, file_name)


def select_data(file_name):
    DATA_DIR = os.path.dirname('/Users/robertbao/Documents/2019_SF/')
    HA = os.path.join(DATA_DIR, "data")
    return os.path.join(HA, file_name)


def bot_app(data):
    model = os.path.join(select_model('decision_bot_v2.pickle'))
    with open(model, 'rb') as file:
        dt = pickle.load(file)

    features = ['screen_name', 'description', 'verified', 'followers_count',
                'friends_count', 'statuses_count', 'listed_count']
    bag_of_words_bot = r'bot|b0t|cannabis|tweet me|mishear|follow me|updates every|gorilla|forget'
    data['screen_name'] = data.screen_name.str.contains(bag_of_words_bot, case=False, na=False)

    data['description'] = data.description.str.contains(bag_of_words_bot, case=False, na=False)
    df = data.reindex(
        columns=['date', 'text', 'location', 'listed_count', 'friends_count', 'followers_count',
                 'verified', 'name', 'description', 'screen_name', 'statuses_count', 'bot'])

    df['bot'] = df['bot'] = dt.predict(df[features])

    # Delete bots
    df['bot'].replace(1, np.nan, inplace=True)

    df = df[pd.notnull(df['bot'])]
    df.drop(['description', 'verified', 'followers_count',
             'friends_count', 'statuses_count', 'listed_count'], axis=1)
    return df


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


def singleton(cls):
    # Singleton pattern to avoid loading class multiple times
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


@singleton
class TweetUSStateGeocoder:

    def __init__(self,
                 geocode_filename='/Users/robertbao/Documents/2019_SF/train/us_geocode.csv',
                 us_places_to_state_mapping_filename='/Users/robertbao/Documents/2019_SF/train/us.states.json'):
        coordinates, self.locations = self.extract_coordinates_and_locations(rel_path(geocode_filename))
        self.tree = KDTree(coordinates)

        self.us_places_to_state_map = self.load_us_places_to_state_mapping_file(
            rel_path(us_places_to_state_mapping_filename))

        # keep only alpha, space, period and comma
        self.keep_alpha_p = re.compile(r'[^a-zA-Z\s\.,]')

        self.geomap = {}

    def load_us_places_to_state_mapping_file(self, local_filename):
        if os.path.exists(local_filename):
            with open(local_filename, 'r') as rf:
                return json.load(rf)
        else:
            print("missing us_places_to_state_mapping file: [%s]" % (local_filename))
            sys.exit(1)

    def extract_coordinates_and_locations(self, local_filename):
        """Extract geocode data from zip
        """
        if os.path.exists(local_filename):
            # open compact CSV
            rows = csv.reader(codecs.getreader('utf-8')(open(local_filename, 'rb')))
        else:
            print("missing geocode file: [%s]" % (local_filename))
            sys.exit(1)

        # load a list of known coordinates and corresponding locations
        coordinates, locations = [], []
        for latitude, longitude, state, place in rows:
            coordinates.append((latitude, longitude))
            locations.append(dict(state=state, city=place, latitude=latitude, longitude=longitude))
        return coordinates, locations

    def query_coordinates(self, coordinates):
        """Find closest match to this list of coordinates
        """
        try:
            distances, indices = self.tree.query(coordinates, k=1)  # , distance_upper_bound=0.1
        except ValueError as e:
            print('Unable to parse coordinates:', coordinates)
            raise e
        else:
            results = []
            for distance, index in zip(distances, indices):
                if not isinf(distance):
                    result = self.locations[index]
                    result['distance'] = distance

                    results.append(result)

            return results

    def distance(self, coordinate_1, coordinate_2):

        R = 6373.0

        lat1, lon1 = coordinate_1
        lat2, lon2 = coordinate_2

        lat1 = radians(float(lat1))
        lon1 = radians(float(lon1))
        lat2 = radians(float(lat2))
        lon2 = radians(float(lon2))

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = (sin(dlat / 2)) ** 2 + cos(lat1) * cos(lat2) * (sin(dlon / 2)) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c

        return distance * 0.621371

    def get_by_coordinate(self, coordinate):
        """Search for closest known location to this coordinate
        """
        tug = TweetUSStateGeocoder()
        results = tug.query_coordinates([coordinate])
        return results[0] if results else None

    def search_by_coordinates(self, coordinates):
        """Search for closest known locations to these coordinates
        """
        tug = TweetUSStateGeocoder()
        return tug.query_coordinates(coordinates)

    def get_state(self, address):

        address = address.strip()

        state = None

        if address not in self.geomap:

            p = re.findall(r'.*?([-+]?\d*\.\d+),([-+]?\d*\.\d+)', address)

            if len(p) > 0:
                coordinate = p.pop()
                nearest = self.get_by_coordinate(coordinate)

                if nearest:
                    c2 = nearest['latitude'], nearest['longitude']
                    d = self.distance(coordinate, c2)
                    if (d < 20):  # less than 100 miles
                        state = nearest['state']
                        self.geomap[address] = state

            else:

                address_ = address.replace(', ', ',')
                address_ = re.sub(self.keep_alpha_p, '', address_)
                address_ = address_.lower()

                for i in range(3):
                    # state = us_places_to_state_map[address] if address in us_places_to_state_map else None
                    if address_ in self.us_places_to_state_map['%s' % i]:
                        state = self.us_places_to_state_map['%s' % i][address_]
                        self.geomap[address] = state
                        break
                        # print('[%s]->%s'%(address, state))
        else:
            state = self.geomap[address]

        return state


def rel_path(filename):
    """Return the path of this filename relative to the current script
    """
    return os.path.join(os.getcwd(), os.path.dirname(__file__), filename)


def location(data):
    tug = TweetUSStateGeocoder()
    data['state_name'] = data['location'].apply(lambda x: tug.get_state(str(x)))
    # df['state_name'].apply(lambda x: states.lookup(str(x)))  # Get the full state name here.
    data = data[pd.notnull(data['state_name'])]
    return data


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
