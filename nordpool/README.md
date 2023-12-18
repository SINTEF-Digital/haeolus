# Test script to get spot price from nord pool (Day-ahead market API)
Based on Python example at https://marketdata.nordpoolgroup.com/docs/services/MarketData-DayAhead-v2/operations/AreaPrices

## Requirements
- pip install python-dotenv
## Important notes:
1. the Nord Pool API requires datetime in UTC.
2. the get_token() returns the access token. This expires after 1 hour.
3. the credentials for get_token() are in an environemnt file (.env) that has to be in the same directory as this script. This file is not tracked in git. You need to get an acquired a day-ahead license at NordPool https://www.nordpoolgroup.com/.

## How to test
- python3 day_ahead_market.py \
It saves on a json file the hourly price for up to the next 24 hours. The horizon lenght depends on the time this script is run. NordPool publishes the day-ahead prices around 13:00 CET/CEST.
- python3 print_day_ahead_market.py \
It prints out the day-ahead prices.


## License
Distributed under the EUPL 1.2. See LICENSE.md in the main repository for more information.

## Contact
Giancarlo Marafioti - giancarlo.marafioti@sintef.nmo
