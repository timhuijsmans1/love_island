import json
import datetime
import re
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()

def extract_keys_values(nested_data_dict):
    dates = []
    tweets = []
    for key, value in nested_data_dict.items():
        for date, tweet in value.items():
            dates.append(date)
            tweets.append(tweet)

    return dates, tweets


def create_dataframe(dates, tweets):
    tweet_df = pd.DataFrame()
    tweet_df["Date"] = dates
    tweet_df["Tweet"] = tweets
    tweet_df.to_csv("../data/collected_data/tweet_df.csv")
    return tweet_df

def create_data_dictionaries(filepath):
    data_dict = {}
    i = 0
    with open(filepath) as f:
        while True:
            line = f.readline()
            if not line:
                break
            tweet = json.loads(line)
            text = tweet["text"]
            split_text = text.split(" ")
            split_date = tweet["created_at"].split("T")
            date = datetime.date.fromisoformat(split_date[0])
            data_dict[i] = {}
            data_dict[i][date] = text
            i += 1
            print("Read " + str(i) + " tweets")
    return data_dict


def extract_statistics(df):
    plt.figure(figsize=(16, 10))
    sns.countplot(x='Date', data=df)
    plt.xlabel("Date", fontsize=15)
    plt.ylabel("Count", fontsize=15)
    plt.title("Number of #loveisland tweets per day", fontsize=20)
    plt.xticks(rotation=45)
    plt.show()


def extract_date_from_df(date, df):
    new_df = df.loc[df['Date'] == date]
    return new_df

def word_cloud_pre_process(df):
    df['pre_process_tweet'] = df['Tweet'].map(lambda x:
                                              re.sub("RT", "", x))
    df["pre_process_tweet"] = df['pre_process_tweet'].map(lambda x:
                                                          re.sub("@\S+", "", x))
    df["pre_process_tweet"] = df["pre_process_tweet"].map(lambda x: x.lower())

    df["pre_process_tweet"] = df["pre_process_tweet"].map(lambda x: re.sub(
        "https\S+", "", x))
    #  joining all twets together

    long_string = ','.join(df["pre_process_tweet"].values)
    return long_string


def visualise_word_cloud(longstring, word_cloud, date):
    word_cloud.generate(longstring)
    plt.figure(figsize=(14, 12))
    plt.imshow(word_cloud)
    plt.title("Wordcloud for " + date, fontsize=20)
    plt.show()


def prepare_stopwords(stopwords):
    contestants = ['tasha', 'gemma', 'danica', 'ekin-su', 'ekin', 'antigoni', 'indiyah', 'paige',
                   'davide', 'charlie', 'luca', 'jacques', 'andrew', 'dami', 'jay', 'su',
                   'ikenna', 'amber']
    love_island_variants = ['love', 'island', 'loveisland', 'loveislanduk']
    apostrophes = ['s', 't', 'm']

    for contestant in contestants:
        stopwords.add(contestant)
    for term in love_island_variants:
        stopwords.add(term)
    for apostrophe in apostrophes:
        stopwords.add(apostrophe)
    stopwords = set(stopwords)
    return stopwords


def extract_contestant_appearances(df, contestants):
    dates = df.Date.unique()
    contestant_mentions_dict = {}
    for contestant in contestants:
        contestant_mentions_dict[contestant] = {}

    for date in dates:
        date_df = extract_date_from_df(date, df)
        for contestant in contestants:
            try:
                contestant_mentions_dict[contestant][date] = date_df["Tweet"].str.contains(contestant).value_counts()[True]
            except KeyError as e:
                contestant_mentions_dict[contestant][date] = 0

    return contestant_mentions_dict


def plot_contestant_appearances(contestant_mentions_dict, list_of_contestants):

    plt.figure(figsize=(16, 10))
    for contestant, mentions_dict in contestant_mentions_dict.items():
        if contestant in list_of_contestants:
            plt.plot(list(mentions_dict.keys()), list(mentions_dict.values()), label=contestant)
    plt.xlabel("Date", fontsize=14)
    plt.ylabel("Appearences", fontsize=14)
    plt.title("Count of appearances of contestant name in Tweets", fontsize=20)
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()



df = pd.read_csv("../data/collected_data/tweet_df.csv")

chosen_date = '2022-06-28'
second_date = '2022-06-08'
extract_statistics(df)
date_df = extract_date_from_df(second_date, df)
longstring = word_cloud_pre_process(date_df)
stopwords = prepare_stopwords(STOPWORDS)
#
# word_cloud = WordCloud(width=800, height=800, max_words=5000, background_color='white',
#                        stopwords=stopwords, contour_color='steelblue',
#                        collocations=False)
#
# visualise_word_cloud(longstring, word_cloud, chosen_date)


contestants = ['tasha', 'gemma', 'danica', 'ekin-su', 'antigoni', 'indiyah', 'paige',
               'davide', 'charlie', 'luca', 'jacques', 'andrew', 'dami', 'jay', 'ikenna', 'amber']
contestant_mentions_dict = extract_contestant_appearances(df, contestants)

boys_names = ['davide', 'charlie', 'luca', 'jacques', 'dami', 'jay']
girl_names = ['tasha', 'gemma', 'danica', 'ekin-su', 'antigoni', 'indiyah', 'paige']
couples_combinations = ['davide', 'ekin-su', 'luca', 'gemma', 'paige', 'jacques', 'tasha', 'andrew']
plot_contestant_appearances(contestant_mentions_dict, boys_names)
plot_contestant_appearances(contestant_mentions_dict, girl_names)
plot_contestant_appearances(contestant_mentions_dict, couples_combinations)

