from constants import HIST_TWEET_INDEX_NAME

def create_historic_tweets_index(es_client):
    if not es_client.indices.exists(index=HIST_TWEET_INDEX_NAME):
        '''Create historical tweets index'''
        body = {
            "settings": {
                "index": {
                    "number_of_shards": 1,
                    "number_of_replicas": 1
                }
            },
            "mappings": {
                "properties": {
                    'day': {"type": "integer"},
                    'month': {"type": "integer"},
                    'year': {"type": "integer"},
                    'total_sentiment': {"type" : "float"},
                    'total_tweets': {"type" : "integer"}
                }
            }
        }

        es_client.indices.create(
            index=HIST_TWEET_INDEX_NAME,
            body = body
        )
        return "Created"
    else:
        return 'Already Exists'