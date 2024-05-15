def create_temperature_index(es_client, index_name):
    if not es_client.indices.exists(index=index_name):
        body = {
            "settings": {
                "index": {
                    "number_of_shards": 1,
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
            index=index_name,
            body = body
        )
        return "Created"
    else:
        return 'Already Exists'