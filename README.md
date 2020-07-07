# PyBithumb API

Python Wrapper for Bithumb REST API

```python
from bithumb_api import BithumbPublicAPI, BithumbPrivateAPI

# Public APIs
result = BithumbPublicAPI.ticker("BTC", "KRW")
result = BithumbPublicAPI.orderbook("ALL", 5)
result = BithumbPublicAPI.transaction_history()
result = BithumbPublicAPI.assets_status()
result = BithumbPublicAPI.btci()
result = BithumbPublicAPI.candlestick()

# Private APIs
api = BithumbPrivateAPI("connect-key", "secret-key")
result = api.info_account("BTC")
result = api.info_balance("BTC")
result = api.info_wallet_address("BTC")
result = api.info_ticker("BTC")
result = api.info_orders("BTC")
result = api.info_user_transactions("BTC")
result = api.trade_place("BTC", "KRW", 1.2, 500000, "bid")
result = api.trade_cancel("1234", "bid", "BTC")
result = api.trade_market_buy("BTC", units=1.0)
result = api.trade_market_sell("BTC", units=200.0)
result = api.trade_btc_withdrawal("BTC", "123456", "111111", 12.0)
result = api.trade_krw_withdrawal("33333", price=1259931)
```

# Author

Kevin Kim
