import csv
from constants import MORTALITY_FEMALES

def insert(es, bulker):       
    if not es.indices.exists(index=MORTALITY_FEMALES):
        return f'{MORTALITY_FEMALES} index does not exist'

    # Use count API to get the number of documents in the index
    document_count = es.count(index=MORTALITY_FEMALES)['count']

    if(document_count > 0):
        return f'{MORTALITY_FEMALES} already has data. Please delete before attempting re-insertion.'

    try:
        with open('../userfunc/deployarchive/data/lung_disease_dataset/aihw_cimar_mortality_females_gccsa_2009.csv', 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')

            inserts = []
            for row in csv_reader:
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
            
        bulker.bulk(es, inserts, index=MORTALITY_FEMALES)
    except Exception as e:
        return f'{e}'
    return 'success'