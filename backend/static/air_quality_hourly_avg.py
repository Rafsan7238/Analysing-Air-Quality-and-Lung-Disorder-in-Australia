import csv
from constants import AIR_QUALITY_HOURLY_AVG

def insert(es, bulker):       
    if not es.indices.exists(index=AIR_QUALITY_HOURLY_AVG):
        return f'{AIR_QUALITY_HOURLY_AVG} index does not exist'

    # Use count API to get the number of documents in the index
    document_count = es.count(index=AIR_QUALITY_HOURLY_AVG)['count']

    if(document_count > 0):
        return f'{AIR_QUALITY_HOURLY_AVG} already has data. Please delete before attempting re-insertion.'

    try:
        with open('../userfunc/deployarchive/data/2022_All_sites_air_quality_hourly_avg.csv', 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')

            inserts = []
            for row in csv_reader:
                insert = {
                    'create': {
                        'date': row['date'],
                        'time': row['time'],
                        'location_name': row['location_name'],
                        'latitude': row['latitude'],
                        'longitude': row['longitude'],
                        'value': row['value'],
                        'parameter_name': row['parameter_name'],
                        'parameter_method_name': row['parameter_method_name'],
                        'parameter_description': row['parameter_description']
                    }
                }
                inserts.append(insert)
            
        bulker.bulk(es, inserts, index=AIR_QUALITY_HOURLY_AVG)
    except Exception as e:
        return f'{e}'
    return 'success'