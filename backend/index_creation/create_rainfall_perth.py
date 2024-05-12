from constants import RAINFALL_PERTH

def create_historic_tweets_index(es_client):
    if not es_client.indices.exists(index=RAINFALL_PERTH):
        '''Create RAINFALL_PERTH index'''
        body = {
            "settings": {
                "index": {
                    "number_of_shards": 3,
                    "number_of_replicas": 1
                }
            },
            "mappings": {
                "properties": {
                    "Month": {
                        "type": "long"
                    },
                    "Monthly Precipitation Total (millimetres)": {
                        "type": "double"
                    },
                    "Product code": {
                        "type": "keyword"
                    },
                    "Quality": {
                        "type": "keyword"
                    },
                    "Station number": {
                        "type": "long"
                    },
                    "Year": {
                        "type": "long"
                    }
                }
            }
        }

        es_client.indices.create(
            index=RAINFALL_PERTH,
            body = body
        )
        return "Created"
    else:
        return 'Already Exists'