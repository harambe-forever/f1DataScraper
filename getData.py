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


nations = {}
drivers = {}
teams = {}


def get_data(doc):
    global nations
    global drivers
    global teams

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
    tds_for_names = tbody.find_all("a", class_="dark bold ArchiveLink")
    for td_for_names in tds_for_names:
        names = td_for_names.find_all(
            True, {"class": ["hide-for-tablet", "hide-for-mobile"]})
        name = names[0].text + " " + names[1].text
        season_drivers.append(name)
        # print("Name:", name)
    tds_for_points = tbody.find_all("td", class_="dark bold")
    for td_for_points in tds_for_points:
        point = td_for_points.string
        drivers_points_this_season.append(point)
        # print(point)
    for i in range(len(season_drivers)):
        key = season_drivers[i]
        drivers[key] = drivers_points_this_season[i]
    print(drivers)


main()
