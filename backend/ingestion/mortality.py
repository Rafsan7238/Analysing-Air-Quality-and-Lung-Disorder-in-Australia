def insert(es, bulker, data, index_name):       
    if not es.indices.exists(index=index_name):
        return f'{index_name} index does not exist'

    # Use count API to get the number of documents in the index
    document_count = es.count(index=index_name)['count']

    if(document_count > 0):
        return f'{index_name} already has data. Please delete before attempting re-insertion.'

    try:
        inserts = []
        for _, row in data.items():
            insert = {
                'create': {
                    "all_cancer_population": row['all_cancer_population'],
                    "all_cancer_total_mortality": row['all_cancer_total_mortality'],
                    "gccsa_code": row['gccsa_code'],
                    "gccsa_name": row['gccsa_name'],
                    "lung_cancer_population": row['lung_cancer_population'],
                    "lung_cancer_rate_per_100k": row['lung_cancer_rate_per_100k'],
                    "lung_cancer_total_mortality": row['lung_cancer_total_mortality']
                }
            }
            inserts.append(insert)
            
        result = bulker.bulk(es, inserts, index=index_name)
    except Exception as e:
        return f'{e}'
    return result