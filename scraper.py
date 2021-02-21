import requests
from bs4 import BeautifulSoup
def scrape(url):
    s = requests.Session()
    content =requests.get(url)

    print(content)
    page = BeautifulSoup(content.text,"html5lib")
    results = []
    for entry in page.find_all("h3", attrs={"class": "gs_rt"}):
        results.append({"title": entry.a.text})

    return results


query = 'machine learning paper'
url = 'https://scholar.google.com/scholar?q=' + query 
scrape(url)