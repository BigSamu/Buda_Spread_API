from services.markets import MarketService
from services.tickers import TickerService
from services.base import BaseAPIClient

class BudaAPI:
    def __init__(self):
        self.markets = MarketService()
        self.tickers = TickerService()


# Instantiate the main API class
buda_api = BaseAPIClient()
