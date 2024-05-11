import json

from backend.index_creation.create_mortality_persons import create_mortality_persons_index
from index_creation.create_air_quality_hourly_avg import create_air_quality_hourly_average
from index_creation.create_census_g21b import create_census_g21b
from index_creation.create_mortality_females import create_mortality_females_index
from index_creation.create_mortality_males import create_mortality_males_index
from index_creation.create_rainfall_adelaide import create_rainfall_adelaide_index
from index_creation.create_rainfall_brisbane import create_rainfall_brisbane_index
from index_creation.create_rainfall_canberra import create_rainfall_canberra_index
from index_creation.create_rainfall_darwin import create_rainfall_darwin_index
from index_creation.create_rainfall_melbourne import create_rainfall_melbourne_index
from index_creation.create_rainfall_perth import create_rainfall_perth_index
from index_creation.create_rainfall_sydney import create_rainfall_sydney_index
from index_creation.create_rainfall_tasmania import create_rainfall_tasmania_index
from index_creation.create_temperature_adelaide import create_temperature_adelaide_index
from index_creation.create_temperature_brisbane import create_temperature_brisbane_index
from index_creation.create_temperature_canberra import create_temperature_canberra_index
from index_creation.create_temperature_darwin import create_temperature_darwin_index
from index_creation.create_temperature_melbourne import create_temperature_melbourne_index
from index_creation.create_temperature_perth import create_temperature_perth_index
from index_creation.create_temperature_sydney import create_temperature_sydney_index
from index_creation.create_temperature_tasmania import create_temperature_tasmania_index
from constants import *
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
        results[AIR_QUALITY_HOURLY_AVG] = create_air_quality_hourly_average(es)   
        results[ASTHMA_BY_REGION_INDEX_NAME] = create_asthma_by_region_index(es)   
        results[CENSUS_G21B] = create_census_g21b(es)   
        results[HIST_TWEET_INDEX_NAME] = create_historic_tweets_index(es)
        results[MORTALITY_FEMALES] = create_mortality_females_index(es)   
        results[MORTALITY_MALES] = create_mortality_males_index(es)   
        results[MORTALITY_PERSONS] = create_mortality_persons_index(es)   

        results[RAINFALL_ADELAIDE] = create_rainfall_adelaide_index(es)   
        results[RAINFALL_BRISBANE] = create_rainfall_brisbane_index(es)   
        results[RAINFALL_CANBERRA] = create_rainfall_canberra_index(es)   
        results[RAINFALL_DARWIN] = create_rainfall_darwin_index(es)   
        results[RAINFALL_MELBOURNE] = create_rainfall_melbourne_index(es)   
        results[RAINFALL_PERTH] = create_rainfall_perth_index(es)   
        results[RAINFALL_SYDNEY] = create_rainfall_sydney_index(es)   
        results[RAINFALL_TASMANIA] = create_rainfall_tasmania_index(es)   

        results[TEMPERATURE_ADELAIDE] = create_temperature_adelaide_index(es)   
        results[TEMPERATURE_BRISBANE] = create_temperature_brisbane_index(es)   
        results[TEMPERATURE_CANBERRA] = create_temperature_canberra_index(es)   
        results[TEMPERATURE_DARWIN] = create_temperature_darwin_index(es)   
        results[TEMPERATURE_MELBOURNE] = create_temperature_melbourne_index(es)   
        results[TEMPERATURE_PERTH] = create_temperature_perth_index(es)   
        results[TEMPERATURE_SYDNEY] = create_temperature_sydney_index(es)   
        results[TEMPERATURE_TASMANIA] = create_temperature_tasmania_index(es)   
    
        return json.dumps(results)
    except Exception as e:
        return json.dumps(e)
