from constants import STATIONS

def insert(es, bulker, data):       
    if not es.indices.exists(index=STATIONS):
        return f'{STATIONS} index does not exist'

    # Use count API to get the number of documents in the index
    document_count = es.count(index=STATIONS)['count']

    if(document_count > 0):
        return f'{STATIONS} already has data. Please delete before attempting re-insertion.'

    try:
        inserts = []
        for _, row in data.items():
            insert = {
                "station_name": row['station_name'],
                "url": row['url']
            }
            inserts.append(insert)
            
        result = bulker.bulk(es, inserts, index=STATIONS)
    except Exception as e:
        return f'{e}'
    return result