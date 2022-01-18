from bs4 import BeautifulSoup
import time
import io
import requests
# file = open('html.txt',"a",encoding="utf-8")



webpage = requests.get('https://economictimes.indiatimes.com/markets/stocks/recos')
# time.sleep(2)
# print(webpage.status_code)
# file.write(webpage.text)
soup = BeautifulSoup(webpage.text, 'html.parser')
# file.close()
titles = set()
# dates = list()
for i in range(50):
    try:
        title = soup.find_all('h3')[i].get_text()
        # date = soup.find_all('time')[i].get_text()
    except:
        pass
    if 'target price' in title:
        titles.add(title)
        # dates.append(date)
# for i in range(len(titles)):
#     print(list(titles)[i].split())
    # print(dates[i])
    
