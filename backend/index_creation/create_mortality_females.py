from constants import MORTALITY_FEMALES

def create_mortality_females_index(es_client):
    if not es_client.indices.exists(index=MORTALITY_FEMALES):
        '''Create mortality_females index'''
        body = {
            "settings": {
                "index": {
                    "number_of_shards": 1,
                    "number_of_replicas": 3
                }
            },
            "mappings": {
                "properties": {
                    "all_cancer_population": {
                        "type": "long"
                    },
                    "all_cancer_total_mortality": {
                        "type": "long"
                    },
                    "gccsa_code": {
                        "type": "keyword"
                    },
                    "gccsa_name": {
                        "type": "keyword"
                    },
                    "lung_cancer_population": {
                        "type": "long"
                    },
                    "lung_cancer_rate_per_100k": {
                        "type": "double"
                    },
                    "lung_cancer_total_mortality": {
                        "type": "long"
                    }
                    }
            }
        }

        es_client.indices.create(
            index=MORTALITY_FEMALES,
            body = body
        )
        return "Created"
    else:
        return 'Already Exists'