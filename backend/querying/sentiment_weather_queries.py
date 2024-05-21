from datetime import datetime

from pytz import UTC
from constants import *
from querying.make_query import make_query
import numpy as np

def get_recent_averaged_sentiment_by_hourly(es):
    data_start = datetime(2024, 5, 17, tzinfo=UTC)
    joined = {}

    query = f"""    
        SELECT    
            HISTOGRAM(DATETIME_PARSE(aifstime_utc,'yyyyMMddHHmmss'), INTERVAL 1 HOUR) as hour,
                AVG(air_temp) as air_temp,
                SUM(rain_trace) as total_rain
        
        FROM {BOM_OBSERVATIONS}
        GROUP BY hour
    """
    weather_rows = make_query(es, query)['rows']
    for hour, avg_temp, total_rain in weather_rows:
        if datetime.strptime(hour, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=UTC) >=  data_start:
            joined[hour] = joined.get(hour, [avg_temp, total_rain, 0])

    query = f"""    
        SELECT    
            HISTOGRAM(created_at, INTERVAL 1 HOUR) as hour,
            SUM(sentiment) as sum_sentiment
        FROM {MASTODON}
        WHERE sentiment <> 0.0 
        GROUP BY hour 
    """
    sentiment_rows = make_query(es, query)['rows']
    for hour, avg_sent in sentiment_rows:
        if datetime.strptime(hour, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=UTC) >=  data_start:  
            if hour in joined.keys():
                joined[hour][2] = avg_sent

    rows = [[hour]+stats for hour, stats in joined.items()]
    columns = ['hour', 'average air temp', 'total rainfall', 'sum sentiment']
    return {'columns': columns, 'rows': rows }


def get_recent_total_sentiment_by_hourly(es):
    data_start = datetime(2024, 5, 17, tzinfo=UTC)
    joined = {}

    query = f"""    
        SELECT    
            HISTOGRAM(DATETIME_PARSE(aifstime_utc,'yyyyMMddHHmmss'), INTERVAL 1 HOUR) as hour,
                AVG(air_temp) as air_temp,
                SUM(rain_trace) as total_rain
        
        FROM {BOM_OBSERVATIONS}
        GROUP BY hour
    """
    weather_rows = make_query(es, query)['rows']
    for hour, avg_temp, total_rain in weather_rows:
        if datetime.strptime(hour, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=UTC) >=  data_start:
            joined[hour] = joined.get(hour, [avg_temp, total_rain, 0])

    query = f"""    
        SELECT    
            HISTOGRAM(created_at, INTERVAL 1 HOUR) as hour,
            SUM(1) as message_count
        FROM {MASTODON}
        WHERE sentiment <> 0.0 
        GROUP BY hour 
    """
    sentiment_rows = make_query(es, query)['rows']
    for hour, avg_sent in sentiment_rows:
        if datetime.strptime(hour, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=UTC) >=  data_start:  
            if hour in joined.keys():
                joined[hour][2] = avg_sent

    rows = [[hour]+stats for hour, stats in joined.items()]
    columns = ['hour', 'average air temp', 'total rainfall', 'message counts']
    return {'columns': columns, 'rows': rows }


def get_averaged_by_month(es):
    rainfall_sources = [
        RAINFALL_ADELAIDE, 
        RAINFALL_BRISBANE, 
        RAINFALL_CANBERRA, 
        RAINFALL_DARWIN, 
        RAINFALL_MELBOURNE, 
        RAINFALL_PERTH, 
        RAINFALL_SYDNEY, 
        RAINFALL_TASMANIA
    ]

    monthly_avg_rainfall = {}
    for source in rainfall_sources:
        query = f"""    
            SELECT 
                Month,
                AVG("Monthly Precipitation Total (millimetres)") as "Avg Rainfall"
            FROM {source}
            GROUP BY Month
        """
        rows = make_query(es, query)['rows']
        rows_np = np.array(rows)
        for month, average in rows_np:
            monthly_avg_rainfall[month] = monthly_avg_rainfall.get(month, []) + [average]

    temperature_sources = [
            TEMPERATURE_ADELAIDE, 
            TEMPERATURE_BRISBANE, 
            TEMPERATURE_CANBERRA, 
            TEMPERATURE_DARWIN, 
            TEMPERATURE_MELBOURNE, 
            TEMPERATURE_PERTH, 
            TEMPERATURE_SYDNEY, 
            TEMPERATURE_TASMANIA
        ]

    monthly_avg_temperature = {}
    for source in temperature_sources:
        query = f"""    
            SELECT 
                Month,
                AVG("Mean maximum temperature (°C)") as "Avg Max Temp"
            FROM {source}
            GROUP BY Month
        """
        rows = make_query(es, query)['rows']
        rows_np = np.array(rows)
        for month, average in rows_np:
            monthly_avg_temperature[month] = monthly_avg_temperature.get(month, []) + [average]

    query = """    
        SELECT 
            month,
            AVG(total_sentiment)/100 as "total_sentiment(scaled)"
        FROM historic_tweet_sentiments
        GROUP BY month
    """
    monthly_avg_sentiment = {}
    for month, avg_scaled_sentiment in make_query(es, query)['rows']:
        monthly_avg_sentiment[month] = monthly_avg_sentiment.get(month, []) + [avg_scaled_sentiment]

    rows=[
        [
        str(month), 
        np.mean(monthly_avg_rainfall.get(month, [0])), 
        np.mean(monthly_avg_temperature.get(month, [0])),
        np.mean(monthly_avg_sentiment.get(month, [0]))
        ]
        for month in range(1, 13)]
    
    columns = ["Month", "Avg Rainfall", "Avg Max Temp", "Avg Sentiment (Scaled)"]
    return {'columns': columns, 'rows': rows}