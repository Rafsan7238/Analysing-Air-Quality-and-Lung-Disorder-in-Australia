from mastodon import Mastodon
import time
from elasticsearch8 import Elasticsearch, helpers
import pytz
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime, timedelta, tzinfo

def parse_json(msg, analyzer):
    new_msg = {}

    new_msg['id'] = msg['id']

    raw_date = msg.get('created_at')
    if raw_date:
        new_msg['created_at'] = str(raw_date)[0:19]                    
        year = str(raw_date)[2:4]
        month = str(raw_date)[5:7]
        day = str(raw_date)[8:10]
        new_msg['date'] = f'{day}/{month}/{year}'
    else:
        new_msg['created_at'] = None

    new_msg['content'] = msg['content']
    
    try:
        new_msg['sentiment'] = analyzer.polarity_scores(new_msg['content']).get('compound')
    except:
        new_msg['sentiment'] = 0

    return new_msg


def generate_docs(msgs):
    for msg in msgs:
        msg['_index'] = 'mastodon_observations'
        yield msg

def insert_observation_batch(elastic_client, observation_batch, analyzer):
    inserts = []
    for entry in observation_batch:
        parsed_msg = parse_json(entry, analyzer)
        inserts.append(parsed_msg)
    
    helpers.bulk(elastic_client, inserts, index='mastodon_observations')
            
def ingest(recents_only = True):
    print('mharvester invoked')
    elastic_client = Elasticsearch (
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs= False,
        basic_auth=('elastic', 'elastic'),
        request_timeout=30
    )

    m = Mastodon(
        api_base_url=f'https://mastodon.au'
    )

    analyzer = SentimentIntensityAnalyzer()

    print('fetching most recent id from index')
    # get latest ID
    page = elastic_client.search(
    index='mastodon_observations',
    scroll='1m',  # Length of time to keep the scroll window open    
    body={
        "query" : {
        "match_all" : { }
        },
        "sort": [
        {
            "created_at": {
            "order": "desc"
            }
        }
        ],
        "size": 1
        }
    )
    
    doc = page['hits']['hits']

    max_id = None
    since_id = None
    utc = pytz.UTC
    if recents_only:
        print('fetching recents only')
        since_date = datetime.now() - timedelta(minutes=5)
        if len(doc)>0:
            val = doc[0]
            since_id = val['_id']
    else:
        print('fetching old')
        since_date = datetime.now() - timedelta(days=5) # a random post on 15/05/2024

        query = """
            SELECT created_at, id FROM mastodon_observations
            ORDER BY created_at ASC LIMIT 1
        """
        response = elastic_client.sql.query(query=query, format='json', fetch_size=5000)
        oldest_doc = response['rows'][0]
        print(oldest_doc)
        print(f'continuing retrieval of old data from {oldest_doc[0]}')
        max_id = oldest_doc[1]

    since_date = since_date.replace(tzinfo=utc)
    done = False
    while not done:
        print(f'fetching toots with since_id:{since_id}, max_id:{max_id}, and up_to:{since_date}')
        # Returns toots more recent than since_id, less recent than max_id
        toots = m.timeline(timeline='public', since_id=since_id, max_id=max_id, limit=2000, remote=True)
        to_add = []
        if len(toots) == 0:
            done = True
        for observation in toots:
            created_at = observation['created_at'].replace(tzinfo=utc)
            if created_at < since_date:
                done = True
                break
            else:
                to_add.append(observation)

        insert_observation_batch(elastic_client, to_add, analyzer)
        
        print(f'Toots had oldest date {created_at} and oldest id {max_id}')
        max_id = toots[-1]['id']

    print('function ending')
    return 'ok'

def main():
    return ingest()
    
def catch_up_history():
    return ingest(recents_only=False)                


if __name__ == '__main__':
    main()