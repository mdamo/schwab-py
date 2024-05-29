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

class xAsset:
    def __init__(self, dic_json: dict) -> None:
        self.json = dic_json
        self.symbol = self.json["symbol"]
        self.assetMainType = self.json['assetMainType']
        self.assetSubType = self.json['assetSubType']
        self.quoteType = self.json['quoteType']
        self.realtime = self.json['realtime']
        self.ssid = self.json['ssid']

    @property
    def askPrice(self):
        return self.json['extended']['askPrice']

    @property
    def askSize(self):
        return self.json['extended']['askSize']

            #self.lastPrice = self.json['extended']['lastPrice']
            #self.lastSize = self.json['extended']['lastSize']
            #self.mark = self.json['extended']['mark']
            #self.quoteTime = self.json['extended']['quoteTime']
            #self.totalVolume = self.json['extended']['totalVolume']
            #self.tradeTime = self.json['extended']['tradeTime']

@dataclass
class Extended:
    askPrice: float
    askSize: int
    bidPrice: float
    bidSize: int
    lastPrice: float
    lastSize: int
    mark: float
    quoteTime: str
    totalVolume: int
    tradeTime: int

    def from_timestamp_to_string(self,
                                 t: str,
                                 format: str = '%Y%m%d %H:%M:%S') -> str:
        return datetime.fromtimestamp(float(t)/1000).strftime(format)

    def __post_init__(self):
        self.quoteTime = self.from_timestamp_to_string(t=self.quoteTime)

@dataclass
class Asset:
    symbol: str
    assetMainType: str
    assetSubType: str
    quoteType: str
    realtime: str
    ssid: str
    extended: Extended
    #quote: dict[Quote]

r = c.get_quotes(symbols=['SPY'])
#r = c.get_instruments(symbols=['SPY'],projection=schwab.client.Client.Instrument.Projection.SYMBOL_SEARCH)
assert r.status_code == 200, r.raise_for_status()
res = r.json()
print(res)
e = Extended(askPrice=res['SPY']['extended']['askPrice'],
             askSize=res['SPY']['extended']['askSize'],
             bidPrice=res['SPY']['extended']['bidPrice'],
             bidSize=res['SPY']['extended']['bidSize'],
             lastPrice=res['SPY']['extended']['lastPrice'],
             lastSize=res['SPY']['extended']['lastSize'],
             mark=res['SPY']['extended']['mark'],
             quoteTime=res['SPY']['extended']['quoteTime'],
             totalVolume=res['SPY']['extended']['totalVolume'],
             tradeTime=res['SPY']['extended']['tradeTime'])

s = Asset(assetMainType=res['SPY']['assetMainType'], symbol=res['SPY']['symbol'], assetSubType=res['SPY']['assetSubType'], quoteType=res['SPY']['quoteType'], realtime=res['SPY']['realtime'], ssid=res['SPY']['ssid'], extended=e)
print(s.extended.quoteTime)

#r = c.get_price_history('AAPL',
#        period_type=client.Client.PriceHistory.PeriodType.YEAR,
#        period=client.Client.PriceHistory.Period.TWENTY_YEARS,
#        frequency_type=client.Client.PriceHistory.FrequencyType.DAILY,
#        frequency=client.Client.PriceHistory.Frequency.DAILY)
#assert r.status_code == 200, r.raise_for_status()
#print(json.dumps(r.json(), indent=4))
