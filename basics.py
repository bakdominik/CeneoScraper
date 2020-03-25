import requests
from bs4 import BeautifulSoup


# URL adress
ceneo = "https://www.ceneo.pl/"
product_id = input("Podaj id produktu: ")
url_postfix = "#tab=reviews"
url = ceneo+product_id+url_postfix
# get html code of opinion
page = requests.get(url)
soup = BeautifulSoup(page.text,'html.parser')
# select opinions from html code
opinions = soup.select("li.js_product-review")

# list to store all opinions dictionary
opinions_list = []

# get single opinion components from opinions
while url:
    for opinion in opinions:

        opinion_id=opinion["data-entry-id"]
        author = opinion.select('div.reviewer-name-line').pop().string.strip()
        try:
            recomendation = opinion.select('div.product-review-summary > em').pop().string.strip()
        except:
            recomendation = None
        stars = opinion.select('span.review-score-count').pop().string.strip()
        try:
            confirmed_by_purchase = opinion.select("div.product-review-pz").pop().string.strip()
        except:
            confirmed_by_purchase = purchased = None
        issue_date = opinion.select('span.review-time > time')[0]["datetime"]
        try:
            purchase_date = opinion.select('span.review-time > time')[1]["datetime"]
        except:
            purchase_date = None
        usefull = opinion.select('button.vote-yes').pop()["data-total-vote"]
        useless = opinion.select('button.vote-no').pop()["data-total-vote"]
        content = opinion.select('p.product-review-body').pop().get_text().strip()
        try:
            cons = opinion.select('div.cons-cell > ul').pop().get_text().strip()
        except IndexError:
            cons = None
        try:
            pros = opinion.select('div.pros-cell > ul').pop().get_text().strip()
        except IndexError:
            pros = None

        # creating dictionary with all elements of opinion = 
        opinion_elements = {
            "opinion_id":opinion_id,
            "author":author,
            "recomendation":recomendation,
            "stars":stars,
            "confirmed_by_purchase":confirmed_by_purchase,
            "issue_date":issue_date,
            "purchase_date":purchase_date,
            "usefull":usefull,
            "useless":useless,
            "content":content,
            "cons":cons,
            "pros":pros
        }
        opinions_list.append(opinion_elements)
    
    try:
        url = ceneo+page_tree.select("a.pagination__next").pop()["href"]
    except IndexError:
        url = False

print(opinions_list[0])



