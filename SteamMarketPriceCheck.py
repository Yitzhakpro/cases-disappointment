from typing import Tuple
import requests


class SteamMarketPriceCheck:
    def __init__(self):
        self.cache = {}
        self.__headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }

    def check_price(self, market_hash_name: str) -> Tuple[float, bool]:
        """
        :param market_hash_name: market hash name to check
        :return: the value of the item and True in case value retried from api and False in case retrived from cache
        """

        if market_hash_name in self.cache:
            # print(f"Found price in cache for: {market_hash_name} = {self.cache[market_hash_name]}")
            return self.cache[market_hash_name], False

        price_check_url = "https://steamcommunity.com/market/priceoverview"
        query = {
            "appid": "730",
            "market_hash_name": market_hash_name
        }

        price_resp = requests.get(price_check_url, params=query, headers=self.__headers)
        price_resp_json = price_resp.json()

        if not price_resp or not price_resp_json.get("success"):
            print(price_resp.status_code)
            raise Exception(f"could not get price check for: {market_hash_name}")

        lowest_price = float(price_resp_json.get("lowest_price")[1::])
        # cache the response
        self.cache[market_hash_name] = lowest_price

        return lowest_price, True
