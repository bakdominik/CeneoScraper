import requests
from bs4 import BeautifulSoup


# URL adress

url = "https://www.ceneo.pl/76891701#tab=reviews"


# get html code of opinion

import requests


page = requests.get(url).text

# get single opinion elements from html

soup = BeautifulSoup(page,'html.parser')

opinion = soup.select("li.review-box")[0]
opinion_id = opinion["data-entry-id"]
author = opinion.select('div.reviever-name-line').pop().string()
recomendation = opinion.select('.product-review-summary > em')
stars = opinion.select('span.review-score-count')
confirmed_bought = opinion.select("div.product-review-pz")
useful = opinion.select('button.vote-yes').pop()['data-total-vote']
date_posted = opinion.select("time[datetime]")
date_bought = opinion.select("time[datetime]")



print(opinion)

# - opinia: li.review-box
# - identyfikator: li.review-box["data-entry-id"] 
# - autor: div.reviever-name-line
# - rekomendacja: .product-review-summary > em
# - liczba gwiazdek: span.review-score-count
# - czy potwierdzona zakupem: div.product-review-pz
# - data wystawienia: time['datetime']
# - data zakupu: time['datetime']
# - przydatna: button.vote-yes['data-total-vote']
# - nieprzydatna: button.vote-no['data-total-vote']
# - treść: p.product-reveiew-body
# - wady: div.cons-cell > ul
# - zalety: div.pros-cell > ul


# ekstrakcja skladowych dla pierwszwj opinii


