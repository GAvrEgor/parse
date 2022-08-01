import requests
from bs4 import BeautifulSoup
import xlsxwriter

headers = {"Accept": "",
           "User-Agent": "",}


def get_url():

    for page in range(1, 5):
        url = f"https://scrapingclub.com/exercise/list_basic/?page={page}"
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        card_in_page = soup.find_all("div", class_="col-lg-4 col-md-6 mb-4")
        for card in card_in_page:
            link = "https://scrapingclub.com" + card.find("a").get("href")
            yield link


def get_data():
    for link in get_url():
        response = requests.get(url=link, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        full_card = soup.find("div", class_="card mt-4 my-4")
        title = full_card.find("h3", class_="card-title").text
        price = full_card.find("h4").text
        description = full_card.find("p").text
        yield title, price, description


def main(param):
    book = xlsxwriter.Workbook(r"C:\Users\Egor4\OneDrive\Рабочий стол\Книга.xlsx")
    sheet = book.add_worksheet("товар")

    sheet.set_column("A:A", 20)
    sheet.set_column("B:B", 20)
    sheet.set_column("C:C", 20)

    row = 0
    column = 0

    for value in param():
        sheet.write(row, column, value[0])
        sheet.write(row, column+1, value[1])
        sheet.write(row, column+2, value[2])
        row += 1
    book.close()


if __name__ == "__main__":
    main(get_data)
