from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
FILE_NAME = "price_history.json"

def get_price():
    response = requests.get(url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("h1").text
    price_text = soup.find("p", class_="price_color").text
    price = float(price_text.replace("£", ""))

    return title, price

def load_history():
    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_history(history):
    with open(FILE_NAME, "w") as f:
        json.dump(history, f, indent=2)

if __name__ == "__main__":
    title, price = get_price()
    history = load_history()

    if history:
        last_price = history[-1]["price"]
        if price < last_price:
            print(f"Price dropped! {title}: ${last_price} --> ${price}")
        elif price > last_price:
            print(f"Price increased! {title}: $${last_price} --> ${price}")
        else:
            print(f"No change: {title} is still ${price}")
    else:
        print(f"First check: {title} is ${price}")
        
    entry = {
        "title": title,
        "price": price,
        "checked at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    history.append(entry)

    save_history(history)

    print(f"{title}: {price} - saved ({len(history)} checks so far)")