from constants import BOM_OBSERVATIONS

def create_bom_index(es_client):
    if not es_client.indices.exists(index=BOM_OBSERVATIONS):
        '''Create bom index'''
        body = {
            "settings": {
                "index": {
                    "number_of_shards": 3,
                    "number_of_replicas": 1
                }
            },
            "mappings": {
                "dynamic": "strict",
                "properties": {
                    "date": {
                        "type": "date",
                        "format": "dd/MM/yy"
                    },
                    "aifstime_utc": {
                        "type": "keyword"
                    },
                    "air_temp": {
                        "type": "double"
                    },
                    "name": {
                        "type": "keyword"
                    },
                    "rain_trace": {
                        "type": "double"
                    }
                }
            }
        }

        es_client.indices.create(
            index=BOM_OBSERVATIONS,
            body = body
        )
        return "Created"
    else:
        return 'Already Exists'