import requests
from bs4 import BeautifulSoup as soup
import time


def get_page(url):
    page = requests.get(url, headers={
        "User-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"})
    doc = soup(page.content, "html.parser")
    return doc


def get_races(doc):
    main = doc.main
    article = main.article
    container = article.find(class_="resultsarchive-filter-container")
    rarchive1 = container.find(
        class_="resultsarchive-filter-wrap")
    rarchive2 = rarchive1.find_next(class_="resultsarchive-filter-wrap")
    rarchive3 = rarchive2.find_next(class_="resultsarchive-filter-wrap")
    lis = rarchive3.find_all("li", class_="resultsarchive-filter-item")
    races = []
    for li in lis:
        races.append(li.a.span.string)
    return races


def get_input():
    year = []
    ipt = input("What year do you want?\nIf multiple, seperate with comma.\n")
    ipt = ipt.split(",")
    if len(ipt) > 1:
        while int(ipt[0]) < 1950 or int(ipt[1]) > 2022:
            ipt = input(
                "No such year. Dates should be given between 1950 and 2022.\n")
            ipt = ipt.split(",")
        for y in range(int(ipt[0]), int(ipt[1])+1):
            year.append(y)
    else:
        while int(ipt[0]) < 1950 or int(ipt[0]) > 2022:
            ipt = input(
                "No such year. Dates should be given between 1950 and 2022.\n")
            ipt = ipt.split(",")
        year.append(int(ipt[0]))
    return year


def scrape_single_race_detailed(race):
    print()


def get_race_input(races, y):
    print("These are the races of", y,
          "select the race you want by typing the whole thing or just the number of it.")
    for i in range(len(races)):
        print(i, "-", races[i])
    ipt = input("Enter: ")
    if(ipt.isdigit()):
        #print("hell yeah")
        while int(ipt) > len(races):
            ipt = input("Get your shit together and try again: ")
        return races[int(ipt)]
    else:
        #print("hell yo")
        while ipt not in races:
            ipt = input("Get your shit together and try again: ")
        return ipt
    #print("selected:", ipt)


def main():
    year = get_input()
    len_year = len(year)
    for y in year:
        print("Scraping year", y)
        url = "https://www.formula1.com/en/results.html/"+str(y)+"/races.html"
        doc = get_page(url)
        races = get_races(doc)
        ipt = get_race_input(races, y)
        print(ipt)
    """url = "https://www.formula1.com/en/results.html/2021/races.html"
    doc = get_page(url)
    get_data(doc)"""


main()
