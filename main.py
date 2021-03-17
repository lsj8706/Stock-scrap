import re
import requests
from bs4 import BeautifulSoup

url = "https://www.fmkorea.com/index.php?mid=stock&category=2997204381"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
# 주식게시판은 끝까지 있어서 다 스크랩하기엔 무리,24시간내에 올라온 것만 체크?


def get_last_page(url):
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.text, "html.parser")
    pg_form = soup.find("form", {"class": "bd_pg clear"})
    pg = pg_form.find("fieldset").find_all("a")
    last_page = pg[-3].get_text(strip=True)
    return int(last_page)


def extract_stock(html):
    try:
        title = html.find("td", {"class": "title"}).find(
            "a", {"class": "hx"}).get_text(strip=True)
        time = html.find("td", {"class": "time"}).get_text(strip=True)
        clicked = html.find("td", {"class": "m_no"}).get_text(strip=True)
        try:
            voted = html.find(
                "td", {"class": "m_no_voted"}).get_text(stip=True)
        except:
            voted = 0
    except:
        return
    return {"title": title, "time": time, "clicked": clicked, "voted": voted}


def extract_stocks(last_page):
    stocks = []
    for page in range(last_page):
        print(f"Scrapping page :{page}")
        result = requests.get(f"{url}&page={page+1}", headers=headers)
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
