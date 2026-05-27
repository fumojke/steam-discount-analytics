import requests

def fetch_game_details(app_id):
    """
    Fetches the live regional price (UAH) directly from Steam API.
    Returns the price as an integer or None if not found.
    """
    # cc=ua форсирует выдачу цен в украинских гривнах
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&cc=ua"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        app_data = data.get(str(app_id)) # Steam API возвращает словарь, где ключ - это ID игры в виде строки

        # Проверяем, что игра найдена
        if app_data and app_data.get("success"):
            # Создаем словарь с названием (оно есть всегда)
            game_info = {
                "title": app_data["data"]["name"],
                "price": 0  # Цена по умолчанию, если игра бесплатная
            }

            # Если игра платная, обновляем цену
            if "price_overview" in app_data["data"]:
                price_info = app_data["data"]["price_overview"]
                game_info["price"] = int(price_info["final"] / 100)

            return game_info

    return None

def fetch_wishlist(steam_id):
    """
    Fetches the wishlist from a public Steam profile
    using a custom URL name.
    """
    print(f"Fetching wishlist for SteamID: {steam_id}...")

    url = f"https://api.steampowered.com/IWishlistService/GetWishlist/v1/?steamid={steam_id}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # В официальном API нужные нам данные лежат чуть глубже
        if "response" in data and "items" in data["response"]:
            return data["response"]["items"]

    print(f"[!] Failed to fetch wishlist. Status code: {response.status_code}")

    return None

if __name__ == "__main__":
    # Вставь свой SteamID64 в кавычки вместо текста!
    my_wishlist = fetch_wishlist("76561198132789707")

    print(my_wishlist)

