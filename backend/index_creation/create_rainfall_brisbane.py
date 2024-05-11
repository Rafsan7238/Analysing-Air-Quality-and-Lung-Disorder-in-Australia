from constants import RAINFALL_BRISBANE

def create_historic_tweets_index(es_client):
    if not es_client.indices.exists(index=RAINFALL_BRISBANE):
        '''Create RAINFALL_BRISBANE index'''
        body = {
            "settings": {
                "index": {
                    "number_of_shards": 1,
                    "number_of_replicas": 3
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
            index=RAINFALL_BRISBANE,
            body = body
        )
        return "Created"
    else:
        return 'Already Exists'