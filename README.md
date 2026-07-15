#PRICE TRACKER

A Python script that tracks product prices from books.toscrape.com, saves price history over time, and sends an email alert when a price drops. 

## Features
- Tracks multiple products at once
- Saves price history to a local JSON file
- Compares each check against the last recorded price
- Sends an email alert when a price drops

## How it works
1. Fetches each product page and parses the price using BeautifulSoup
2. Compares the new price to the last saved price for that product
3. Logs the result (first check / dropped / increased / no change)
4. Sends an email if the price dropped
5. Saves the updated history to 'price_history.json'

## Setup
1. Install dependencies:
2. Create a '.env' file with:
3. Run it:

## What I learned
- Making HTTP requests and parsing HTML with BeautifulSoup
- Handling character encoding issues
- Reading/writing JSON for persistent storage
- Sending email via smtplib
- Managing secrets with environment variables
