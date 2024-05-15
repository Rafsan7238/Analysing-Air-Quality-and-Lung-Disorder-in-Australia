def create_mortality_index(es_client, mortality_index_name):
    if not es_client.indices.exists(index=mortality_index_name):
        body = {
            "settings": {
                "index": {
                    "number_of_shards": 1,
                    "number_of_replicas": 1
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
            index=mortality_index_name,
            body = body
        )
        return "Created"
    else:
        return 'Already Exists'