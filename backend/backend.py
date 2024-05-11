import json

from constants import ASTHMA_BY_REGION_INDEX_NAME, HIST_TWEET_INDEX_NAME
from elastic_client_provider import get_bulker, get_client
from index_creation.create_asthma_by_region_index import create_asthma_by_region_index
from index_creation.create_historic_tweets_index import create_historic_tweets_index
from static.historic_tweet_sentiments import insert_hist_tweets
from static.asthma_by_region import insert_region_asthma

def insert_hist_tweets_endpoint():
    try:
        es = get_client()
        bulker = get_bulker()

        res = insert_hist_tweets(es, bulker)

        return json.dumps({'result': res})
    except Exception as e:
        return json.dumps(e)
    
def insert_region_asthma_endpoint():
    try:
        es = get_client()
        bulker = get_bulker()

        res = insert_region_asthma(es, bulker)

        return json.dumps({'result': res})
    except Exception as e:
        return json.dumps(e)

def create_indexes_endpoint():
    try:    
        es = get_client()

        results = dict()
        results[HIST_TWEET_INDEX_NAME] = create_historic_tweets_index(es)
        results[ASTHMA_BY_REGION_INDEX_NAME] = create_asthma_by_region_index(es)
       
        return json.dumps(results)
    except Exception as e:
        return json.dumps(e)


### ^^ insert x endpoint()

###############################
# air quality vs lung disease 
def query_elastic(index, query):

    es = get_client()
    list_of_docs = []

    # Initialize the scroll
    scroll = es.search(
        index=index,
        body=query,
        scroll='2m',  # Keep the search context alive for 2 minutes
        size=10000  # Number of results per page
    )

    # Keep track of the scroll ID
    scroll_id = scroll['_scroll_id']

    # Fetch the initial page of results
    for doc in scroll['hits']['hits']:
        list_of_docs.append(doc['_source'])

    # Use the scroll ID to fetch the next batch of documents
    while True:
        response = es.scroll(scroll_id=scroll_id, scroll='2m')
        print('response', response)
        # Break the loop if there are no more documents
        if not response['hits']['hits']:
            break
        
        for doc in response['hits']['hits']:
            list_of_docs.append(doc['_source'])

    # Clean up the scroll context
    es.clear_scroll(scroll_id=scroll_id)
    return list_of_docs

def get_air_quality_hourly_avg():
    # get 2022_All_sites_air_quality_hourly_avg, 
    # select parameter_names = ['CO', 'PM10', 'PM2.5', 'O3', 'SO2']
    try: 
        selected_parameters = ['CO', 'PM10', 'PM2.5', 'O3', 'SO2']
        query = {"query": {"terms": {"parameter_name": selected_parameters}}}
        list_of_docs = query_elastic("air_quality_hourly_avg", query)
        return jsonify({"success": True, "data": list_of_docs}), 200

    except Exception as e:
        return json.dumps(e) 
    

def get_lung_cancer(request):
    # get all lung cancer data aihw_cimar_mortality_persons_gccsa_2009
 
    try: 
        data = json.loads(request.body)

        # Retrieve data from JSON, defaulting to 'Guest' if not found
        index = data.get('index')

        if index not in ['mortality_persons', 'mortality_females', 'mortality_males']:
            return jsonify({"success": False, "data": "incorrect index"}), 400

        query = {"query": {"match_all": {}}}
        list_of_docs = query_elastic(index)

        return jsonify({"success": True, "data": list_of_docs}), 200

    except Exception as e:
        return json.dumps(e) 
    # merge with census_by_cob_data abs_2021census_g21a_aust_gccsa
    # join on inner, ['gccsa_code', 'gccsa_name']
    


def get_census_by_inc_emp():
    # return census data 
    try: 
        
        index = 'census_g21b'
        query = {"query": {"match_all": {}}}
        list_of_docs = query_elastic(index)

        return jsonify({"success": True, "data": list_of_docs}), 200

    except Exception as e:
        return json.dumps(e) 

    pass

#############################
# weather vs sentiment 

def get_historic_tweet_sentiment():
    # return hiostoric tweet sentiment
    pass 

def get_rainfall_data():
    # get all cities, 
    # group by month
    # get mean
    pass 

def get_temperature_data():
    # get all cities, 
    # group by month
    # get mean
    pass 
