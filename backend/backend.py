import json
from flask import request, jsonify
from harvesters.BOM import addobservations
from harvesters.Mastodon import mharvester
from constants import *
from elastic_client_provider import get_bulker, get_client
import time
from datetime import datetime

from querying.sentiment_weather_queries import *
from querying.air_quality_analysis_queries import *
from querying.query_path_constants import *
from querying.make_query import make_query

from index_creation.create_station_index import create_station_index
from index_creation.create_bom_index import create_bom_index
from index_creation.create_mastodon_index import create_mastodon_index
from index_creation.create_mortality_index import create_mortality_index
from index_creation.create_temperature_index import create_temperature_index
from index_creation.create_air_quality_hourly_avg import create_air_quality_hourly_average
from index_creation.create_census_g21b import create_census_g21b
from index_creation.create_rainfall_index import create_rainfall_index
from index_creation.create_asthma_by_region_index import create_asthma_by_region_index
from index_creation.create_historic_tweets_index import create_historic_tweets_index
from index_creation.create_station_index import create_station_index

import ingestion.historic_tweet_sentiments 
import ingestion.asthma_by_region 
import ingestion.air_quality_hourly_avg 
import ingestion.census_g21b
import ingestion.rainfall
import ingestion.stations
import ingestion.temperature
import ingestion.mortality

def insert_documents():
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
        elif index == STATIONS: 
            res = ingestion.stations.insert(es, bulker, data)
        elif index == BOM_OBSERVATIONS:
            res = addobservations.catch_up_history()
        elif index == MASTODON:
            res = mharvester.catch_up_history(data)
        else:
            return "Index not found", 404
        return f"{res}", 201
    
    except Exception as e:
        return json.dumps(str(e)), 500

def create_indexes_endpoint():
    try:    
        es = get_client()

        results = dict()
        results[AIR_QUALITY_HOURLY_AVG] = create_air_quality_hourly_average(es)   
        results[ASTHMA_BY_REGION_INDEX_NAME] = create_asthma_by_region_index(es)   
        results[CENSUS_G21B] = create_census_g21b(es)   
        results[HIST_TWEET_INDEX_NAME] = create_historic_tweets_index(es)
        results[MORTALITY_FEMALES] = create_mortality_index(es, MORTALITY_FEMALES)   
        results[MORTALITY_MALES] = create_mortality_index(es, MORTALITY_MALES)   
        results[MORTALITY_PERSONS] = create_mortality_index(es, MORTALITY_PERSONS)   
        results[RAINFALL_ADELAIDE] = create_rainfall_index(es, RAINFALL_ADELAIDE)   
        results[RAINFALL_BRISBANE] = create_rainfall_index(es, RAINFALL_BRISBANE)      
        results[RAINFALL_CANBERRA] = create_rainfall_index(es, RAINFALL_CANBERRA)   
        results[RAINFALL_DARWIN] = create_rainfall_index(es, RAINFALL_DARWIN)   
        results[RAINFALL_MELBOURNE] =  create_rainfall_index(es, RAINFALL_MELBOURNE)   
        results[RAINFALL_PERTH] = create_rainfall_index(es, RAINFALL_PERTH)   
        results[RAINFALL_SYDNEY] = create_rainfall_index(es, RAINFALL_SYDNEY)   
        results[RAINFALL_TASMANIA] = create_rainfall_index(es, RAINFALL_TASMANIA)   

        results[TEMPERATURE_ADELAIDE] = create_temperature_index(es, TEMPERATURE_ADELAIDE)   
        results[TEMPERATURE_BRISBANE] = create_temperature_index(es, TEMPERATURE_BRISBANE)   
        results[TEMPERATURE_CANBERRA] = create_temperature_index(es, TEMPERATURE_CANBERRA)   
        results[TEMPERATURE_DARWIN] = create_temperature_index(es, TEMPERATURE_DARWIN)    
        results[TEMPERATURE_MELBOURNE] = create_temperature_index(es, TEMPERATURE_MELBOURNE)   
        results[TEMPERATURE_PERTH] = create_temperature_index(es, TEMPERATURE_PERTH)     
        results[TEMPERATURE_SYDNEY] = create_temperature_index(es, TEMPERATURE_SYDNEY)   
        results[TEMPERATURE_TASMANIA] = create_temperature_index(es, TEMPERATURE_TASMANIA)   

        results[MASTODON] = create_mastodon_index(es)
        results[BOM_OBSERVATIONS] = create_bom_index(es)
        results[STATIONS] = create_station_index(es)

        return json.dumps(results), 201
    except Exception as e:
        return json.dumps(str(e)), 500

###############################

def select_all_from_index():
    try:
        index = request.headers['X-Fission-Params-Index']
    except KeyError:
        return jsonify({'Index not found in headers': str(request.headers)}), 400
    
    es = get_client()

    if index == AIR_QUALITY_HOURLY_AVG:
        return jsonify({'result': "Select all is not allowed for this index"}), 400
    
    query = f"""
        SELECT * FROM {index}
    """

    try:
        return jsonify({'result': make_query(es, query)}), 200
    except Exception as e:
        return json.dumps(str(e)), 500

def air_quality_endpoint():
    start = time.time()
    print(f'Function invoked at {datetime.now()}')

    try:
        resource = request.headers['X-Fission-Params-Resource']

    except KeyError:
        return jsonify({'Resource not found in headers': str(request.headers)}), 400

    es = get_client()

    result = None
    try:
        if resource == SUMMARY_STATS_BY_PARAM:
            result = jsonify({'result': get_air_quality_hourly_summary_stats_by_parameter(es)}), 200
        elif resource == SUMMARY_STATS_BY_LOC:
            result = jsonify({'result': get_air_quality_hourly_summary_stats_by_location(es)}), 200
        elif resource == DATA_DIST:
            result = jsonify({'result': get_air_quality_data_dist(es)}), 200
        elif resource == FOR_STATISTICAL_ANALYSIS:
            result = jsonify({'result': get_air_quality_hourly_for_statistical(es)}), 200
        elif resource == FOR_SPATIAL_ANALYSIS:
            result = jsonify({'result': get_air_quality_hourly_for_spatial(es)}), 200
        else:
            result = jsonify({'Resource in headers is not valid': resource}), 400
    except Exception as e:
        result = json.dumps(str(e)), 500

    print(f'Time taken: {time.time() - start}')
    return result

def sentiment_weather_queries_endpoint():
    try:
        resource = request.headers['X-Fission-Params-Resource']

    except KeyError:
        return jsonify({'Resource not found in headers': str(request.headers)}), 400

    es = get_client()
    
    try:
        if resource == AVG_MONTHLY_ANALYSIS:
            return jsonify({'result': get_averaged_by_month(es)}), 200
        if resource == UPDATING_ANALYSIS:
            return jsonify({'result': get_recent_averaged_sentiment_by_hourly(es)}), 200
        if resource == MESSAGE_COUNTS_HOURLY:
            return jsonify({'result': get_recent_total_sentiment_by_hourly(es)}), 200
        else:
            return jsonify({'Resource in headers is not valid': resource}), 400
        
    except Exception as e:
        return json.dumps(str(e)), 500

def make_query_endpoint():
    es = get_client()

    try:
        data = request.json
    except KeyError:
        return 'failed to parse request json body', 400

    try:
        if data is not None:
            res = make_query(es, data['query'])
            return jsonify({'result': res}), 200
        else:
            return jsonify({'result': 'No data in body'}), 400
    except Exception as e:
        return jsonify({"Query failed": str(e)}), 500