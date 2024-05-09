from constants import TEMPERATURE_PERTH

def create_historic_tweets_index(es_client):
    if not es_client.indices.exists(index=TEMPERATURE_PERTH):
        '''Create TEMPERATURE_PERTH index'''
        body = {
            "settings": {
                "index": {
                    "number_of_shards": 3,
                    "number_of_replicas": 1
                }
            },
            "mappings": {
                "properties": {
                    "Bureau of Meteorology station number": {
                        "type": "long"
                    },
                    "Mean maximum temperature (°C)": {
                        "type": "double"
                    },
                    "Month": {
                        "type": "long"
                    },
                    "Product code": {
                        "type": "keyword"
                    },
                    "Quality": {
                        "type": "keyword"
                    },
                    "Year": {
                        "type": "long"
                    }
                }
            }
        }

        es_client.indices.create(
            index=TEMPERATURE_PERTH,
            body = body
        )
        return "Created"
    else:
        return 'Already Exists'