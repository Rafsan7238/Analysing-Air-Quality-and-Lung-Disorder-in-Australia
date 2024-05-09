from constants import CENSUS_G21B

def create_census_g21b(es_client):
    if not es_client.indices.exists(index=CENSUS_G21B):
        '''Create census_g21b index'''
        body = {
            "settings": {
                "index": {
                    "number_of_shards": 3,
                    "number_of_replicas": 1
                }
            },
            "mappings": {
                "properties": {
                    "assistance_needed_asthma": {
                    "type": "long"
                    },
                    "assistance_needed_copd": {
                        "type": "long"
                    },
                    "employed_copd": {
                        "type": "long"
                    },
                    "gccsa_code": {
                        "type": "keyword"
                    },
                    "gccsa_name": {
                        "type": "keyword"
                    },
                    "total_asthma": {
                        "type": "long"
                    },
                    "total_copd": {
                        "type": "long"
                    },
                    "unemployed_asthma": {
                        "type": "long"
                    },
                    "unemployed_copd": {
                        "type": "long"
                    },
                    "weekly_income_1000_1749_asthma": {
                        "type": "long"
                    },
                    "weekly_income_1000_1749_copd": {
                        "type": "long"
                    },
                    "weekly_income_1750_2999_asthma": {
                        "type": "long"
                    },
                    "weekly_income_1750_2999_copd": {
                        "type": "long"
                    },
                    "weekly_income_1_299_asthma": {
                        "type": "long"
                    },
                    "weekly_income_1_299_copd": {
                        "type": "long"
                    },
                    "weekly_income_3000_asthma": {
                        "type": "long"
                    },
                    "weekly_income_3000_copd": {
                        "type": "long"
                    },
                    "weekly_income_300_649_asthma": {
                        "type": "long"
                    },
                    "weekly_income_300_649_copd": {
                        "type": "long"
                    },
                    "weekly_income_650_999_asthma": {
                        "type": "long"
                    },
                    "weekly_income_650_999_copd": {
                        "type": "long"
                    },
                    "weekly_income_nil_asthma": {
                        "type": "long"
                    },
                    "weekly_income_nil_copd": {
                        "type": "long"
                    }
                }
            }
        }

        es_client.indices.create(
            index=CENSUS_G21B,
            body = body
        )
        return "Created"
    else:
        return 'Already Exists'