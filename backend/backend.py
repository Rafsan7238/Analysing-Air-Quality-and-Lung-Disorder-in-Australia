import json
from flask import current_app, request
from flask import jsonify
from constants import ASTHMA_BY_REGION_INDEX_NAME, HIST_TWEET_INDEX_NAME

from flask import jsonify, current_app, request
from index_creation.create_mortality_persons import create_mortality_persons_index
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
import static.historic_tweet_sentiments 
import static.asthma_by_region 
import static.air_quality_hourly_avg 
import static.census_g21b 
import static.mortality_females 
import static.mortality_males 
import static.mortality_persons 
import static.rainfall_adelaide
import static.rainfall_brisbane
import static.rainfall_canberra
import static.rainfall_darwin
import static.rainfall_melbourne
import static.rainfall_perth
import static.rainfall_sydney
import static.rainfall_tasmania
import static.temperature_adelaide
import static.temperature_brisbane
import static.temperature_canberra
import static.temperature_darwin
import static.temperature_melbourne
import static.temperature_perth
import static.temperature_sydney
import static.temperature_tasmania

def insert_hist_tweets_endpoint():
    try:
        es = get_client()
        bulker = get_bulker()

        res = insert_hist_tweets(es, bulker)

        return json.dumps({'result': res})
    except Exception as e:
        return json.dumps(str(e))
    
def insert_region_asthma_endpoint():
    try:
        es = get_client()
        bulker = get_bulker()

        res = insert_region_asthma(es, bulker)

        return json.dumps({'result': res})
    except Exception as e:
        return json.dumps(str(e))

def insert_indexes():
    try: 
        print('starting')
        es = get_client()
        bulker = get_bulker()
        try:
            index= request.headers['X-Fission-Params-Index']
        except KeyError:
                print(request.headers)
                index= None

        if index == AIR_QUALITY_HOURLY_AVG:
            res = static.air_quality_hourly_avg.insert(es, bulker)
        elif index == ASTHMA_BY_REGION_INDEX_NAME:
            res = static.asthma_by_region.insert(es, bulker)
        elif index == CENSUS_G21B:
            res = static.census_g21b.insert(es, bulker)
        elif index == HIST_TWEET_INDEX_NAME:
            res = static.historic_tweet_sentiments.insert(es, bulker)
        elif index == MORTALITY_FEMALES:
            res = static.mortality_females.insert(es, bulker)
        elif index == MORTALITY_MALES:
            res = static.mortality_males.insert(es, bulker)
        elif index == MORTALITY_PERSONS:
            res = static.mortality_persons.insert(es, bulker)
        elif index == RAINFALL_ADELAIDE: 
            res = static.rainfall_adelaide.insert(es, bulker)
        elif index == RAINFALL_BRISBANE: 
            res = static.rainfall_brisbane.insert(es, bulker)
        elif index == RAINFALL_CANBERRA: 
            res = static.rainfall_canberra.insert(es, bulker)
        elif index == RAINFALL_DARWIN: 
            res = static.rainfall_darwin.insert(es, bulker)
        elif index == RAINFALL_MELBOURNE: 
            res = static.rainfall_melbourne.insert(es, bulker)
        elif index == RAINFALL_PERTH: 
            res = static.rainfall_perth.insert(es, bulker)
        elif index == RAINFALL_SYDNEY: 
            res = static.rainfall_sydney.insert(es, bulker)
        elif index == RAINFALL_TASMANIA: 
            res = static.rainfall_tasmania.insert(es, bulker)
        elif index == TEMPERATURE_ADELAIDE: 
            res = static.temperature_adelaide.insert(es, bulker)
        elif index == TEMPERATURE_BRISBANE: 
            res = static.temperature_brisbane.insert(es, bulker)
        elif index == TEMPERATURE_CANBERRA: 
            res = static.temperature_canberra.insert(es, bulker)
        elif index == TEMPERATURE_DARWIN: 
            res = static.temperature_darwin.insert(es, bulker)
        elif index == TEMPERATURE_MELBOURNE: 
            res = static.temperature_melbourne.insert(es, bulker)
        elif index == TEMPERATURE_PERTH: 
            res = static.temperature_perth.insert(es, bulker)
        elif index == TEMPERATURE_SYDNEY: 
            res = static.temperature_sydney.insert(es, bulker)
        elif index == TEMPERATURE_TASMANIA: 
            res = static.temperature_tasmania.insert(es, bulker)
        else:
            return jsonify({"success":False, "message":"incorrect index"}), 400
        return json.dumps({'result': res})
    
    except Exception as e:
        return json.dumps(str(e)) 

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



###############################
# air quality vs lung disease 
def query_elastic(index, query):

    es = get_client()
    list_of_docs = []

    # Initialize the scroll
    scroll = es.search(
        index=index,
        body=query,
        scroll='2m',  # Keep the search context alive for 2 minutes
        size=10000  # Number of results per page
    )

    # Keep track of the scroll ID
    scroll_id = scroll['_scroll_id']

    # Fetch the initial page of results
    for doc in scroll['hits']['hits']:
        print("DOC", doc)
        list_of_docs.append(doc['_source'])
    print("len", len(list_of_docs))
    # Use the scroll ID to fetch the next batch of documents
    while True:
        response = es.scroll(scroll_id=scroll_id, scroll='2m')
        print('response', response)
        # Break the loop if there are no more documents
        if not response['hits']['hits']:
            break
        
        for doc in response['hits']['hits']:
            list_of_docs.append(doc['_source'])
        print("len", len(list_of_docs))
    # Clean up the scroll context
    es.clear_scroll(scroll_id=scroll_id)
    return list_of_docs

def get_air_quality_hourly_avg():
    # get 2022_All_sites_air_quality_hourly_avg, 
    # select parameter_names = ['CO', 'PM10', 'PM2.5', 'O3', 'SO2']
    try: 
        selected_parameters = ['CO', 'PM10', 'PM2.5', 'O3', 'SO2']
        query = {"query": {"terms": {"parameter_name": selected_parameters}}}
        list_of_docs = query_elastic("air_quality_hourly_avg", query)
        print('returned', list_of_docs)
        return jsonify({"success": True, "data": list_of_docs}), 200

    except Exception as e:
        return json.dumps(str(e)) 
    

def get_index():
    # get all lung cancer data aihw_cimar_mortality_persons_gccsa_2009
 
    try: 
        print('starting')

        try:
            index= request.headers['X-Fission-Params-Index']
        except KeyError:
            print(request.headers)
            index= None


        print("index", index)
        
        query = {"query": {"match_all": {}}}
        list_of_docs = query_elastic(index, query)
        print('list_of_docs', list_of_docs)
        return jsonify({"success": True, "data": list_of_docs}), 200

    except Exception as e:
        return jsonify({"success": False, "data": json.dumps(str(e))}), 400
    # merge with census_by_cob_data abs_2021census_g21a_aust_gccsa
    # join on inner, ['gccsa_code', 'gccsa_name']
    