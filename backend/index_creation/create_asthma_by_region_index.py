from constants import ASTHMA_BY_REGION_INDEX_NAME

def create_asthma_by_region_index(es_client):
    if not es_client.indices.exists(index=ASTHMA_BY_REGION_INDEX_NAME):
        '''Create asthma by region index'''
        body = {
            "settings": {
                "index": {
                    "number_of_shards": 1,
                    "number_of_replicas": 1
                }
            },
            "mappings": {
                "dynamic": "strict",
                "properties": {
                    'gccsa_code': {"type": "text"},
                    'gccsa_name': {"type": "text"},
                    'total asthma': {"type": "integer"},
                    'employed asthma': {"type": "integer"},
                    'australian asthma': {"type": "integer"},
                    'total copd': {"type": "integer"},
                    'australian copd': {"type": "integer"},
                    'foreigner asthma': {"type": "integer"},
                    'foreigner copd': {"type": "integer"}
                }
            }
        }

        es_client.indices.create(
            index=ASTHMA_BY_REGION_INDEX_NAME,
            body = body
        )
        return "Created"
    else:
        return 'Already Exists'