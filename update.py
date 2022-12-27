import os
from dotenv import load_dotenv
import requests
from requests.structures import CaseInsensitiveDict
from miflora.miflora_poller import (
    MI_BATTERY,
    MI_CONDUCTIVITY,
    MI_LIGHT,
    MI_MOISTURE,
    MI_TEMPERATURE,
    MiFloraPoller,
)
import datetime
from btlewrap import BluepyBackend, GatttoolBackend, PygattBackend, available_backends
import logging

backend = GatttoolBackend

# FUNCTIONS
def get_sensor_data(mac, uuid):
    """
    Returns a dictionary with the sensor data
    """
    data = {}
    data["uuid"] = uuid
    data["mac"] = mac
    data["battery"] = 1
    data["conductivity"] = 1
    data["light"] = 1
    data["moisture"] = 1
    data["temperature"] = 1
    data["timestamp"] = 1
    return data

def poll(mac, uuid, log_file):
    """
    Polls the sensor and returns a dictionary with the sensor data
    """
    try:
        poller = MiFloraPoller(mac, GatttoolBackend)
        data = {}
        data["uuid"] = uuid
        data["mac"] = mac
        data["battery"] = poller.parameter_value(MI_BATTERY)
        data["conductivity"] = poller.parameter_value(MI_CONDUCTIVITY)
        data["light"] = poller.parameter_value(MI_LIGHT)
        data["moisture"] = poller.parameter_value(MI_MOISTURE)
        data["temperature"] = poller.parameter_value(MI_TEMPERATURE)
        data["timestamp"] = 1 
        return data
    except Exception as e:
        logging.error("Error while polling sensor: %s", e)
        return None

def get_headers(BEE_HOME_TOKEN):
    """
    Returns the headers for the request
    """
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer " + BEE_HOME_TOKEN

def get_config(BEE_HOME_ENDPOINT, BEE_HOME_TOKEN):
    """
    Returns the configuration from the server
    """
    headers = get_headers(BEE_HOME_TOKEN)
    config_response = requests.get(url=BEE_HOME_ENDPOINT, headers=headers)
    # validate response
    if config_response.status_code  != 200:
        raise requests.ConnectionError("Expected status code 200, but got" + str(config_response.status_code))
    return config_response.json()

def post_data(BEE_HOME_ENDPOINT, BEE_HOME_TOKEN, data):
    """
    Posts the data to the server
    """
    headers = get_headers(BEE_HOME_TOKEN)
    data_post = requests.post(url=BEE_HOME_ENDPOINT, json=data, headers=headers)
    if data_post.status_code != 200:
        raise requests.ConnectionError("Expected status code 200, but got" + str(data_post.status_code))
    return data_post.json()



if __name__ == "__main__":
    # do not log logging.info
    logging.getLogger().setLevel(logging.ERROR)
    # load environment variables
    load_dotenv()
    BEE_HOME_TOKEN = os.getenv('BEE_HOME_TOKEN')
    BEE_HOME_ENDPOINT = os.getenv('BEE_HOME_ENDPOINT')

    if BEE_HOME_TOKEN is None:
        raise ValueError("BEE_HOME_TOKEN is not set")
    if BEE_HOME_ENDPOINT is None:
        raise ValueError("BEE_HOME_ENDPOINT is not set")


    # retrieve data from sensors
    config = get_config(BEE_HOME_ENDPOINT, BEE_HOME_TOKEN)
    sensors = config.get("sensors")
    data = []
    for sensor in sensors:
        mac = sensor.get("mac")
        uuid = sensor.get("uuid")
        try:
            data.append(poll(mac, uuid))
        except Exception as e:
            logging.error("Error while polling sensor: %s", e + " mac: " + mac + " uuid: " + uuid)
    
    # post data
    post_data(BEE_HOME_ENDPOINT, BEE_HOME_TOKEN, data)
    logging.info("Updated data for %s sensors", len(data))