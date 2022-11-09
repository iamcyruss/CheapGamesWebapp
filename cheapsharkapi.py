


def return_cheapest(cheapshark_response_json, store_response_init_json):
    game_title_check = ''
    game_sale_price = ''
    CHEAPSHARP_REDIRECT = "https://www.cheapshark.com/redirect?dealID="
    # need to fix the below poop. Trying to check to see if the next title matches the previous title and if so ignore it.
    # it should look at the previous title and previous sale price and if the same then ignore it.
    for games_counts, games in enumerate(cheapshark_response_json):
        print(f"Title #{games_counts}: {games['title']}")
        if games['title'] == game_title_check and games['salePrice'] == game_sale_price:
            game_title_check = cheapshark_response_json[games_counts]['title']
            game_sale_check = cheapshark_response_json[games_counts]['salePrice']
            print(f"{games_counts}. {game_title_check}")
        else:
            for store_counts, store in enumerate(store_response_init_json):
                if games['storeID'] == store['storeID']:
                    print(f"Title: {games['title']}\nStore Name: {store['storeName']}\nNormal Price: {games['normalPrice']}\nSale Price: {games['salePrice']}\nLink: {CHEAPSHARP_REDIRECT + games['dealID']}\n")
