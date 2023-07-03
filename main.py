import math
import time
from SteamMarketCaseHistory import SteamMarketCaseHistory
from SteamMarketPriceCheck import SteamMarketPriceCheck


def main():
    secure_cookie = input("Please enter your steam secure cookie (steamLoginSecure): ")

    case_history_client = SteamMarketCaseHistory(secure_cookie)
    price_checker_client = SteamMarketPriceCheck()

    all_cases = case_history_client.get_all_case_market_history()

    total_val = 0

    check_price_req_count = 0
    start_time = time.time()

    for case_object in all_cases:
        hash_name = case_object.get("item_market_hash")

        if check_price_req_count >= 20:
            need_to_wait = math.ceil(60 - (time.time() - start_time))
            print(f"[PAUSE] Waiting {need_to_wait} seconds for API throttle to finish")
            time.sleep(need_to_wait)

        price, request_made = price_checker_client.check_price(hash_name)
        total_val += price
        print(f"[ITEM] {hash_name}: ${price}")
        if request_made:
            check_price_req_count += 1

        elapsed_time = time.time() - start_time
        if elapsed_time >= 60:
            check_price_req_count = 0
            start_time = time.time()

    print(f"[FINISHED] You could have sold all your cases for: ${total_val}")


if __name__ == '__main__':
    main()
