from constants import MORTALITY_MALES

def create_historic_tweets_index(es_client):
    if not es_client.indices.exists(index=MORTALITY_MALES):
        '''Create MORTALITY_MALES index'''
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
            index=MORTALITY_MALES,
            body = body
        )
        return "Created"
    else:
        return 'Already Exists'