from datetime import datetime

from pytz import UTC
from constants import *
from querying.make_query import make_query
import numpy as np

def get_recent_averaged_by_daily(es):
    data_start = datetime(2024, 5, 17, tzinfo=UTC)
    joined = {}

    query = f"""    
        SELECT    
            "date" as "date", 
            AVG(air_temp) as "average air temp", 
            SUM(rain_trace) as "total rainfall"
        FROM {BOM_OBSERVATIONS}
        GROUP BY "date"
    """
    weather_rows = make_query(es, query)['rows']
    for date, avg_temp, total_rain in weather_rows:
        if datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=UTC) >=  data_start:
            joined[date] = joined.get(date, [avg_temp, total_rain, 0])

    query = f"""    
        SELECT    
            "date" as "date", 
            AVG(sentiment) as "average sentiment"
        FROM {MASTODON}
        GROUP BY "date"
    """
    sentiment_rows = make_query(es, query)['rows']
    for date, avg_sent in sentiment_rows:
        if datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=UTC) >=  data_start:  
            joined[date][2] = avg_sent

    rows = [[date]+stats for date, stats in joined.items()]
    columns = ['date', 'average air temp', 'total rainfall', 'average sentiment']
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