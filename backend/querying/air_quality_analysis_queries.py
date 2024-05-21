from querying.make_query import make_query

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
    return result
