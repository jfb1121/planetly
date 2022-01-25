from typing import Callable
from flask import Flask
from itsdangerous import json
from mongoengine import get_connection
import pytest


BASE_URL = '/temperatures/'

@pytest.mark.skip
def test_list_all_records(client, tear_downdb):
    """
    tests the GET function for checking valid responses being delivered.
    """
    # check empty database returns empty response
    res = client.get(BASE_URL)
    assert res.json == []

    service = _get_service()
    service.add_temperature_reading("foo", "2022-01-01", 5, 0)

    res = client.get(BASE_URL)
    response_data = res.json
    print(response_data)
    expected_keys = ["city_name", "recording_date", "average_temperature",
                     "average_temperature_uncertainty", "created_at"]
    assert set(expected_keys).issubset(set(response_data[0].keys()))
    assert len(response_data) == 1

    tear_downdb()

@pytest.mark.skip
def test_create_record(client: Flask, tear_downdb):
    """
    Checks if the POST function works as expected
    """
    # check we can create a new record
    new_record = {
        "city_name": "foo",
        "recording_date": "2022-01-01",
        "average_temperature": 5,
        "average_temperature_uncertainty": 0,
    }
    res = client.post(BASE_URL, json=new_record,
                      content_type="application/json")
    assert res.status_code == 200

    # check creating a duplicate record fails wit appropriate response
    res = client.post(BASE_URL, json=new_record,
                      content_type="application/json")
    assert res.status_code == 422
    assert res.json['message'] == "resource already exists"
    tear_downdb()

@pytest.mark.skip
def test_list_hottest(client: Flask, tear_downdb):
    """
    Checks if the GET function works with appropriate query string params
    """
    url = f"{BASE_URL}/ChasingSummer"

    # this test needs some setup, as we want some records to exist in the
    #  database

    service = _get_service()

    for i in range(1, 6):
        service.add_temperature_reading("foo", f"2020-0{i}-01", i, i+1)

    query = {
        "fromDate": "2020-01-01",
        "limit": 2
    }

    res = client.get(url, query_string=query, follow_redirects=True)
    response_json = res.json
    # request respects the query limit
    assert len(response_json) == query["limit"]
    firs_obj = response_json[0]
    # the hottest of the test data
    assert firs_obj["average_temperature"] == 5

    query["toDate"] = "2019-01-01"
    res = client.get(url, query_string=query, follow_redirects=True)
    assert res.status_code == 405
    assert res.json["message"] == "Invalid query"

@pytest.mark.skip
def test_get_record(client: Flask, tear_downdb: Callable):
    """
    tests if getting a single record by city and date works
    """
    date = "2020-01-01"
    city_name = "foo"
    url = f"{BASE_URL}/{city_name}/{date}"
    # test not found
    res = client.get(url, follow_redirects=True)
    assert res.status_code == 404

    service = _get_service()
    service.add_temperature_reading(city_name, date, 0.0, 0.0)

    res = client.get(url, follow_redirects=True)
    assert res.status_code == 200
    assert res.json["city_name"] == city_name

    date_for_assert = service.date_helper(date).date()
    assert service.date_helper(res.json["recording_date"]).date() == \
        date_for_assert
    assert res.json["average_temperature"] == 0.0
    assert res.json["average_temperature_uncertainty"] == 0.0

    tear_downdb()

@pytest.mark.skip
def test_create_record_by_name_date(client: Flask, tear_downdb: Callable):
    """
    tests POST for record creation.
    """
    date = "2020-01-01"
    city_name = "foo"
    url = f"{BASE_URL}/{city_name}/{date}"
    data = {
        "average_temperature": 0,
        "average_temperature_uncertainty": 0
    }
    res = client.post(url, json=data, follow_redirects=True)
    assert res.status_code == 200
    # test creation only works once
    res = client.post(url, json=data, follow_redirects=True)
    assert res.status_code == 422

    tear_downdb()



def test_update_record_by_name_date(client, tear_downdb):
    # create a record that needs to be updated.  
    date = "2020-01-01"
    city_name = "foo"
    url = f"{BASE_URL}/{city_name}/{date}"
    data = {
        "average_temperature": 1,
        "average_temperature_uncertainty": 1
    }  
    service = _get_service()
    # check cannot update non existent entry
    res = client.put(url, json=data, follow_redirects=True)
    assert res.status_code == 404
    service.add_temperature_reading(city_name, date, 0.0, 0.0)
    # check update is possible
    res = client.put(url, json=data, follow_redirects=True)
    assert res.status_code == 200
    
    # check values actually got updated. 
    rec = service.get_recorded_avg_temp(city_name, date)
    assert rec["average_temperature"] == data["average_temperature"]
    assert rec["average_temperature_uncertainty"] == \
        data["average_temperature_uncertainty"]

    tear_downdb()




def _get_service():
    from planetly.services.temperature_recording_service import \
        TemperatureRecordingService

    service = TemperatureRecordingService()

    return service
