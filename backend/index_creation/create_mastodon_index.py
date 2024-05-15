from constants import MASTODON

def create_mastodon_index(es_client):
    if not es_client.indices.exists(index=MASTODON):
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
                    "id": {
                        "type": "text"
                    },
                    "content": {
                        "type": "text"
                    },
                    "created_at": {
                        "type": "date",
                        "format": "yyyy-MM-dd HH:mm:ss"
                    },
                    "sentiment": {
                        "type":"double"
                    }
                }
            }
        }

        es_client.indices.create(
            index=MASTODON,
            body = body
        )
        return "Created"
    else:
        return 'Already Exists'