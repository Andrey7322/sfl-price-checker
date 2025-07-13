import requests
from bs4 import BeautifulSoup
import json
import time

# === Telegram config ===
BOT_TOKEN = "7689422674:AAGU1101BBWCE5wpDQtatTLAWNBv7yOEsxY"
CHAT_ID = "653797157"
CHECK_INTERVAL = 2 * 60 * 60  # 2 часа

# === Список ресурсов ===
RESOURCES = [
    "Wood", "Stone", "Iron", "Gold", "Crimstone", "Obsidian",
    "Egg", "Honey", "Leather", "Wool", "Merino Wool", "Feather", "Milk",
    "Grape", "Tomato", "Lemon", "Blueberry", "Orange", "Apple", "Banana",
    "Celestine", "Lunara", "Duskberry", "Rice", "Corn", "Carrot", "Pumpkin",
    "Cabbage", "Cauliflower", "Beetroot", "Parsnip", "Radish", "Garlic",
    "Sunflower", "Potato", "Onion", "Wheat", "Kale", "Soybean", "Peanut",
    "Lavender", "Coffee", "Peach", "Pear", "Coconut", "Papaya", "Pineapple"
]

# === Telegram message sender ===
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    try:
        response = requests.post(url, json=data)
        if not response.ok:
            print("Ошибка Telegram:", response.text)
    except Exception as e:
        print("Ошибка подключения к Telegram:", e)

# === Get all prices by parsing ===
def fetch_all_prices():
    url = "https://sfl.world/trade"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        prices = {}
        rows = soup.find_all("div", class_="css-1u7zfla")  # класс может измениться

        for row in rows:
            name_div = row.find("div", class_="css-1xhj18k")
            price_div = row.find("div", class_="css-17r6zjv")

            if name_div and price_div:
                name = name_div.text.strip()
                price = price_div.text.strip().replace("$", "")
                try:
                    prices[name] = float(price)
                except:
                    continue

        return prices
    except Exception as e:
        print("Ошибка при получении данных:", e)
        return {}

# === Работа с price.json ===
def load_prices():
    try:
        with open("price.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_prices(prices):
    with open("price.json", "w") as f:
        json.dump(prices, f)

# === Основ
