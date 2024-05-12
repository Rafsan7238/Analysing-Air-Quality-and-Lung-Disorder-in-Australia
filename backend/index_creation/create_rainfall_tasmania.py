from constants import RAINFALL_TASMANIA

def create_rainfall_tasmania_index(es_client):
    if not es_client.indices.exists(index=RAINFALL_TASMANIA):
        '''Create RAINFALL_TASMANIA index'''
        body = {
            "settings": {
                "index": {
                    "number_of_shards": 1,
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
            index=RAINFALL_TASMANIA,
            body = body
        )
        return "Created"
    else:
        return 'Already Exists'