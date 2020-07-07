import time
import base64
import requests
import json
import hashlib
import hmac
import urllib.parse


class BithumbAPI:

    def __init__(self, connect_key=None, secret_key=None):
        self.base_url = "https://api.bithumb.com"
        self.connect_key = connect_key
        self.secret_key = secret_key
    
    def get(self, path):
        """
        빗썸 Base Url을 Path와 합친 후 GET 요청을 보냅니다.
        """
        uri = urllib.parse.urljoin(self.base_url, path)

        response = requests.get(uri)
        if response.status_code != 200:
            raise Exception(f"get({path}) failed (status code: {response.status_code})")
        
        json_data = json.loads(response.text)
        if "status" in json_data and json_data["status"] == "0000":
            return json_data
        else:
            raise Exception(f"get({path}) failed (bithumb code: {json_data['status']}, message: {json_data['message']}) https://apidocs.bithumb.com/docs/err_code")

    def post(self, path, payload):
        """
        빗썸 Base Url을 Path와 합친 후 Payload와 함께 POST 요청을 보냅니다.
        """
        uri = urllib.parse.urljoin(self.base_url, path)

        nonce = str(int(time.time() * 1000))
        headers = {
            "Api-Key": self.connect_key,
            "Api-Sign": self.signature(path, payload, nonce),
            "Api-Nonce": nonce
        }

        response = requests.post(uri, headers=headers, data=payload)
        if response.status_code != 200:
            raise Exception(f"post({path}) failed (status code: {response.status_code})")
        
        json_data = json.loads(response.text)
        if "status" in json_data and json_data["status"] == "0000":
            return json_data
        else:
            raise Exception(f"post({path}) failed (bithumb code: {json_data['status']}, message: {json_data['message']}) https://apidocs.bithumb.com/docs/err_code")
    
    def signature(self, path, payload, nonce):
        """
        Path와 Payload 그리고 Nonce를 Secret Key로 싸이닝 합니다.
        """
        data = path + chr(0) + urllib.parse.urlencode(payload) + chr(0) + nonce
        h = hmac.new(self.secret_key.encode("utf-8"), data.encode("utf-8"), hashlib.sha512)
        return base64.b64encode(h.hexdigest().encode("utf-8")).decode("utf-8")


class BithumbPublicAPI:

    @staticmethod
    def ticker(order_currency="BTC", payment_currency="KRW"):
        """
        요청 당시 빗썸 거래소 가상자산 현재가 정보를 제공합니다.
        """
        path = f"/public/ticker/{order_currency}_{payment_currency}"
        return BithumbAPI().get(path)
    
    @staticmethod
    def orderbook(order_currency="BTC", payment_currency="KRW", count=30):
        """
        요청 당시 빗썸 거래소 가상자산 현재가 정보를 제공합니다.
        """
        path = f"/public/orderbook/{order_currency}_{payment_currency}?count={count}"
        return BithumbAPI().get(path)
    
    @staticmethod
    def transaction_history(order_currency="BTC", payment_currency="KRW", count=20):
        """
        빗썸 거래소 가상자산 거래 체결 완료 내역을 제공합니다.
        """
        path = f"/public/transaction_history/{order_currency}_{payment_currency}?count={count}"
        return BithumbAPI().get(path)
    
    @staticmethod
    def assets_status(order_currency="BTC"):
        """
        가상 자산의 입/출금 현황 정보를 제공합니다.
        """
        path = f"/public/assetsstatus/{order_currency}"
        return BithumbAPI().get(path)
    
    @staticmethod
    def btci():
        """
        빗썸 지수 (BTMI,BTAI) 정보를 제공합니다.
        """
        path = "/public/btci"
        return BithumbAPI().get(path)
    
    @staticmethod
    def candlestick(order_currency="BTC", payment_currency="KRW", chart_intervals="24h"):
        """
        시간 및 구간 별 빗썸 거래소 가상자산 가격, 거래량 정보를 제공합니다.
        """
        path = f"/public/candlestick/{order_currency}_{payment_currency}/{chart_intervals}"
        return BithumbAPI().get(path)


