import requests


class SteamMarketCaseHistory:
    def __init__(self, auth_token: str):
        self.__cookies = {
            "steamLoginSecure": auth_token
        }
        self.__headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }

    def __parse_market_history_result(self, result):
        success = result.get("success")
        page_size = result.get("pagesize")
        total_count = result.get("total_count")
        start = result.get("start")

        # parsing items sold on market
        assets = result.get("assets")
        cs_items = None
        try:  # TODO: remove later
            cs_items = assets.get("730")
        except:
            print(assets)
        if not cs_items:  # checking if there is no cs items in history section
            return None

        items = cs_items.get("2")
        if not items:  # cases and some other stuff apparently under number "2" TODO: need to figure out what is "2"
            return None

        cases = []
        for k, v in items.items():
            item_name = v.get("name")
            item_market_name = v.get("market_name")
            item_market_hash = v.get("market_hash_name")

            if "case" in item_name.lower():
                cases.append({
                    "item_name": item_name,
                    "item_market_name": item_market_name,
                    "item_market_hash": item_market_hash
                })

        return {
            "success": success,
            "page_size": page_size,
            "total_count": total_count,
            "start": start,
            "cases": cases
        }

    def get_case_market_history_by_page(self, count=10, start=0):
        resp = requests.get("https://www.steamcommunity.com/market/myhistory", params={"count": count, "start": start},
                            cookies=self.__cookies, headers=self.__headers).json()

        success = resp.get("success")
        if not success:
            print(f"Failed to get market history, count: {count} | start_items_number: {start}")

        parsed_result = self.__parse_market_history_result(resp)

        return parsed_result

    def get_all_case_market_history(self):
        count = 50
        start = 0

        all_cases = []

        first_resp = self.get_case_market_history_by_page(count, start)
        if first_resp and first_resp.get("success"):
            all_cases += first_resp.get("cases")

        all_sales = first_resp.get("total_count")
        print(f"[SCANNING] getting items: {start + count} of {all_sales}")

        start += 50
        while start <= all_sales:
            print(f"[SCANNING] getting items: {start + count} of {all_sales}")
            market_history_resp = self.get_case_market_history_by_page(count, start)
            if market_history_resp and market_history_resp.get("success"):
                all_cases += market_history_resp.get("cases")

            start += 50

        return all_cases
