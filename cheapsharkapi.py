


def return_cheapest(cheapshark_response_json, store_response_init_json):
    game_title_check = ''
    game_sale_price = ''
    # need to fix the below poop. Trying to check to see if the next title matches the previous title and if so ignore it.
    # it should look at the previous title and previous sale price and if the same then ignore it.
    for games_counts, games in enumerate(cheapshark_response_json):
        #return f"Title #{games_counts}: {games['title']}"
        if games['title'] == game_title_check and games['salePrice'] == game_sale_price:
            game_title_check = cheapshark_response_json[games_counts]['title']
            game_sale_check = cheapshark_response_json[games_counts]['salePrice']
            return f"{games_counts}. {game_title_check}"
        else:
            for store_counts, store in enumerate(store_response_init_json):
                if games['storeID'] == store['storeID']:
                    return f"Title: {games['title']}\nStore Name: {store['storeName']}\nNormal Price: {games['normalPrice']}\nSale Price: {games['salePrice']}\nLink: {CHEAPSHARP_REDIRECT + games['dealID']}\n"
