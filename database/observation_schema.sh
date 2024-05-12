curl -XPUT -k 'https://127.0.0.1:9200/observations' \
   --user 'elastic:elastic' \
   --header 'Content-Type: application/json' \
   --data '{
    "settings": {
        "index": {
            "number_of_shards": 10,
            "number_of_replicas": 1
        }
    },
    "mappings": {
        "properties": {
            "wmo": {
                "type": "text"
            },
            "name": {
                "type": "text"
            },
            "history_product": {
                "type": "text"
            },
            "local_date_time": {
                "type": "text"
            },
            "local_date_time_full": {
                "type": "text"
            },
            "lat": {
                "type": "float"
            },
            "lon": {
                "type": "float"
            },
            "apparent_t": {
                "type": "float"
            },
            "cloud": {
                "type": "text"
            },
            "cloud_base_m": {
                "type": "text"
            },
            "cloud_oktas": {
                "type": "text"
            },
            "cloud_type": {
                "type": "text"
            },
            "cloud_type_id": {
                "type": "text"
            },
            "delta_t": {
                "type": "text"
            },
            "gust_kmh": {
                "type": "text"
            },
            "gust_kt": {
                "type": "text"
            },
            "dewpt": {
                "type": "text"
            },
            "press": {
                "type": "text"
            },
            "press_msl": {
                "type": "text"
            },
            "press_qnh": {
                "type": "text"
            },
            "press_tend": {
                "type": "text"
            },
            "rain_trace": {
                "type": "text"
            },
            "sea_state": {
                "type": "text"
            },
            "swell_dir_worded": {
                "type": "text"
            },
            "swell_height": {
                "type": "text"
            },
            "swell_period": {
                "type": "text"
            },
            "vis_km": {
                "type": "text"
            },
            "weather": {
                "type": "text"
            },
            "wind_dir": {
                "type": "text"
            },
            "wind_spd_kmh": {
                "type": "text"
            },
            "wind_spd_kt": {
                "type": "text"
            }
        }
    }
}'  | jq '.'
