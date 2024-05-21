import pytest
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from backend.elastic_client_provider import get_client
from backend.harvesters.BOM.addobservations import call_bom
from backend.harvesters.Mastodon.mharvester import parse_json, generate_docs

from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    return app

def test_call_bom_success(app,mocker):
    with app.app_context():
        # Setting up the mock for requests.get to return a successful response
        mock_response = mocker.MagicMock(status_code=200)
        mock_response.json.return_value = {"data": "example"}
        mocker.patch('requests.get', return_value=mock_response)
        mocker.patch('flask.current_app.logger.info', return_value=None)
        # Calling the function
        station_name, result = call_bom("TestStation", "http://example.com")

        # Assertions to check the expected output
        assert station_name == "TestStation"
        assert result == {"data": "example"}, "JSON response should be returned on success"

def test_call_bom_failure(app, mocker):
    with app.app_context():
        # Setting up the mock for requests.get to return a non-successful response
        mock_response = mocker.MagicMock(status_code=404)  # Example of a failed status code
        mocker.patch('requests.get', return_value=mock_response)
        mocker.patch('flask.current_app.logger.info', return_value=None)
        
        # Calling the function
        station_name, result = call_bom("TestStation", "http://example.com")

        # Assertions to check the expected output
        assert station_name == "TestStation"
        assert result is None, "None should be returned if the response is not 200"


# test elastic search client
def test_get_client(app, mocker):
    with app.app_context():
        mocker.patch('flask.current_app.logger.info', return_value=None)
        assert str(type(get_client())) == "<class 'elasticsearch8.Elasticsearch'>"


def test_parse_json_normal_input(app, mocker):
    with app.app_context():
        # Input with a typical list of message dictionaries
        msgs = {'content': 'Hello World', 'created_at': '2021-07-07T12:00:00.123456Z', 'id': 1, 'sentiment':None}
        # Expected output should trim the datetime and include all keys
        expected = {'id': 1, 'created_at': '2021-07-07T12:00:00', 'date': '07/07/21', 'content': 'Hello World', 'sentiment': 1.0}
        mocker.patch('flask.current_app.logger.info', return_value=None)

        mock_analyzer = mocker.Mock(spec=SentimentIntensityAnalyzer)

        # Define the return value of the polarity_scores method
        mock_analyzer.polarity_scores.return_value = {
            'neg': 0.0,
            'neu': 0.0,
            'pos': 1.0,
            'compound': 1.0
        }
        assert parse_json(msgs, mock_analyzer) == expected

def test_parse_json_empty_input(app, mocker):
    with app.app_context():
        mocker.patch('flask.current_app.logger.info', return_value=None)
        # Define the return value of the polarity_scores method
        mock_analyzer = mocker.Mock(spec=SentimentIntensityAnalyzer)

        mock_analyzer.polarity_scores.return_value = {
            None
        }
        # Testing the function with an empty list
      
        assert parse_json({}, mock_analyzer) == {'id': None, 'created_at': None, 'content': None, 'sentiment': 0}

def test_parse_json_missing_keys(app, mocker):
    with app.app_context():
        mocker.patch('flask.current_app.logger.info', return_value=None)
        # Input where some messages are missing one or more keys
        msgs = {'content': 'Incomplete', 'id': 3}  # missing 'created_at'
           
        # Expected output handles missing keys gracefully
        expected = {'content': 'Incomplete', 'created_at': None, 'id': 3}
            

        mock_analyzer = mocker.Mock(spec=SentimentIntensityAnalyzer)

        # Define the return value of the polarity_scores method
        mock_analyzer.polarity_scores.return_value = {
            'neg': 0.0,
            'neu': 0.0,
            'pos': 1.0,
            'compound': 1.0
        }
        # Custom assertion to handle possible None values in dictionary
        assert parse_json(msgs, mock_analyzer) == {'id': 3, 'created_at': None, 'content': 'Incomplete', 'sentiment': 1.0}

    # You can also include additional test cases for malformed input, etc.
