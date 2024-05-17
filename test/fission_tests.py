import pytest
import requests
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
        msgs = [
            {'content': 'Hello World', 'created_at': '2021-07-07T12:00:00.123456Z', 'id': 1, 'sentiment':0},
            {'content': 'Test Message', 'created_at': '2021-07-07T13:00:00.123456Z', 'id': 2, 'sentiment':0}
        ]
        # Expected output should trim the datetime and include all keys
        expected = [
            {'content': 'Hello World', 'created_at': '2021-07-07T12:00:00', 'id': 1, 'sentiment':0},
            {'content': 'Test Message', 'created_at': '2021-07-07T13:00:00', 'id': 2, 'sentiment':0}
        ]
        mocker.patch('flask.current_app.logger.info', return_value=None)
        assert parse_json(msgs) == expected

def test_parse_json_empty_input(app, mocker):
    with app.app_context():
        mocker.patch('flask.current_app.logger.info', return_value=None)
        # Testing the function with an empty list
        assert parse_json([]) == []

def test_parse_json_missing_keys(app, mocker):
    with app.app_context():
        mocker.patch('flask.current_app.logger.info', return_value=None)
        # Input where some messages are missing one or more keys
        msgs = [
            {'content': 'Incomplete', 'id': 3},  # missing 'created_at'
            {'created_at': '2021-07-07T14:00:00.123456Z', 'id': 4}  # missing 'content'
        ]
        # Expected output handles missing keys gracefully
        expected = [
            {'content': 'Incomplete', 'created_at': None, 'id': 3},
            {'content': None, 'created_at': '2021-07-07T14:00:00', 'id': 4}
        ]
        result = parse_json(msgs)
        # Custom assertion to handle possible None values in dictionary
        for res, exp in zip(result, expected):
            for key in ['content', 'created_at', 'id']:
                assert res.get(key) == exp.get(key)

    # You can also include additional test cases for malformed input, etc.
