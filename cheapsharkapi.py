import requests


def return_cheapest(deals_params, CHEAPSHARK_API_DEALS, CHEAPSHARK_API_STORES, CHEAPSHARP_REDIRECT):
    game_title_check = ''
    game_sale_check = ''
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
                        "link": CHEAPSHARP_REDIRECT + games['dealID'],
                        "gameID": games['gameID']
                    }
                    cheapest_dict_list.append(cheapest_dict)
    return cheapest_dict_list


def return_game(deals_params, CHEAPSHARK_API_DEALS, CHEAPSHARK_API_STORES, CHEAPSHARP_REDIRECT):
    game_title_check = ''
    game_sale_check = ''
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
        else:
            for store_counts, store in enumerate(store_response_init_json):
                if games['storeID'] == store['storeID']:
                    cheapest_dict = {
                        "title": games['title'],
                        "storeName": store['storeName'],
                        "normalPrice": games['normalPrice'],
                        "salePrice": games['salePrice'],
                        "link": CHEAPSHARP_REDIRECT + games['dealID'],
                        "gameID": games['gameID']
                    }
                    cheapest_dict_list.append(cheapest_dict)
    return cheapest_dict_list


def set_alert(CHEAPSHARK_API_ALERT, alert_params):
    set_alert = requests.get(url=CHEAPSHARK_API_ALERT, params=alert_params)
    if set_alert.status_code == 200:
        all_good = f"Text response: {set_alert.text} Status code: {set_alert.status_code}"
        return all_good
    else:
        no_good = f'Something went wrong. Please try again. {set_alert.text}'
        return no_good


def manage_alerts(CHEAPSHARK_API_ALERT, alert_params):
    manage_alert = requests.get(url=CHEAPSHARK_API_ALERT, params=alert_params)
    if manage_alert.status_code == 200:
        all_good = manage_alert.text
        return all_good
    else:
        no_good = f"{manage_alert.text}"
        return no_good
