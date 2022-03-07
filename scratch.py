from dataclasses import dataclass
import string
import requests
from bs4 import BeautifulSoup as soup
import linkedlist
import time
import matplotlib.pyplot as plt


def get_page(url):
    page = requests.get(url, headers={
        "User-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"})
    doc = soup(page.content, "html.parser")
    return doc


def get_data(doc):
    site_wrapper = doc.find(class_="site-wrapper")
    main = site_wrapper.find(class_="template template-resultsarchive")
    inner_class = main.find(class_="inner-wrap ResultArchiveWrapper")
    result_archive = inner_class.find(class_="ResultArchiveContainer")
    results_archive_wrapper = result_archive.find(
        class_="resultsarchive-wrapper")
    content = results_archive_wrapper.table
    tbody = content.tbody
    return tbody


def get_driver_name(tbody):
    drivers_this_season = []
    tds_for_names = tbody.find_all("a", class_="dark bold ArchiveLink")
    for td_for_names in tds_for_names:
        names = td_for_names.find_all(
            True, {"class": ["hide-for-tablet", "hide-for-mobile"]})
        name = names[0].text + " " + names[1].text
        drivers_this_season.append(name)
        #print("Name:", name)
    return drivers_this_season


def get_driver_point(tbody):
    points_this_season = []
    tds_for_points = tbody.find_all("td", class_="dark bold")
    for td_for_points in tds_for_points:
        point = td_for_points.string
        points_this_season.append(point)
        #print("PTS:", point)
    return points_this_season


def get_team_name(tbody):
    teams_this_season = []
    tds_for_teams = tbody.find_all(
        "a", class_="grey semi-bold uppercase ArchiveLink")
    for td_for_teams in tds_for_teams:
        team = td_for_teams.string
        #print("Team:", team)
        teams_this_season.append(team)
    return teams_this_season


def main():
    url = "https://www.formula1.com/en/results.html/1950/drivers.html"
    doc = get_page(url)
    data = get_data(doc)
    names = get_driver_name(data)
    points = get_driver_point(data)
    teams = get_team_name(data)
    print(len(names), " ", len(points), " ", len(teams))
    for i in range(len(names)):
        print(names[i], " ", points[i], " ", teams[i])


main()
