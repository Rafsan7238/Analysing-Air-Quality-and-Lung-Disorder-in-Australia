from constants import *
from querying.make_query import make_query
import pandas as pd

def get_PM_and_disease_by_greater_or_regional(es):
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
    location_PM = make_query(es, query)
    location_PM_df = pd.DataFrame(location_PM['rows'], columns=location_PM['columns']) 
    # Get PM values for locations

    pm25_df = location_PM_df[['location_name', 'value']].copy()
    pm25_df.rename(columns={'value': 'PM2.5'}, inplace=True)

    region_map = {
        'Alphington': 'Greater Melbourne',
        'Bendigo': 'Rest of Vic',
        'Box Hill': 'Greater Melbourne',
        'Brighton': 'Greater Melbourne',
        'Campbellfield': 'Greater Melbourne',
        'Churchill': 'Rest of Vic',
        'Footscray': 'Greater Melbourne',
        'Geelong South': 'Rest of Vic',
        'Melbourne CBD': 'Greater Melbourne',
        'Melton': 'Greater Melbourne',
        'Moe': 'Rest of Vic',
        'Morwell East': 'Rest of Vic',
        'Morwell South': 'Rest of Vic',
        'Newborough': 'Rest of Vic',
        'Traralgon': 'Rest of Vic'
    }

    # Map locations to greater or regional melbourne
    pm25_df.loc[:, 'region'] = pm25_df['location_name'].map(region_map)

    # Take means of pm values in the two regions
    pm25_aggregated = pm25_df.groupby(['region'])['PM2.5'].mean().reset_index()  ##

    # Get lung cancer data for inner and outer melbourne
    merged_data = get_cob_merge(es) 
    lung_cancer_df = merged_data[merged_data['gccsa_code'].isin(['2GMEL', '2RVIC'])]

    merged_df = pd.merge(lung_cancer_df, pm25_aggregated, left_on='gccsa_name', right_on='region', how='inner')
    data_json = merged_df.to_dict(orient='split')
    return {'columns': list(data_json['columns']), 'rows': list(data_json['data'])}

def get_cancer_by_gender(es):
    query = f"""
        SELECT * FROM {MORTALITY_MALES}
    """
    print('querying persons')
    male_json = make_query(es, query)
    male_df = pd.DataFrame(male_json['rows'], columns=male_json['columns'])    
    
    query = f"""
        SELECT * FROM {MORTALITY_FEMALES}
    """
    print('querying persons')
    female_json = make_query(es, query)
    female_df = pd.DataFrame(female_json['rows'], columns=female_json['columns'])    

    merged_data = male_df[['gccsa_name', 'lung_cancer_rate_per_100k']].merge(female_df[['gccsa_name', 'lung_cancer_rate_per_100k']], how='inner', on='gccsa_name', suffixes=('_male', '_female'))
    data_json = merged_data.to_dict(orient='split')
    return {'columns': list(data_json['columns']), 'rows': list(data_json['data'])}

def get_cob_merge(es):
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
    return persons_df.merge(asthma_by_region_df, how='inner', on=['gccsa_code', 'gccsa_name'])

def get_prevalence_by_location(es):
    merged_data = get_cob_merge(es)
    # Major locations
    major_locations = ['Greater Melbourne', 'Greater Sydney', 'Greater Brisbane', 'Greater Adelaide', 'Rest of Vic', 'Rest of NSW', 'Rest of Qld']

    # Define the aggregation function
    def aggregate_locations(location):
        if location in major_locations:
            return location
        else:
            return 'Others'

    # Apply the aggregation function to create a new column 'aggregated_location'
    merged_data.loc[:, 'aggregated_location'] = merged_data['gccsa_name'].apply(aggregate_locations)

    # Filter data for pie charts (include only major locations and "Others")
    filtered_data = merged_data.groupby('aggregated_location')[['total asthma', 'total copd', 'lung_cancer_total_mortality']].sum().reset_index()
    data_json = filtered_data.to_dict(orient='split')
    return {'columns': list(data_json['columns']), 'rows': list(data_json['data'])}

def get_cob_merge_lung_cancer(es):
    merged_data_json = get_cob_merge(es).to_dict(orient='split')
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
