import requests
from bs4 import BeautifulSoup as soup
import matplotlib.pyplot as plt


def main():
    doc = get_page(
        "https://www.formula1.com/en/results.html/1950/drivers.html")
    data = get_data(doc)


def get_page(url):
    page = requests.get(url, headers={
        "User-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"})
    doc = soup(page.content, "html.parser")
    return doc


def get_data(doc):
    nations = {}
    drivers = {}
    teams = {}
    season_drivers = []
    drivers_points_this_season = []
    site_wrapper = doc.find(class_="site-wrapper")
    main = site_wrapper.find(class_="template template-resultsarchive")
    inner_class = main.find(class_="inner-wrap ResultArchiveWrapper")
    result_archive = inner_class.find(class_="ResultArchiveContainer")
    results_archive_wrapper = result_archive.find(
        class_="resultsarchive-wrapper")
    content = results_archive_wrapper.table
    tbody = content.tbody
    """trs = tbody.find_all("tr")
    # print(trs)
    for tr in trs:
        tds = tr.find_all("td")
        for td in tds:
            driver_name = td.a
            print(driver_name)"""
    tds_for_names = tbody.find_all("td", class_="dark bold ArchiveLink")
    print(tds_for_names)
    tds_for_points = tbody.find_all("td", class_="dark bold")
    for td_for_points in tds_for_points:
        point = td_for_points.string
        drivers_points_this_season.append(point)
        # print(point)

    """point = td.find(class_="dark bold")
        print(point)"""
    """if td.a == None:
            continue
        else:
            a = td.a
            print(a, "\n")"""


main()
