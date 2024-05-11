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


### ^^ insert x endpoint()

###############################
# air quality vs lung disease 

def get_air_quality_hourly_avg():
    # get 2022_All_sites_air_quality_hourly_avg, 
    # select parameter_names = ['CO', 'PM10', 'PM2.5', 'O3', 'SO2']
    try: 
        es = get_client()
        bulker = get_bulker()


    except Exception as e:
        return json.dumps(e)
    

    pass


def get_lung_cancer_join():
    # get all lung cancer data aihw_cimar_mortality_persons_gccsa_2009
    # merge with census_by_cob_data abs_2021census_g21a_aust_gccsa
    # join on inner, ['gccsa_code', 'gccsa_name']
    pass 

def get_gender_lung_cancer():
    # get male lung cancer 
    # get female lung cancer
    # join on gccsa_name
    # columns 'gccsa_name', 'Lung cancer rate per 100k'
    # add suffix (male, female)
    pass


def get_census_by_inc_emp():
    # return census data 
    pass

#############################
# weather vs sentiment 

def get_historic_tweet_sentiment():
    # return hiostoric tweet sentiment
    pass 

def get_rainfall_data():
    # get all cities, 
    # group by month
    # get mean
    pass 

def get_temperature_data():
    # get all cities, 
    # group by month
    # get mean
    pass 
