import re
import requests
from bs4 import BeautifulSoup

url = "https://www.fmkorea.com/index.php?mid=stock&category=2997204381"

# 주식게시판은 끝까지 있어서 다 스크랩하기엔 무리,24시간내에 올라온 것만 체크?


def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pg_form = soup.find("form", {"class": "bd_pg clear"})
    pg = pg_form.find("fieldset").find_all("a")
    last_page = pg[-3].get_text(strip=True)
    return int(last_page)


def extract_stock(html):
    try:
        title = html.find("td", {"class": "title"}).find(
            "a", {"class": "hx"}).get_text(strip=True)
    except:
        return
    return {"title": title}


def extract_stocks(last_page):
    stocks = []
    for page in range(last_page):
        print(f"Scrapping page :{page}")
        result = requests.get(f"{url}&page={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        table = soup.find("table", {"class": "bd_lst bd_tb_lst bd_tb"})
        results = table.find_all("tr", {"class": ""})
        for result in results:
            stock = extract_stock(result)
            if stock:
                stocks.append(stock)
    return stocks


def get_stocks():
    last_page = get_last_page(url)
    stocks = extract_stocks(last_page)
    return stocks


print(get_stocks())
