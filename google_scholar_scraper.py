import requests
from lxml import etree
import time
from samir.helpers import get_csv_file_writer
import random
from modules.Proxier import Proxier
from modules.User_Agent_Rotator import User_Agent_Rotator


class Google_Scholar_Scraper:
    def __init__(self):
        self.proxier = Proxier()
        self.proxier.load_proxies()
        self.session = requests.Session()
        self.params = {
            'start': 0,
            'q': '',
            'hl': 'en',
            'as_sdt': '0,5'
        }
        self.headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'
        }
        self.user_agent_rotator = User_Agent_Rotator()
        self.page_dom = etree.HTML
        self.change_proxy()

    def scrap(self, query: str) -> list:
        self.params['q'] = query
        csv_writer, output_file = get_csv_file_writer('output.csv', ['title'], previlage='w')
        results = []
        trials = 0
        while trials < 10:
            self.load_page()
            articles = self.get_articles()
            if len(articles) == 0:
                print('Error while loading.')
                # time.sleep(random.uniform(20, 30))
                self.session = requests.session()
                self.change_proxy()
                self.headers['user-agent'] = self.user_agent_rotator.get_user_agent()
                trials += 1
                continue
            trials = 0
            for article in articles:
                results.append({
                    "title": article.xpath('string()')
                })
                csv_writer.writerow({
                    "title": article.xpath('string()')
                })
                output_file.flush()
            print('offset:', self.params['start'], end='\r')
            time.sleep(random.uniform(3, 7))
            self.params['start'] += 10
        return results

    def load_page(self):
        url = 'https://scholar.google.com/scholar'
        html_content = ''
        trials = 0
        while True:
            try:
                html_content = self.session.get(url, params=self.params, headers=self.headers, timeout=10).text
                break
            except:
                trials += 1
                if trials % 5 == 0:
                    self.change_proxy()
                print('timedout.')
        with open('output.html', 'w') as file:
            file.write(html_content)
        self.page_dom = etree.HTML(html_content)
    
    def get_articles(self) -> list:
        return self.page_dom.xpath('//h3[@class="gs_rt"]')

    def change_proxy(self):
        self.proxy = self.proxier.get_https_proxy()
        self.proxy = self.proxy['ip'] + ':' + self.proxy['port']
        self.session.proxies =  {
            'http': 'http://' + self.proxy,
            'https': 'https://' + self.proxy,
        }
        print('Proxy changed:', self.proxy)


if __name__ == "__main__":
    scraper = Google_Scholar_Scraper()
    query = 'machine learning paper'
    results = scraper.scrap(query)
    print(results)
