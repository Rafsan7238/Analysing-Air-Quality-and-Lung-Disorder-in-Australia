import csv
from constants import TEMPERATURE_SYDNEY

def insert_region_asthma(es, bulker):       
    if not es.indices.exists(index=TEMPERATURE_SYDNEY):
        return f'{TEMPERATURE_SYDNEY} index does not exist'

    # Use count API to get the number of documents in the index
    document_count = es.count(index=TEMPERATURE_SYDNEY)['count']

    if(document_count > 0):
        return f'{TEMPERATURE_SYDNEY} already has data. Please delete before attempting re-insertion.'

    try:
        with open('../userfunc/deployarchive/data/bom_historic_data/temperature_cities/Sydney.csv', 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')

            inserts = []
            for row in csv_reader:
                insert = {
                    'create': {
                    "Bureau of Meteorology station number": row['Bureau of Meteorology station number'],
                    "Mean maximum temperature (°C)": row['Mean maximum temperature (°C)'],
                    "Month": row['Month'],
                    "Product code": row['Product code'],
                    "Quality": row['Quality'],
                    "Year": row['Year']
                }
                }
                inserts.append(insert)
            
        bulker.bulk(es, inserts, index=TEMPERATURE_SYDNEY)
    except Exception as e:
        return f'{e}'
    return 'success'