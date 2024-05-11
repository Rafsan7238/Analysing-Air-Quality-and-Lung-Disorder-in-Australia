from constants import TEMPERATURE_MELBOURNE

def create_historic_tweets_index(es_client):
    if not es_client.indices.exists(index=TEMPERATURE_MELBOURNE):
        '''Create TEMPERATURE_MELBOURNE index'''
        body = {
            "settings": {
                "index": {
                    "number_of_shards": 1,
                    "number_of_replicas": 3
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
            index=TEMPERATURE_MELBOURNE,
            body = body
        )
        return "Created"
    else:
        return 'Already Exists'