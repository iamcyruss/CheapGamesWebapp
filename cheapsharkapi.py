import requests


def return_cheapest(deals_params):
    game_title_check = ''
    game_sale_check = ''
    CHEAPSHARK_API_DEALS = "https://www.cheapshark.com/api/1.0/deals"
    CHEAPSHARK_API_STORES = "https://www.cheapshark.com/api/1.0/stores"
    CHEAPSHARP_REDIRECT = "https://www.cheapshark.com/redirect?dealID="
    store_response_init = requests.get(url=CHEAPSHARK_API_STORES)
    store_response_init.raise_for_status()
    store_response_init_json = store_response_init.json()
    cheapshark_response = requests.get(url=CHEAPSHARK_API_DEALS, params=deals_params)
    cheapshark_response.raise_for_status()
    cheapshark_response_json = cheapshark_response.json()
    # need to fix the below poop. Trying to check to see if the next title matches the previous title and if so ignore it.
    # it should look at the previous title and previous sale price and if the same then ignore it.
    cheapest_dict_list = []
    for games_counts, games in enumerate(cheapshark_response_json):
        #print(f"Title #{games_counts}: {games['title']}")
        if games['title'] == game_title_check and games['salePrice'] == game_sale_check:
            game_title_check = cheapshark_response_json[games_counts]['title']
            game_sale_check = cheapshark_response_json[games_counts]['salePrice']
            #print(f"Title #{games_counts}: {game_title_check}")
        elif games['normalPrice'] == games['salePrice']:
            pass
        else:
            for store_counts, store in enumerate(store_response_init_json):
                if games['storeID'] == store['storeID']:
                    cheapest_dict = {
                        "title": games['title'],
                        "storeName": store['storeName'],
                        "normalPrice": games['normalPrice'],
                        "salePrice": games['salePrice'],
                        "link": CHEAPSHARP_REDIRECT + games['dealID']
                    }
                    cheapest_dict_list.append(cheapest_dict)
    return cheapest_dict_list
