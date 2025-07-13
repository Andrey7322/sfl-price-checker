
import requests
import json
import time

# === Конфигурация ===
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
CHECK_INTERVAL = 7200  # Каждые 2 часа

# === Все 48 ресурсов ===
RESOURCES = [
    "Wood", "Stone", "Iron", "Gold", "Crimstone", "Obsidian",
    "Egg", "Honey", "Leather", "Wool", "Merino Wool", "Feather", "Milk",
    "Grape", "Tomato", "Lemon", "Blueberry", "Orange", "Apple", "Banana",
    "Celestine", "Lunara", "Duskberry",
    "Rice", "Olive", "Sunflower", "Potato", "Rhubarb", "Pumpkin", "Zucchini", "Carrot",
    "Yam", "Cabbage", "Broccoli", "Soybean", "Beetroot", "Pepper", "Cauliflower",
    "Parsnip", "Eggplant", "Corn", "Onion", "Radish", "Wheat", "Turnip", "Kale",
    "Artichoke", "Barley"
]

# === Telegram уведомление ===
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, headers=headers, json=data)
        if not response.ok:
            print("Ошибка Telegram:", response.text)
    except Exception as e:
        print("Ошибка подключения к Telegram:", e)

# === Получить цену ресурса ===
def get_price(resource):
    url = f"https://api.sfl.tools/api/trade/{resource}"
    try:
        response = requests.get(url)
        data = response.json()
        latest_trade = data[-1]
        return float(latest_trade["price"])
    except Exception as e:
        print(f"Ошибка получения цены для {resource}:", e)
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
            change = (current_price - last_price) / last_price * 100
            direction = "📈" if change > 0 else "📉"
            msg = f"{direction} {resource}: {last_price:.3f} → {current_price:.3f} ({change:+.2f}%)"
        else:
            msg = f"📊 {resource}: {current_price:.3f} (нет предыдущих данных)"

        send_telegram_message(msg)

    save_prices(current_prices)

# === Цикл ===
if __name__ == "__main__":
    send_telegram_message("🚀 Бот запущен. Проверка цен каждые 2 часа.")
    while True:
        check_prices()
        time.sleep(CHECK_INTERVAL)
