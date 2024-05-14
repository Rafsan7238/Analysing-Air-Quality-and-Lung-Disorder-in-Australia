import json
from flask import request
from index_creation.create_mortality_index import create_mortality_index
from index_creation.create_temperature_index import create_temperature_index
from index_creation.create_air_quality_hourly_avg import create_air_quality_hourly_average
from index_creation.create_census_g21b import create_census_g21b
from index_creation.create_rainfall_index import create_rainfall_index
from constants import *
from elastic_client_provider import get_bulker, get_client
from index_creation.create_asthma_by_region_index import create_asthma_by_region_index
from index_creation.create_historic_tweets_index import create_historic_tweets_index
import ingestion.historic_tweet_sentiments 
import ingestion.asthma_by_region 
import ingestion.air_quality_hourly_avg 
import ingestion.census_g21b
import ingestion.rainfall
import ingestion.temperature
import ingestion.mortality

def insert_indexes():
    try: 
        print('starting')

        es = get_client()
        bulker = get_bulker()
        try:
            index= request.headers['X-Fission-Params-Index']
            data = request.json
        except KeyError:
            print(request.headers)
            index= None

        if index == AIR_QUALITY_HOURLY_AVG:
            res = ingestion.air_quality_hourly_avg.insert(es, bulker, data)
        elif index == ASTHMA_BY_REGION_INDEX_NAME:
            res = ingestion.asthma_by_region.insert(es, bulker, data)
        elif index == CENSUS_G21B:
            res = ingestion.census_g21b.insert(es, bulker, data)
        elif index == HIST_TWEET_INDEX_NAME:
            res = ingestion.historic_tweet_sentiments.insert(es, bulker, data)
        elif index == MORTALITY_FEMALES:
            res = ingestion.mortality.insert(es, bulker, data, MORTALITY_FEMALES)
        elif index == MORTALITY_MALES:
            res = ingestion.mortality.insert(es, bulker, data, MORTALITY_MALES)
        elif index == MORTALITY_PERSONS:
            res = ingestion.mortality.insert(es, bulker, data, MORTALITY_PERSONS)
        elif index == RAINFALL_ADELAIDE: 
            res = ingestion.rainfall.insert(es, bulker, data, RAINFALL_ADELAIDE)
        elif index == RAINFALL_BRISBANE: 
            res = ingestion.rainfall.insert(es, bulker, data, RAINFALL_BRISBANE)
        elif index == RAINFALL_CANBERRA: 
            res = ingestion.rainfall.insert(es, bulker, data, RAINFALL_CANBERRA)
        elif index == RAINFALL_DARWIN: 
            res = ingestion.rainfall.insert(es, bulker, data, RAINFALL_DARWIN)
        elif index == RAINFALL_MELBOURNE: 
            res = ingestion.rainfall.insert(es, bulker, data, RAINFALL_MELBOURNE)
        elif index == RAINFALL_PERTH: 
            res = ingestion.rainfall.insert(es, bulker, data, RAINFALL_PERTH)
        elif index == RAINFALL_SYDNEY: 
            res = ingestion.rainfall.insert(es, bulker, data, RAINFALL_SYDNEY)
        elif index == RAINFALL_TASMANIA: 
            res = ingestion.rainfall.insert(es, bulker, data, RAINFALL_TASMANIA)
        elif index == TEMPERATURE_ADELAIDE: 
            res = ingestion.temperature.insert(es, bulker, data, TEMPERATURE_ADELAIDE)
        elif index == TEMPERATURE_BRISBANE: 
            res = ingestion.temperature.insert(es, bulker, data, TEMPERATURE_BRISBANE)
        elif index == TEMPERATURE_CANBERRA: 
            res = ingestion.temperature.insert(es, bulker, data, TEMPERATURE_CANBERRA)
        elif index == TEMPERATURE_DARWIN: 
            res = ingestion.temperature.insert(es, bulker, data, TEMPERATURE_DARWIN)
        elif index == TEMPERATURE_MELBOURNE: 
            res = ingestion.temperature.insert(es, bulker, data, TEMPERATURE_MELBOURNE)
        elif index == TEMPERATURE_PERTH: 
            res = ingestion.temperature.insert(es, bulker, data, TEMPERATURE_PERTH)
        elif index == TEMPERATURE_SYDNEY: 
            res = ingestion.temperature.insert(es, bulker, data, TEMPERATURE_SYDNEY)
        elif index == TEMPERATURE_TASMANIA: 
            res = ingestion.temperature.insert(es, bulker, data, TEMPERATURE_TASMANIA)
        else:
            return "Index not found", 404
        return f"{res}", 201
    
    except Exception as e:
        return json.dumps(str(e)), 500

def create_indexes_endpoint():
    try:    
        results = dict()
        results[AIR_QUALITY_HOURLY_AVG] = create_air_quality_hourly_average(get_client())   
        results[ASTHMA_BY_REGION_INDEX_NAME] = create_asthma_by_region_index(get_client())   
        results[CENSUS_G21B] = create_census_g21b(get_client())   
        results[HIST_TWEET_INDEX_NAME] = create_historic_tweets_index(get_client())
        results[MORTALITY_FEMALES] = create_mortality_index(get_client(), MORTALITY_FEMALES)   
        results[MORTALITY_MALES] = create_mortality_index(get_client(), MORTALITY_MALES)   
        results[MORTALITY_PERSONS] = create_mortality_index(get_client(), MORTALITY_PERSONS)   
        results[RAINFALL_ADELAIDE] = create_rainfall_index(get_client(), RAINFALL_ADELAIDE)   
        results[RAINFALL_BRISBANE] = create_rainfall_index(get_client(), RAINFALL_BRISBANE)      
        results[RAINFALL_CANBERRA] = create_rainfall_index(get_client(), RAINFALL_CANBERRA)   
        results[RAINFALL_DARWIN] = create_rainfall_index(get_client(), RAINFALL_DARWIN)   
        results[RAINFALL_MELBOURNE] =  create_rainfall_index(get_client(), RAINFALL_MELBOURNE)   
        results[RAINFALL_PERTH] = create_rainfall_index(get_client(), RAINFALL_PERTH)   
        results[RAINFALL_SYDNEY] = create_rainfall_index(get_client(), RAINFALL_SYDNEY)   
        results[RAINFALL_TASMANIA] = create_rainfall_index(get_client(), RAINFALL_TASMANIA)   

        results[TEMPERATURE_ADELAIDE] = create_temperature_index(get_client(), TEMPERATURE_ADELAIDE)   
        results[TEMPERATURE_BRISBANE] = create_temperature_index(get_client(), TEMPERATURE_BRISBANE)   
        results[TEMPERATURE_CANBERRA] = create_temperature_index(get_client(), TEMPERATURE_CANBERRA)   
        results[TEMPERATURE_DARWIN] = create_temperature_index(get_client(), TEMPERATURE_DARWIN)    
        results[TEMPERATURE_MELBOURNE] = create_temperature_index(get_client(), TEMPERATURE_MELBOURNE)   
        results[TEMPERATURE_PERTH] = create_temperature_index(get_client(), TEMPERATURE_PERTH)     
        results[TEMPERATURE_SYDNEY] = create_temperature_index(get_client(), TEMPERATURE_SYDNEY)   
        results[TEMPERATURE_TASMANIA] = create_temperature_index(get_client(), TEMPERATURE_TASMANIA)   
    
        return json.dumps(results), 201
    except Exception as e:
        return json.dumps(str(e)), 500
