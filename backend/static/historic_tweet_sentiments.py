import json, os
from constants import HIST_TWEET_INDEX_NAME

def insert_hist_tweets(es, bulker):        
    if not es.indices.exists(index=HIST_TWEET_INDEX_NAME):
        return f'{HIST_TWEET_INDEX_NAME} index does not exist'

    # Use count API to get the number of documents in the index
    document_count = es.count(index=HIST_TWEET_INDEX_NAME)['count']

    if(document_count > 0):
        return f'{HIST_TWEET_INDEX_NAME} already has data. Please delete before attempting re-insertion.'

    try:
        with open('../userfunc/deployarchive/data/historic_tweet_sentiments.json', 'r') as f:
            data = json.load(f)
        inserts = []
        for entry in data['entries']:
            insert = {
                'create': {
                    'day': entry['day'],
                    'month': entry['month'],
                    'year': entry['year'],
                    'total_sentiment': entry['total_sentiment'],
                    'total_tweets': entry['total_tweets']
                }
            }
            inserts.append(insert)
        
        bulker.bulk(es, inserts, index=HIST_TWEET_INDEX_NAME)
    except Exception as e:
        return f'{e}'
    return 'success'