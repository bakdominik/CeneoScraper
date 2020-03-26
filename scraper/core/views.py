from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from . models import Product,Opinion
import requests
from bs4 import BeautifulSoup
# Create your views here.


def home(request):
    return render(request, 'core/home.html')


@login_required()
def extract(request):
    if request.method == 'POST':
        if request.POST.get('product_id'):

             # URL adress
            ceneo = "https://www.ceneo.pl/"
            product_id = request.POST.get('product_id')
            url_postfix = "#tab=reviews"
            url = ceneo+product_id+url_postfix

            # get html code of opinion
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            # select opinions from html code
            opinions = soup.select("li.js_product-review")

            # create Product object
            product = Product()
            product.name = soup.select('h1.product-name').pop().string.strip()
            product.product_id = product_id
            product.user = request.user
            product.save()

            # get single opinion components from opinions, create opinion object
            while url:
                for opinion in opinions:
                    op = Opinion()
                    op.product_id = product_id
                    op.opinion_id = opinion["data-entry-id"]
                    op.author = opinion.select('div.reviewer-name-line').pop().string.strip()
                    try:
                        if opinion.select('div.product-review-summary > em').pop().string.strip() == "Polecam":
                            op.recomendation = True
                    except:
                        op.recomendation = None
                    op.stars = opinion.select('span.review-score-count').pop().string[0]
                    try:
                        if opinion.select("div.product-review-pz").pop().string.strip():
                            op.confirmed_by_purchase = True
                    except:
                        op.confirmed_by_purchase = False
                    op.issue_date = opinion.select('span.review-time > time')[0]["datetime"].split(' ')[0]
                    try:
                        op.purchase_date = opinion.select(
                            'span.review-time > time')[1]["datetime"].split(' ')[0]
                    except:
                        op.purchase_date = None
                    op.usefull = opinion.select('button.vote-yes').pop()["data-total-vote"]
                    op.useless = opinion.select('button.vote-no').pop()["data-total-vote"]
                    op.content = opinion.select(
                        'p.product-review-body').pop().get_text().strip()
                    try:
                        op.cons = opinion.select(
                            'div.cons-cell > ul').pop().get_text().strip()
                    except IndexError:
                        op.cons = ''
                    try:
                        op.pros = opinion.select(
                            'div.pros-cell > ul').pop().get_text().strip()
                    except IndexError:
                        op.pros = ''
                    op.save()
                try:
                    url = ceneo+soup.select("a.pagination__next").pop()["href"]
                except IndexError:
                    url = False

            
        else:
            # komunikat o błędnym id
            pass
        return redirect('extract')
    else:
        return render(request, 'core/extract.html')
