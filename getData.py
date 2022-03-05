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
    site_wrapper = doc.find(class_="site-wrapper")
    main = site_wrapper.find(class_="template template-resultsarchive")
    inner_class = main.find(class_="inner-wrap ResultArchiveWrapper")
    result_archive = inner_class.find(class_="ResultArchiveContainer")
    results_archive_wrapper = result_archive.find(
        class_="resultsarchive-wrapper")
    content = results_archive_wrapper.table
    tbody = content.tbody
    tr = tbody.find_all("tr")
    for every_a in tr:
        a = every_a.find_all("a")
        for every_name in a:
            name = every_name.span.string
            print(name)
    """a = tr.find_all("a")
    name = a.span
    print(name)"""


main()
