import csv
from constants import MORTALITY_MALES

def insert_region_asthma(es, bulker):       
    if not es.indices.exists(index=MORTALITY_MALES):
        return f'{MORTALITY_MALES} index does not exist'

    # Use count API to get the number of documents in the index
    document_count = es.count(index=MORTALITY_MALES)['count']

    if(document_count > 0):
        return f'{MORTALITY_MALES} already has data. Please delete before attempting re-insertion.'

    try:
        with open('../userfunc/deployarchive/data/lung_disease_dataset/aihw_cimar_mortality_males_gccsa_2009.csv', 'r') as csv_file:
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
            
        bulker.bulk(es, inserts, index=MORTALITY_MALES)
    except Exception as e:
        return f'{e}'
    return 'success'