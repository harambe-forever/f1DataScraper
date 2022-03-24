from numpy import empty
import requests
from bs4 import BeautifulSoup as soup
import time


def get_page(url):
    page = requests.get(url, headers={
        "User-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"})
    doc = soup(page.content, "html.parser")
    return doc


def get_tbody(race_name, y):
    url = "https://www.formula1.com/en/results.html/"+str(y)+"/races/" + \
        race_name+"/race-result.html"
    doc = get_page(url)
    site_wrapper = doc.find(class_="site-wrapper")
    main = site_wrapper.find(class_="template template-resultsarchive")
    inner_class = main.find(class_="inner-wrap ResultArchiveWrapper")
    result_archive = inner_class.find(class_="ResultArchiveContainer")
    results_archive_wrapper = result_archive.find(
        class_="resultsarchive-wrapper")
    content = results_archive_wrapper.table
    tbody = content.tbody
    return tbody


def get_races(doc):
    main = doc.main
    article = main.article
    container = article.find(class_="resultsarchive-filter-container")
    rarchive1 = container.find(
        class_="resultsarchive-filter-wrap")
    rarchive2 = rarchive1.find_next(class_="resultsarchive-filter-wrap")
    rarchive3 = rarchive2.find_next(class_="resultsarchive-filter-wrap")
    lis = rarchive3.find_all("li", class_="resultsarchive-filter-item")
    race_links = []                                 # bunu dict ile yapmaya calis
    for li in lis:
        race_links.append([item["data-value"]
                           for item in li.find_all() if "data-value" in item.attrs])
    return race_links


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


def get_race_input(races, y):
    print("These are the races of", y,
          "select the race you want by typing number of it.")

    for i in range(len(races)):
        print(i, "-", races[i][0].strip("-/1234567890"))
    ipt = input("Enter: ")
    while int(ipt) > len(races):
        ipt = input("Get your shit together and try again: ")
    # print("selected:", races[int(ipt)])
    if int(ipt) == 0:
        return "all"
    else:
        return races[int(ipt)][0]


def get_driver_name(tbody):
    list_of_names = []
    tds = tbody.find_all("td", class_="dark bold")
    for td in tds:
        names = td.find_all(
            True, {"class": ["hide-for-tablet", "hide-for-mobile"]})
        if not names:
            continue
        else:
            name = names[0].string + " " + names[1].string
            list_of_names.append(name)
    return list_of_names


def get_team_name(tbody):
    list_of_teams = []
    tds = tbody.find_all("td", class_="semi-bold uppercase hide-for-tablet")
    for td in tds:
        list_of_teams.append(td.text)
    return list_of_teams


def get_laps(tbody):
    list_of_completed_laps = []
    tds = tbody.find_all("td", class_="bold hide-for-mobile")
    for td in tds:
        list_of_completed_laps.append(td.text)
    return list_of_completed_laps


def get_times(tbody):
    list_of_times = []
    tds = tbody.find_all("td", class_="bold hide-for-mobile")
    for td in tds:
        time = td.find_next(class_="dark bold")
        list_of_times.append(time.text)
    return list_of_times


def get_points(tbody):
    list_of_points = []
    tds = tbody.find_all(lambda tag: tag.name ==
                         "td" and tag["class"] == ["bold"])
    for td in tds:
        list_of_points.append(td.text)
    return list_of_points


def save(path, year, race, names, teams, laps, time, points):
    lines = []
    header = ("Pos" + " Name" + " "*(21) + "Team" + " "*(21) +
              "Laps" + " "*(10) + "Time" + " "*(10) + "Points")
    lines.append(header)
    for i in range(len(names)):
        n = str(names[i])
        te = str(teams[i])
        l = str(laps[i])
        t = str(time[i])
        p = str(points[i])
        appendLine = (str(i+1) + "-" + n + " "*(25 - len(n)) + te + " "*(25 - len(te)) +
                      l + " "*(14 - len(l)) + t + " "*(14 - len(t)) + p)
        lines.append(appendLine)
    with open(path, "a", encoding="utf-8") as f:
        txt = "-"*20 + str(year) + " " + str(race) + \
            " Race Info" + "-"*60 + "\n"
        f.write(txt)
        for line in lines:
            f.write(line)
            f.write("\n")
    f.close()


def main():
    year = get_input()
    len_year = len(year)
    open("race_info.txt", "w").close()
    for y in year:
        print("Scraping year", y)
        url = "https://www.formula1.com/en/results.html/"+str(y)+"/races.html"
        doc = get_page(url)
        race_links = get_races(doc)
        race_name = get_race_input(race_links, y)
        if race_name == "all":
            for index in range(1, len(race_links)):
                print(race_links[index][0])
                race_name = race_links[index][0]
                tbody = get_tbody(race_name, y)
                name = get_driver_name(tbody)
                team = get_team_name(tbody)
                completed_laps = get_laps(tbody)
                times = get_times(tbody)
                points = get_points(tbody)
                save("race_info.txt", y, race_name, name,
                     team, completed_laps, times, points)
                time.sleep(1)
        else:
            print(race_name)
            tbody = get_tbody(race_name, y)
            name = get_driver_name(tbody)
            team = get_team_name(tbody)
            completed_laps = get_laps(tbody)
            times = get_times(tbody)
            points = get_points(tbody)
            save("race_info.txt", y, race_name, name,
                 team, completed_laps, times, points)
        print("Done")


main()
