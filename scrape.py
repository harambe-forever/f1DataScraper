import requests
from bs4 import BeautifulSoup as soup
import time
#import matplotlib.pyplot as plt
import pandas as pd


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
        teams_this_season.append(team)
        #print("Team:", team)
    return teams_this_season


def save(path, names, points, teams):
    lines = []
    for i in range(len(names)):
        appendLine = names[i] + "," + points[i] + "," + teams[i]
        lines.append(appendLine)
    with open(path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line)
            f.write("\n")


name_point_dict = {}


def update_dicts(names_list, points_list):
    global name_point_dict
    for i in range(len(names_list)):
        key = names_list[i]
        if key in name_point_dict:
            name_point_dict[key] += float(points_list[i])
        else:
            name_point_dict[key] = float(points_list[i])


def main():
    global name_point_dict
    multiple = int(input("Enable multiple years? Default 0\n(1/0):"))
    if multiple:
        fromm = int(input("From: "))
        to = int(input("To (to is included): "))
        names = []
        points = []
        teams = []
        for i in range(fromm, to+1):
            print("Scraping year", i)
            year = str(i)
            url = "https://www.formula1.com/en/results.html/"+year+"/drivers.html"
            get_multiple_years_then_print(url)
            time.sleep(1)
        sorted_drivers = sorted(name_point_dict.items(),
                                key=lambda x: x[1], reverse=True)
        for i in range(len(sorted_drivers)):
            names.append(sorted_drivers[i][0])
            points.append(str(sorted_drivers[i][1]))
            teams.append("")
        save("data.txt", names, points, teams)
    else:
        year = str(input("Enter desired year: "))
        url = "https://www.formula1.com/en/results.html/"+year+"/drivers.html"
        get_single_year_then_print(url)
    print("donanza")


def get_multiple_years_then_print(url):
    doc = get_page(url)
    data = get_data(doc)
    names = get_driver_name(data)
    points = get_driver_point(data)
    #teams = get_team_name(data)
    update_dicts(names, points)


def get_single_year_then_print(url):
    doc = get_page(url)
    data = get_data(doc)
    names = get_driver_name(data)
    points = get_driver_point(data)
    teams = get_team_name(data)
    save("year_data.txt", names, points, teams)
    new_dataframe = pd.DataFrame({
        "Name": names,
        "Point": points,
        "Team": teams
    })
    new_dataframe.index += 1
    print(new_dataframe)


yes = 1
while yes == 1:
    main()
    yes = int(input("Re-run? (1/0):"))
