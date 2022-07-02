import os
import datetime
import json

from twarc import Twarc2, expansions
from itertools import islice

class TweetCollector():

    def __init__(self, 
                client, 
                query,
                start_datetime, 
                end_datetime,
                output_path,
        ):
        self.client = client
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.output_path = output_path
        self.query = query

    def execute_search(self, query):
        search_results = self.client.search_all(
                            query=query, 
                            start_time=self.start_datetime, 
                            end_time=self.end_datetime, 
                            max_results=100
        )

        return search_results

    def result_writer(self, search_results):
        count = 0
        with open(self.output_path, 'w+') as f: 
            for page in search_results:
                result = expansions.flatten(page)
                print(f'{len(result)} tweets found')
                for tweet in result:
                    tweet_date_text = {
                        'created_at': tweet['created_at'],
                        'text': tweet['text']
                    }
                    count += 1
                    f.write('%s\n' % json.dumps(tweet_date_text))
                    print(f'{count} tweets written to output file')
        return
    
    def execute(self):
        results = self.execute_search(self.query)
        self.result_writer(results)

if __name__ == "__main__":
    # global vars
    NOW = datetime.datetime.now().strftime("%m-%d-%Y_%H;%M;%S")
    OUTPUT_PATH = f"../data/collected_data/filtered_search_results_{NOW}.txt"
    BEARER = os.environ.get("BEARER")
    CLIENT = Twarc2(bearer_token=BEARER)
    START_TIME = datetime.datetime(2022, 6, 6, 0, 0, 0, 0, 
                    datetime.timezone.utc)
    END_TIME = datetime.datetime(2022, 6, 30, 0, 0, 0, 0, 
                    datetime.timezone.utc)
    QUERY = "#loveisland OR #LoveIsland OR Loveisland -is:retweet"

    # execute program
    tweet_collector = TweetCollector(
                        CLIENT,
                        QUERY,
                        START_TIME,
                        END_TIME,
                        OUTPUT_PATH
    )
    tweet_collector.execute()

