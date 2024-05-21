from mastodon import Mastodon
import time
from elasticsearch8 import Elasticsearch, helpers
import pytz
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime, timedelta, tzinfo

def parse_json(msg, analyzer):
    new_msg = {}

    new_msg['id'] = msg.get('id')

    raw_date = msg.get('created_at')
    if raw_date:
        new_msg['created_at'] = str(raw_date)[0:19]                    
        year = str(raw_date)[2:4]
        month = str(raw_date)[5:7]
        day = str(raw_date)[8:10]
        new_msg['date'] = f'{day}/{month}/{year}'
    else:
        new_msg['created_at'] = None

    new_msg['content'] = msg.get('content')
    
    try:
        new_msg['sentiment'] = analyzer.polarity_scores(new_msg.get('content')).get('compound')
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
    
    print(helpers.bulk(elastic_client, inserts, index='mastodon_observations'))
            
def ingest(recents_only = True, max_id = None):
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
    created_at = None
    toots = []
    utc = pytz.UTC
    if recents_only:
        print('fetching recents only')
        since_date = datetime.now().replace(tzinfo=utc) - timedelta(minutes=5)
        if len(doc)>0:
            val = doc[0]
            print(val)
            since_id = val['_source']['id']
    else:
        print('backfilling old')
        since_date = datetime.now().replace(tzinfo=utc) - timedelta(days=5) # a random post on 15/05/2024
        since_date = since_date.replace(tzinfo=utc)

        query = """
            SELECT created_at, id FROM mastodon_observations
            ORDER BY created_at ASC LIMIT 1
        """
        response = elastic_client.sql.query(query=query, format='json', fetch_size=5000)
        oldest_doc = response['rows'][0]
        print(oldest_doc)
        print(f'continuing retrieval of old data from {oldest_doc[0]}')
        max_id = max_id if max_id else oldest_doc[1]

    since_date = since_date.replace(tzinfo=utc)
    done = False
    while not done:
        print(f'fetching toots with since_id:{since_id}, max_id:{max_id}, and since the date:{since_date}')
        # Returns toots more recent than since_id, less recent than max_id
        toots = m.timeline(timeline='public', since_id=since_id, max_id=max_id, limit=100)
        to_add = []

        if not toots and len(toots) == 0:
            print('no toots retrieved')
            done = True

        for observation in toots:
            created_at = observation['created_at'].replace(tzinfo=utc)
            if created_at < since_date:
                print(f'since date {since_date} has been reached by toot at {created_at}. Ending loop')
                done = True
                break
            else:
                to_add.append(observation)

        if len(to_add) > 0:
            insert_observation_batch(elastic_client, to_add, analyzer)

        if toots and len(toots) > 0:
            max_id = toots[-1]['id']
            print(f'Toots had oldest date {created_at} and largest id {max_id}')
        else:
            print(f'toots was empty')

    print('function ending')
    return 'ok'

def main():
    return ingest()
    
def catch_up_history(data):
    max_id = data['max_id']
    return ingest(recents_only=False, max_id=max_id)                


if __name__ == '__main__':
    main()