# See readme.md
import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, json, os, sys ,logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
import numpy as np

logging.basicConfig(filename='nordpool.log', level=logging.DEBUG)

# return current time in UTC
def get_current_time(start_of_hour: bool = False):
    if start_of_hour:
        return datetime.utcnow().replace(microsecond=0, second=0, minute=0)
    else:
        return datetime.utcnow().replace(microsecond=0)

# return start time as string in RFC3339 - e.g. 2019-05-30T23:59:59Z
def _start_time(dt):
    return dt.isoformat("T") + "Z"
# return end time as string in RFC3339 - e.g. 2019-05-30T23:59:59Z (default is dt/current_time + 24 hours)
def _end_time(dt, horizon_hours=24):
    return (dt + timedelta(hours=horizon_hours)).isoformat("T") + "Z"

def _get_token():
    url = "https://sts.nordpoolgroup.com/connect/token"
    load_dotenv()
    user = os.getenv("user")
    password = os.getenv("password")

    payload = f"grant_type=password&scope=marketdata_api&username={user}&password={password}"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic Y2xpZW50X21hcmtldGRhdGFfYXBpOmNsaWVudF9tYXJrZXRkYXRhX2FwaQ=="
    }
    response = requests.request("POST", url, data=payload, headers=headers).json()
    return response['token_type'] + ' ' + response['access_token']


def get_ahead_prices(start: datetime, horizon_hours: int):
    data_j = []
    headers = {
        # Request headers
        'Accept-Encoding': '',
        'Authorization': _get_token(),
    }

    # Get the current time in UTC

    params = urllib.parse.urlencode({
        # Request parameters
        'deliveryarea': 'NO4',          # This is the delivery area Raggovidda wind park is
        'status': 'O',                  # Get the official prices
        'currency': 'EUR',              # Select EUR/MWh
        'startTime': _start_time(start),   # Start time in UTC
        'endTime': _end_time(start, horizon_hours=horizon_hours),       # End time in UTC
    })

    try:
        conn = http.client.HTTPSConnection('marketdata-api.nordpoolgroup.com')
        conn.request("GET", "/dayahead/prices/area?%s" % params, "{body}", headers)
        logging.info(f'NordPool API request made with the following parameters {urllib.parse.unquote(params)}')
        response = conn.getresponse()
        data = response.read()
        if response.status == 200:
            data_j = json.loads(data.decode('utf8').replace("'", '"'))
        else:
            error=f'NordPool HTTPS response is  {response.status}. See https://marketdata.nordpoolgroup.com/docs/services/MarketData-DayAhead-v2/operations/AreaBlockPrices \n'
            logging.error(error)
            sys.stderr.write(error)
            # TO DO if necessary: we could use the previous price as backup solution here or we could try to make a new request, depending on the response.status code.
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    return data_j


def to_prices_only_array(json_data: list):
    # TODO? Sort?
    logging.warning("prices only list is not guaranteed to be sorted")
    res = []
    if json_data:
        for e in json_data[0]["values"]:
            res.append(e["value"])
    return np.array(res)


def write_json_file(json_data: list, file_name: str):
    data_jsons = json.dumps(json_data, indent=2)

    with open(file_name, "w") as outfile:
        outfile.write(data_jsons)
    logging.info(f'Day-ahead market price written in {file_name}')


def example():
    start = get_current_time(start_of_hour=True)
    file_name = "day_ahead.json"
    data = get_ahead_prices(start, 24)
    pl = to_prices_only_array(data)
    print(pl)
    write_json_file(data, file_name)



if __name__ == "__main__":
    example()
