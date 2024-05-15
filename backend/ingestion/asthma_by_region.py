from constants import ASTHMA_BY_REGION_INDEX_NAME

def insert(es, bulker, data):       
    if not es.indices.exists(index=ASTHMA_BY_REGION_INDEX_NAME):
        return f'{ASTHMA_BY_REGION_INDEX_NAME} index does not exist'

    # Use count API to get the number of documents in the index
    document_count = es.count(index=ASTHMA_BY_REGION_INDEX_NAME)['count']

    if(document_count > 0):
        return f'{ASTHMA_BY_REGION_INDEX_NAME} already has data. Please delete before attempting re-insertion.'

    try:
        inserts = []
        for _, row in data.items():
            insert = {
                'create': {
                    'gccsa_code': row['gccsa_code'],
                    'gccsa_name': row['gccsa_name'],
                    'total asthma': row['Total asthma'],
                    'employed asthma': row['Employed asthma'],
                    'australian asthma': row['Australian asthma'],
                    'total copd': row['Total COPD'],
                    'australian copd': row['Australian COPD'],
                    'foreigner asthma': row['Foreigner asthma'],
                    'foreigner copd': row['Foreigner COPD']
                }
            }
            inserts.append(insert)
        
        result = bulker.bulk(es, inserts, index=ASTHMA_BY_REGION_INDEX_NAME)
    except Exception as e:
        return f'{e}'
    return result