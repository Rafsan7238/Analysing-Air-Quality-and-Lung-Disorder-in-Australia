import json

from constants import ASTHMA_BY_REGION_INDEX_NAME, HIST_TWEET_INDEX_NAME
from elastic_client_provider import get_bulker, get_client
from index_creation.create_asthma_by_region_index import create_asthma_by_region_index
from index_creation.create_historic_tweets_index import create_historic_tweets_index
from static.historic_tweet_sentiments import insert_hist_tweets
from static.asthma_by_region import insert_region_asthma

def insert_hist_tweets_endpoint():
    try:
        es = get_client()
        bulker = get_bulker()

        res = insert_hist_tweets(es, bulker)

        return json.dumps({'result': res})
    except Exception as e:
        return json.dumps(e)
    
def insert_region_asthma_endpoint():
    try:
        es = get_client()
        bulker = get_bulker()

        res = insert_region_asthma(es, bulker)

        return json.dumps({'result': res})
    except Exception as e:
        return json.dumps(e)

def create_indexes_endpoint():
    try:    
        es = get_client()

        results = dict()
        results[HIST_TWEET_INDEX_NAME] = create_historic_tweets_index(es)
        results[ASTHMA_BY_REGION_INDEX_NAME] = create_asthma_by_region_index(es)
       
        return json.dumps(results)
    except Exception as e:
        return json.dumps(e)
