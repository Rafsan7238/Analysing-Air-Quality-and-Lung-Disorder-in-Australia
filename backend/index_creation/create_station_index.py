from constants import STATIONS

def create_station_index(es_client):
    if not es_client.indices.exists(index=STATIONS):
        '''Create stations index'''
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
                    "station_name": {"type": "text"},
                    "url": {"type": "text"}
                    }
                }
        }

        es_client.indices.create(
            index=STATIONS,
            body = body
        )
        return "Created"
    else:
        return 'Already Exists'