class BithumbPrivateAPI:

    def __init__(self, connect_key=None, secret_key=None):
        if not connect_key or not secret_key:
            raise Exception("private api init() failed : provide connect_key and secret_key")
        self.bithumb_api = BithumbAPI(connect_key=connect_key, secret_key=secret_key)
    
    def info_account(self, order_currency, payment_currency="KRW"):
        """
        회원 정보 및 코인 거래 수수료 정보를 제공합니다.
        """
        path = "/info/account"
        payload = {
            "order_currency": order_currency,
            "payment_currency": payment_currency
        }
        return self.bithumb_api.post(path, payload)
    
    def info_balance(self, currency="KRW"):
        """
        요청 당시 빗썸 거래소 가상자산 현재가 정보를 제공합니다.
        """
        path = "/info/balance"
        payload = {
            "currency": currency
        }
        return self.bithumb_api.post(path, payload)

    def info_wallet_address(self, currency="KRW"):
        """
        회원의 코인 입금 지갑 주소를 제공합니다.
        """
        path = "/info/wallet_address"
        payload = {
            "currency": currency
        }
        return self.bithumb_api.post(path, payload)

    def info_ticker(self, order_currency, payment_currency="KRW"):
        """
        회원의 가상자산 거래 정보를 제공합니다.
        """
        path = "/info/ticker"
        payload = {
            "order_currency": order_currency,
            "payment_currency": payment_currency
        }
        return self.bithumb_api.post(path, payload)

    def info_orders(self, order_currency, payment_currency="KRW", order_id=None, order_type=None, count=100, after=None):
        """
        회원의 매수/매도 등록 대기 또는 거래 중 내역 정보를 제공합니다.
        """
        path = "/info/orders"
        payload = {
            "order_currency": order_currency,
            "payment_currency": payment_currency,
            "count": count
        }
        if order_id or order_type:
            if order_id and order_type:
                payload["order_id"] = order_id
                payload["type"] = order_type
            else:
                raise Exception(f"private api orders() failed : provide both order_id and order_type")
        if after:
            payload["after"] = after
        return self.bithumb_api.post(path, payload)
    
    # NOT TESTED
    def info_order_detail(self, order_id, order_currency, payment_currency="KRW"):
        """
        회원의 매수/매도 체결 내역 상세 정보를 제공합니다.
        """
        path = "/info/order_detail"
        payload = {
            "order_id": order_id,
            "order_currency": order_currency,
            "payment_currency": payment_currency
        }
        return self.bithumb_api.post(path, payload)
    
    def info_user_transactions(self, order_currency, payment_currency="KRW", offset=0, count=20, searchGb=0):
        """
        회원의 거래 완료 내역 정보를 제공합니다.
        """
        path = "/info/user_transactions"
        payload = {
            "order_currency": order_currency,
            "payment_currency": payment_currency,
            "offset": offset,
            "count": count,
            "searchGb": searchGb
        }
        return self.bithumb_api.post(path, payload)

    def trade_place(self, order_currency, payment_currency="KRW", units=0.0, price=0, order_type="bid/ask"):
        """
        지정가 매수/매도 등록 기능을 제공합니다.
        """
        path = "/trade/place"
        payload = {
            "order_currency": order_currency,
            "payment_currency": payment_currency,
            "units": units,
            "price": price,
            "type": order_type
        }
        return self.bithumb_api.post(path, payload)
    
    def trade_cancel(self, order_id, order_type, order_currency, payment_currency="KRW"):
        """
        등록된 매수/매도 주문 취소 기능을 제공합니다.
        주문 취소 결과에 따른 취소 완료 개수는 Private API/Info/Orders detail을 통해 확인할 수 있습니다.
        """
        path = "/trade/cancel"
        payload = {
            "order_id": order_id,
            "type": order_type,
            "order_currency": order_currency,
            "payment_currency": payment_currency
        }
        return self.bithumb_api.post(path, payload)
    
    def trade_market_buy(self, order_currency, payment_currency="KRW", units=0.0):
        """
        시장가 매수 기능을 제공합니다.
        """
        path = "/trade/market_buy"
        payload = {
            "order_currency": order_currency,
            "payment_currency": payment_currency,
            "units": units
        }
        return self.bithumb_api.post(path, payload)
    
    def trade_market_sell(self, order_currency, payment_currency="KRW", units=0.0):
        """
        시장가 매도 기능을 제공합니다.
        """
        path = "/trade/market_sell"
        payload = {
            "order_currency": order_currency,
            "payment_currency": payment_currency,
            "units": units
        }
        return self.bithumb_api.post(path, payload)
    
    def trade_btc_withdrawal(self, currency, address, destination, units=0.0):
        """
        가상자산 출금 신청 기능을 제공합니다.
        """
        path = "/trade/btc_withdrawal"
        payload = {
            "currency": currency,
            "address": address,
            "destination": destination,
            "units": units
        }
        return self.bithumb_api.post(path, payload)

    def trade_krw_withdrawal(self, account, bank="011_농협은행", price=0):
        """
        원화(KRW) 출금 신청 기능을 제공합니다.
        """
        path = "/trade/krw_withdrawal"
        payload = {
            "bank": bank,
            "account": account,
            "price": price
        }
        return self.bithumb_api.post(path, payload)
