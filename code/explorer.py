import json

with open("../data/collected_data/filtered_search_results_06-30-2022_21;47;06.txt") as f:
    while True:
        line = f.readline()
        if not line:
            break
        tweet = json.loads(line)
        date = tweet["created_at"]
        print(date)