from bs4 import BeautifulSoup
import requests
import json
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

FILE_NAME = "price_history.json"
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

PRODUCTS = [
    {
        "name": "A Light in the Attic",
        "url": "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    },
    {
        "name" : "Soumission", 
        "url": "http://books.toscrape.com/catalogue/soumission_998/index.html"
    },
    {
        "name": "Sharp Objects",
        "url": "http://books.toscrape.com/catalogue/sharp-objects_997/index.html"
    }
]

def get_price(url):
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

def get_last_price(history, name):
    matches = [entry for entry in history if entry["title"] == name]
    if matches:
        return matches[-1]["price"]
    return None

def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

if __name__ == "__main__":
    history = load_history()

    for product in PRODUCTS:
        title, price = get_price(product["url"])
        last_price = get_last_price(history, title)
        if last_price is None:
            print(f"First check: {title} is ${price}")
        elif price < last_price:
            print(f"Price dropped! {title}: ${last_price} --> ${price}")
            send_email(
                subject=f"Price drop: {title}",
                body=f"{title} dropped from ${last_price} to ${price}!"
            )
        elif price > last_price:
            print(f"Price increased! {title}: ${last_price} --> ${price}")
        else:
            print(f"No change: {title} is still ${price}")

        entry = {
            "title": title,
            "price": price,
            "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        history.append(entry)

    save_history(history)

    print(f"\nChecked {len(PRODUCTS)} products - {len(history)} total records saved.")