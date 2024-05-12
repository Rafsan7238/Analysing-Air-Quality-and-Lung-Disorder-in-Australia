import csv
from constants import RAINFALL_BRISBANE

def insert(es, bulker):       
    if not es.indices.exists(index=RAINFALL_BRISBANE):
        return f'{RAINFALL_BRISBANE} index does not exist'

    # Use count API to get the number of documents in the index
    document_count = es.count(index=RAINFALL_BRISBANE)['count']

    if(document_count > 0):
        return f'{RAINFALL_BRISBANE} already has data. Please delete before attempting re-insertion.'

    try:
        with open('../userfunc/deployarchive/data/bom_historic_data/rainfall_cities/Brisbane.csv', 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')

            inserts = []
            for row in csv_reader:
                insert = {
                    'create': {
                    "Month": row['Month'],
                    "Monthly Precipitation Total (millimetres)": row['Monthly Precipitation Total (millimetres)'],
                    "Product code": row['Product code'],
                    "Quality": row['Quality'],
                    "Station number": row['Station number'],
                    "Year": row['Year']
                }
                }
                inserts.append(insert)
            
        bulker.bulk(es, inserts, index=RAINFALL_BRISBANE)
    except Exception as e:
        return f'{e}'
    return 'success'