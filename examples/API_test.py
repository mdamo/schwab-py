from schwab import auth, client
import schwab
import json
from dataclasses import dataclass
from datetime import datetime


api_key = ""
app_secret = ""
redirect_uri = "https://127.0.0.1"
token_path = './examples/token.json'

try:
    c = auth.client_from_token_file(token_path, api_key, app_secret)
except FileNotFoundError:
    c = auth.client_from_manual_flow(
        api_key, app_secret, redirect_uri, token_path)

r = c.get_quotes(symbols=['BRK/B','SPY'])
#r = c.get_instruments(symbols=['SPY'],projection=schwab.client.Client.Instrument.Projection.SYMBOL_SEARCH)
assert r.status_code == 200, r.raise_for_status()
res = r.json()
print(res)

#r = c.get_price_history('AAPL',
#        period_type=client.Client.PriceHistory.PeriodType.YEAR,
#        period=client.Client.PriceHistory.Period.TWENTY_YEARS,
#        frequency_type=client.Client.PriceHistory.FrequencyType.DAILY,
#        frequency=client.Client.PriceHistory.Frequency.DAILY)
#assert r.status_code == 200, r.raise_for_status()
#print(json.dumps(r.json(), indent=4))
