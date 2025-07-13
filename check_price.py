import requests
import json

# === Конфигурация ===
BOT_TOKEN = "7689422674:AAGU1101BBWCE5wpDQtatTLAWNBv7yOEsxY"
CHAT_ID = "653797157"
THRESHOLD = 0.10  # 10% вверх или вниз

# === Список ресурсов ===
RESOURCES = ["Wood", "Egg", "Stone", "Milk", "Pumpkin", "Carrot", "Corn"]

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
            change = (current_price - last_price) / last_price
            if abs(change) >= THRESHOLD:
                direction = "📈 выросла" if change > 0 else "📉 упала"
                percent = abs(change) * 100
                msg = f"{direction} цена на {resource} на {percent:.2f}%\n{last_price:.3f} → {current_price:.3f}"
                send_telegram_message(msg)

    save_prices(current_prices)

# === Запуск ===
send_telegram_message("⏰ Скрипт запущен. Проверка цен ресурсов...")
check_prices()