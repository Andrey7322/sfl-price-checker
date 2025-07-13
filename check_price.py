import requests
import json
import time
from bs4 import BeautifulSoup

BOT_TOKEN = "7689422674:AAGU1101BBWCE5wpDQtatTLAWNBv7yOEsxY"
CHAT_ID = "653797157"
CHECK_INTERVAL = 7200  # 2 часа
THRESHOLD = 0.10  # 10%

RESOURCES = [
    "Wood", "Stone", "Iron", "Gold", "Crimstone", "Obsidian",
    "Egg", "Honey", "Leather", "Wool", "Merino Wool", "Feather", "Milk",
    "Pumpkin", "Carrot", "Beetroot", "Cauliflower", "Parsnip", "Radish", "Cabbage",
    "Potato", "Onion", "Garlic", "Corn", "Sunflower", "Wheat", "Rice",
    "Apple", "Orange", "Banana", "Blueberry", "Lemon", "Grape", "Tomato",
    "Celestine", "Lunara", "Duskberry",
    "Pumpkin Soup", "Roast Veggies", "Kale Stew", "Club Sandwich",
    "Sauerkraut", "Fermented Carrots", "Roasted Garlic", "Tropical Smoothie",
    "Boiled Eggs", "Kebab"
]

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, json=data)
    except Exception as e:
        print("Ошибка отправки Telegram:", e)

def get_price(resource):
    try:
        url = "https://sfl.world/market"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        cells = soup.find_all("div", class_="market-cell")
        for cell in cells:
            name_tag = cell.find("div", class_="market-item")
            price_tag = cell.find("div", class_="market-price")
            if name_tag and_
