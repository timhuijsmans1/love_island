import json

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class preProcessing:

    def __init__(self, raw_data_path, output_path):
        self.raw_data_path = raw_data_path
        self.output_path = output_path
        print('fuck you guz')

    def pre_process_tweet(self, tweet_string):
        pass

    def file_reader_writer(self):
        print('fuck you laz')
        with open(self.raw_data_path, 'r') as f_in, open(self.output_path, 'w') as f_out:
            while True:
                print('hello')
                line = f_in.readline()
                if not line:
                    break
                else:
                    tweet = json.loads(line)
                    print(tweet.keys())

if __name__ == "_main_":
    INPUT_PATH = "../data/collected_data/filtered_search_results_06-30-2022_21;47;06.txt"
    OUTPUT_PATH = "../data/pre_processed_data/pre_processed.txt"
    pp = preProcessing(INPUT_PATH, OUTPUT_PATH)
    pp.file_reader_writer()
