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
                "Month": row['Month'],
                "Monthly Precipitation Total (millimetres)": row['Monthly Precipitation Total (millimetres)'],
                "Product code": row['Product code'],
                "Quality": row['Quality'],
                "Station number": row['Station number'],
                "Year": row['Year']
            }
            inserts.append(insert)
            
        result = bulker.bulk(es, inserts, index=index_name)
    except Exception as e:
        return f'{e}'
    return result