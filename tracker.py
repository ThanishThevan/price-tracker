from bs4 import BeautifulSoup
import requests

url = "https://books.toscrape.com/"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

books = soup.find_all("article", class_ ="product_pod")

for books in books:
    title = book.h3.a["title"]
    price = book.find("p", class_ ="price_color").text
    print(f"{title} - {price}")