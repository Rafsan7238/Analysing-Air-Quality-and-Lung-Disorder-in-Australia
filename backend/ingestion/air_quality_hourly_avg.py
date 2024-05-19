from constants import AIR_QUALITY_HOURLY_AVG

def insert(es, bulker, data):       
    if not es.indices.exists(index=AIR_QUALITY_HOURLY_AVG):
        return f'{AIR_QUALITY_HOURLY_AVG} index does not exist'

    # Use count API to get the number of documents in the index
    document_count = es.count(index=AIR_QUALITY_HOURLY_AVG)['count']

    smallest_id = int(list(data.keys())[0])
    if(document_count > smallest_id + 1):
        return f'{AIR_QUALITY_HOURLY_AVG} already has data. Please delete before attempting re-insertion.'
    print('inserting')
    try:
        inserts = []
        for _, row in data.items():
            insert = {
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
            inserts.append(insert)
        print('inserts made')
        print('row')

        messages = []
        for ok, response in bulker.streaming_bulk(es, inserts, index=AIR_QUALITY_HOURLY_AVG, request_timeout=120):
            if not ok:
                messages.append(response)
        print('bulked')
    except Exception as e:
        return str(e)
    return ' '.join(messages)