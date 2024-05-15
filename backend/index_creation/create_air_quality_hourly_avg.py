from constants import AIR_QUALITY_HOURLY_AVG

def create_air_quality_hourly_average(es_client):
    if not es_client.indices.exists(index=AIR_QUALITY_HOURLY_AVG):
        '''Create air quality hourly avg index'''
        body = {
            "settings": {
                "index": {
                    "number_of_shards": 3, # 765202 rows, deserves multiple shards
                    "number_of_replicas": 1
                }
            },
            "mappings": {
                "dynamic": "strict",
                "properties": {
                    "date": {"type": "keyword"},
                    "latitude": {"type": "double"},
                    "location": {"type": "geo_point"},
                    "location_name": {"type": "keyword"},
                    "longitude": {"type": "double"},
                    "parameter_description": {"type": "text"},
                    "parameter_method_name": {"type": "keyword"},
                    "parameter_name": {"type": "keyword"},
                    "time": {"type": "keyword"},
                    "value": { "type": "double"}
                    }
                }
        }

        es_client.indices.create(
            index=AIR_QUALITY_HOURLY_AVG,
            body = body
        )
        return "Created"
    else:
        return 'Already Exists'