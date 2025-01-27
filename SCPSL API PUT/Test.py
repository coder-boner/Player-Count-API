import os
import logging
import requests
import json
import time
from filelock import FileLock
from typing import NoReturn  # Changed from Never to NoReturn

logger = logging.getLogger("slapi")

class Exceptions:
    class APIError(Exception):
        pass

    class APIRateLimited(Exception):
        pass

    class APIBadCredentials(Exception):
        pass

    class APINoCredentials(Exception):
        pass

class Config:
    base = "https://api.scpslgame.com/serverinfo.php"
    id_param = "id=30017"
    key_param = "key=wojRclHhzLFl3xMy6hXhGTge"
    params = ["players=true", "list=true", "nicknames=true", "online=true"]
    cache_dir = "cache"  # You can change this to your preferred cache directory

def _get_credentials() -> tuple:
    ID = os.getenv('SCPSL_ID', None)
    KEY = os.getenv('SCPSL_KEY', None)

    if ID is None or KEY is None:
        raise Exceptions.APINoCredentials('No API credentials found')
    logger.debug(f"API ID: {ID}")
    logger.debug(f"API KEY: {KEY}")
    return ID, KEY

def _create_exception(response: requests.Response) -> NoReturn:
    if response.json().get("error", None) == "ID must be Numeric":
        raise Exceptions.APIBadCredentials("API ID must be numeric")
    if response.json().get("error", None) == "Access denied":
        raise Exceptions.APIBadCredentials("API key is invalid")
    elif response.status_code == 429:
        raise Exceptions.APIRateLimited("API rate limited")
    else:
        raise Exceptions.APIError(f"API returned an unknown error: {response.json()}")

def _make_request() -> dict:
    ID, KEY = _get_credentials()
    URL = f"{Config.base}?{Config.id_param}{int(ID)}&{Config.key_param}{str(KEY)}"
    for param in Config.params:
        URL += f"&{param}"
    logger.debug(f"Requesting URL: {URL}")
    response = requests.get(URL)
    if response.status_code != 200:
        _create_exception(response)
    elif response.json().get("Success", None) != True:
        _create_exception(response)
    elif response.json().get("Success", None):
        return response.json()

def _store_cache(data: dict):
    if not os.path.exists(Config.cache_dir):
        os.makedirs(Config.cache_dir)
    cache_file = os.path.join(Config.cache_dir, "slapi_cache.json")
    lock = FileLock(f"{cache_file}.lock")
    with lock:
        data["Updated"] = time.time()
        logger.debug(f"Storing cache in {cache_file}")
        with open(cache_file, "w") as f:
            json.dump(data, f)

def update_cache():
    data = _make_request()
    _store_cache(data)
    logger.info("Cache updated successfully")

def blind_update_cache():
    success = False
    retries = 0
    while not success and retries < 6:
        try:
            update_cache()
            success = True
        except Exception as e:
            retries += 1
            logger.error(f"Failed to update cache - ({retries} / 6): {e}")
            time.sleep(5)

def get_player_count():
    try:
        data = _make_request()
        return data.get("PlayerCount", "Player count not available")
    except Exception as e:
        logger.error(f"Failed to get player count: {e}")
        return "Error retrieving player count"

# Usage
if __name__ == "__main__":
    player_count = get_player_count()
    print(f"Current player count: {player_count}")
