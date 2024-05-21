from constants import *
from querying.make_query import make_query
import pandas as pd

def get_cob_merge_lung_cancer(es):
    query = f"""
        SELECT * FROM {MORTALITY_PERSONS}
    """
    print('querying persons')
    persons_json = make_query(es, query)
    persons_df = pd.DataFrame(persons_json['rows'], columns=persons_json['columns'])

    query = f"""
        SELECT * FROM {ASTHMA_BY_REGION_INDEX_NAME}
    """
    print('querying asthma')

    asthma_by_region = make_query(es, query)
    asthma_by_region_df = pd.DataFrame(asthma_by_region['rows'], columns=asthma_by_region['columns'])
    merged_data = persons_df.merge(asthma_by_region_df, how='inner', on=['gccsa_code', 'gccsa_name'])
    merged_data_json = merged_data.to_dict(orient='split')
    return {'columns': list(merged_data_json['columns']), 'rows': list(merged_data_json['data'])}


def get_air_quality_hourly_for_spatial(es):
    query = """
        SELECT location_name, 
        parameter_name,
        latitude,
        longitude,
        AVG(value) as value
        FROM air_quality_hourly_avg 
            WHERE parameter_name = 'PM2.5' 
            AND date > '01/01/22'
            AND date < '31/12/22'
        GROUP BY location_name, parameter_name, latitude, longitude
    """
    return make_query(es, query)

def get_air_quality_hourly_for_statistical(es):
    query = """
        SELECT 
            location_name, 
            value,
            date,
            time
        FROM air_quality_hourly_avg
        WHERE parameter_name = 'PM2.5'
    """
    return make_query(es, query)

def get_air_quality_hourly_summary_stats_by_parameter(es):
    query = """
            SELECT 
                parameter_name, 
                SUM(1) as count, 
                AVG(value) as mean, 
                STDDEV_POP(value) as std, 
                MIN(value) as min, 
                PERCENTILE(value, 25) as "25%", 
                PERCENTILE(value, 50) as "50%", 
                PERCENTILE(value, 75) as "75%", 
                MAX(value) as max
            FROM air_quality_hourly_avg 
                WHERE 
                parameter_name in ('CO','O3','PM10','PM2.5','SO2')
            GROUP BY parameter_name 
        """
    return make_query(es, query)

def get_air_quality_hourly_summary_stats_by_location(es):
    query = """  
        SELECT 
            location_name, 
            SUM(1) as count, 
            AVG(value) as mean, 
            STDDEV_POP(value) as std, 
            MIN(value) as min, 
            PERCENTILE(value, 25) as "25%", 
            PERCENTILE(value, 50) as "50%", 
            PERCENTILE(value, 75) as "75%", 
            MAX(value) as max
        FROM air_quality_hourly_avg
        WHERE parameter_name = 'PM2.5'
        GROUP BY location_name 
    """
    return make_query(es, query)

def get_air_quality_data_dist(es):
    query = """
        SELECT location_name, 
        SUM(1) as row_count
        FROM air_quality_hourly_avg 
            WHERE parameter_name = 'PM2.5' 
        GROUP BY location_name
    """
    return make_query(es, query)
