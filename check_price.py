import requests
import json
import time
from bs4 import BeautifulSoup

# === Конфигурация ===
BOT_TOKEN = "7689422674:AAGU1101BBWCE5wpDQtatTLAWNBv7yOEsxY"
CHAT_ID = "653797157"
CHECK_INTERVAL = 7200  # 2 часа
THRESHOLD = 0.10  # 10% вверх или вниз

# === Все 48 ресурсов ===
RESOURCES = [
    "Wood", "Stone", "Iron", "Gold", "Crimstone", "Obsidian", "Egg", "Honey", "Leather", "Wool", "Merino Wool",
    "Feather", "Milk", "Pumpkin", "Carrot", "Corn", "Beetroot", "Cauliflower", "Radish", "Parsnip",
    "Cabbage", "Potato", "Onion", "Garlic", "Chili", "Apple", "Orange", "Banana", "Blueberry", "Lemon",
    "Grape", "Tomato", "Sunflower", "Rice", "Celestine", "Lunara", "Duskberry", "Yam", "Kale", "Broccoli",
    "Strawberry", "Raspberry", "Peach", "Avocado", "Coconut", "Cocoa", "Tea Leaf", "Coffee Bean"
]

# === Telegram уведомление ===
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    try:
        response = requests.post(url, json=data)
        print("Telegram response:", response.text)
    except Exception as e:
        print("Ошибка отправки в Telegram:", e)

# === Получить цену ресурса с сайта (без API) ===
def get_price(resource):
    try:
        url = f"https://sfl.world/trade/{resource.replace(' ', '%20')}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        price_elem = soup.select_one(".text-xxs.text-white.text-right")
        if not price_elem:
            return None
        return float(price_elem.text.strip().replace('$', ''))
    except Exception as e:
        print(f"Ошибка получения цены для {resource}: {e}")
        return None

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

# === Основная логика ===
def check_prices():
    last_prices = load_prices()
    current_prices = {}

    for resource in RESOURCES:
        current_price = get_price(resource)
        if current_price is None:
            continue

        current_prices[resource] = current_price
        last_price = last_prices.get(resource)

        if last_price is not None:
            change = (current_price - last_price) / last_price
            if abs(change) >= THRESHOLD:
                direction = "📈 выросла" if change > 0 else "📉 упала"
                percent = abs(change) * 100
                msg = f"{direction} цена на {resource} на {percent:.2f}%\n{last_price:.3f} → {current_price:.3f}"
                send_telegram_message(msg)
        else:
            # При первом запуске просто отправим текущую цену
            send_telegram_message(f"💰 {resource}: {current_price:.3f}")

    save_prices(current_prices)

# === Стартовое уведомление ===
send_telegram_message("🔁 Бот отслеживает 48 ресурсов. Изменения ±10% будут присылаться каждые 2 часа!")

# === Цикл ===
while True:
    check_prices()
    time.sleep(CHECK_INTERVAL)
