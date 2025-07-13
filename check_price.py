import requests
import json
import time
from bs4 import BeautifulSoup

BOT_TOKEN = "7689422674:AAGU1101BBWCE5wpDQtatTLAWNBv7yOEsxY"
CHAT_ID = "653797157"
CHECK_INTERVAL = 2 * 60 * 60  # 2 часа
THRESHOLD = 0.10  # 10%

RESOURCES = [
    "Wood", "Stone", "Iron", "Gold", "Crimstone", "Obsidian", "Egg", "Honey", "Leather", "Wool",
    "Merino Wool", "Feather", "Milk", "Grape", "Tomato", "Lemon", "Blueberry", "Orange", "Apple", "Banana",
    "Celestine", "Lunara", "Duskberry", "Rice", "Pumpkin", "Carrot", "Corn", "Cabbage", "Beetroot",
    "Cauliflower", "Radish", "Parsnip", "Potato", "Onion", "Garlic", "Sunflower", "Wheat", "Kale", "Broccoli",
    "Eggplant", "Bell Pepper", "Chili", "Mushroom", "Strawberry", "Pineapple", "Coconut", "Avocado"
]

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    try:
        response = requests.post(url, json=data)
        if not response.ok:
            print("Ошибка Telegram:", response.text)
    except Exception as e:
        print("Ошибка подключения к Telegram:", e)

def get_price(resource):
    try:
        url = "https://sfl.world/market"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        cells = soup.find_all("div", class_="market-item-cell")
        for cell in cells:
            name_tag = cell.find("div", class_="market-item")
            price_tag = cell.find("div", class_="market-price")
            if name_tag and price_tag:
                name = name_tag.get_text(strip=True)
                price = price_tag.get_text(strip=True).replace("$", "")
                if name == resource:
                    return float(price)
    except Exception as e:
        print(f"Ошибка получения цены для {resource}:", e)
    return None

def load_prices():
    try:
        with open("price.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_prices(prices):
    with open("price.json", "w") as f:
        json.dump(prices, f)

def check_prices():
    last_prices = load_prices()
    current_prices = {}
    messages = []
    for resource in RESOURCES:
        current_price = get_price(resource)
        if current_price is None:
            continue
        current_prices[resource] = current_price
        last_price = last_prices.get(resource)
        if last_price:
            change = (current_price - last_price) / last_price
            if abs(change) >= THRESHOLD:
                direction = "📈 выросла" if change > 0 else "📉 упала"
                percent = abs(change) * 100
                messages.append(f"{resource}: {direction} на {percent:.2f}%\n{last_price:.3f} → {current_price:.3f}")
    save_prices(current_prices)

    if messages:
        header = "📊 Изменения цен (±10%):"
        send_telegram_message(header + "\n\n" + "\n\n".join(messages))

# стартовое уведомление
send_telegram_message("🔁 Бот отслеживает 48 ресурсов. Изменения ±10% будут присылаться каждые 2 часа!")

# бесконечный цикл
while True:
    check_prices()
    time.sleep(CHECK_INTERVAL)
