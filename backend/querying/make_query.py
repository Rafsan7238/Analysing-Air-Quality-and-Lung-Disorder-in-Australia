def make_query(es, data):
    query = data['query']
    response = es.sql.query(query=query, format='json', fetch_size=1000)
    return_rows = response['rows']
    columns = [col_def['name'] for col_def in response['columns']]

    while ('cursor' in response.keys()):
        cursor = response['cursor']
        response =  es.sql.query(format='json', cursor=cursor)
        return_rows += response['rows']

    return {'columns': columns, 'rows': return_rows}
