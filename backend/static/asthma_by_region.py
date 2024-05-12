import csv
from constants import ASTHMA_BY_REGION_INDEX_NAME

def insert(es, bulker):       
    if not es.indices.exists(index=ASTHMA_BY_REGION_INDEX_NAME):
        return f'{ASTHMA_BY_REGION_INDEX_NAME} index does not exist'

    # Use count API to get the number of documents in the index
    document_count = es.count(index=ASTHMA_BY_REGION_INDEX_NAME)['count']

    if(document_count > 0):
        return f'{ASTHMA_BY_REGION_INDEX_NAME} already has data. Please delete before attempting re-insertion.'

    try:
        with open('../userfunc/deployarchive/data/lung_disease_dataset/abs_2021census_g21a_aust_gccsa.csv', 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')

            inserts = []
            for row in csv_reader:
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
            
        bulker.bulk(es, inserts, index=ASTHMA_BY_REGION_INDEX_NAME)
    except Exception as e:
        return f'{e}'
    return 'success'