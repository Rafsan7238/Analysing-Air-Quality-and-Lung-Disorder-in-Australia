import json
from elasticsearch8 import Elasticsearch

HIST_TWEET_INDEX_NAME = 'historic_tweet_sentiments'

def get_client():
    return Elasticsearch (
            'https://elasticsearch-master.elastic.svc.cluster.local:9200',
            verify_certs= False,
            basic_auth=('elastic', 'elastic')
        )

def insert_hist_tweets():
    try:
        es = get_client()

        if not es.indices.exists(index=HIST_TWEET_INDEX_NAME):
            return {'result': f'{HIST_TWEET_INDEX_NAME} index does not exist'}

        # Use count API to get the number of documents in the index
        document_count = es.count(index=HIST_TWEET_INDEX_NAME)['count']

        if(document_count > 0):
            return {'result': f'{HIST_TWEET_INDEX_NAME} already has data. Please delete before attempting re-insertion.'}

        with open('./data/historic_tweet_sentiments.json', 'r') as f:
            data = json.load(f)

        inserts = []
        for entry in data['entries']:
            insert = {
                'day': entry['day'],
                'month': entry['month'],
                'year': entry['year'],
                'total_sentiment': entry['total_sentiment'],
                'total_tweets': entry['total_tweets']
            }
            inserts.append(insert)
        
        es.bulk(index=HIST_TWEET_INDEX_NAME, body = inserts, refresh=True)

        return json.dumps({'result': 'Success'})
    except Exception as e:
        return json.dumps(e)

def create_indexes():
    try:    
        es = get_client()

        results = dict()

        if not es.indices.exists(index=HIST_TWEET_INDEX_NAME):
            '''Create historical tweets index'''
            body = {
                "settings": {
                    "index": {
                        "number_of_shards": 3,
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

            es.indices.create(
                index=HIST_TWEET_INDEX_NAME,
                body = body
            )
            results[HIST_TWEET_INDEX_NAME] = "Created"
        else:
            results[HIST_TWEET_INDEX_NAME] = 'Already Exists'

        # if not es.indices.exists(index={insert index name const here}}):
        #     body = {
        #         "settings": {
        #             "index": {
        #                 "number_of_shards": 3,
        #                 "number_of_replicas": 1
        #             }
        #         },
        #         "mappings": {
        #             "properties": {
        #                 'field1': {"type": "type def"}, #https://www.elastic.co/guide/en/elasticsearch/reference/8.13/mapping-types.html
        #                 ...
        #             }
        #         }
        #     }

        #     es.indices.create(
        #         index={insert index name const here},
        #         body = body
        #     )
        #     results[{insert index name const here}] = "Created"
        # else:
        #     results[{insert index name const here}] = 'Already Exists'
            

        return json.dumps(results)
    except Exception as e:
        return json.dumps(e)
