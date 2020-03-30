from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from . models import Product,Opinion
import requests
from bs4 import BeautifulSoup
from django.core.serializers import serialize
from django.views.generic import ListView, TemplateView
# Create your views here.


class HomeView(TemplateView):
    template_name = 'home.html'

class AuthorView(TemplateView):
    template_name = "author.html"

class ProductOpinionsView(ListView):
    template_name = "core/opinions.html"
    model = Opinion

    def get_queryset(self, **kwargs):
        return Opinion.objects.filter(product_id=self.kwargs['slug'],user=self.request.user)

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

            if page.status_code == 200:
                soup = BeautifulSoup(page.text, 'html.parser')
                # select opinions from html code
                opinions = soup.select("li.js_product-review")
                if opinions:
                    # if user already extracted product opinions, raise error
                    if Product.objects.filter(user=request.user,product_id=product_id):
                        return render(request,'core/extract.html', {'error':'Opinie do tego produktu zostały już pobrane'})
                    # if user didnt extract product opinions yet, create Product and Opinions objects
                    else:
                        # create Product object

                        product = Product()
                        product.opinions = 0
                        product.name = soup.select('h1.product-name').pop().string.strip()
                        product.product_id = product_id
                        product.user = request.user
                        product.pros = 0 #number of opinions with pros
                        product.cons = 0 #number of opinions with cons
                        stars = [] #used to count mean of stars

                        while url:
                            # get single opinion components from opinions, create opinion object
                            for opinion in opinions:
                                product.opinions += 1
                                op = Opinion()
                                op.user = request.user
                                op.product_id = product_id
                                op.opinion_id = opinion["data-entry-id"]
                                op.author = opinion.select('div.reviewer-name-line').pop().string.strip()
                                try:
                                    op.recomendation = opinion.select('div.product-review-summary > em').pop().string.strip()
                                except:
                                    op.recomendation = 'BRAK'
                                op.stars = opinion.select('span.review-score-count').pop().string[0]
                                stars.append(int(op.stars))
                                try:
                                    if opinion.select("div.product-review-pz > em").pop().string.strip():
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
                                    'p.product-review-body').pop().get_text().strip().replace('\r', ', ').replace('\n', ', ')
                                try:
                                    op.cons = opinion.select(
                                        'div.cons-cell > ul').pop().get_text().strip().replace('\r', ', ').replace('\n', ', ')
                                    product.cons += 1
                                except IndexError:
                                    op.cons = ''
                                try:
                                    op.pros = opinion.select(
                                        'div.pros-cell > ul').pop().get_text().strip().replace('\r', ', ').replace('\n', ', ')
                                    product.pros += 1
                                except IndexError:
                                    op.pros = ''
                                op.save()
                            
                            try:
                                url = ceneo+soup.select("a.pagination__next").pop()["href"]
                                page = requests.get(url)

                                if page.status_code == 200:
                                    soup = BeautifulSoup(page.text, 'html.parser')
                                    # select opinions from html code
                                    opinions = soup.select("li.js_product-review")
                            except:
                                url = False

                        product.mean_stars = sum(stars)/len(stars)
                        product.save() #save Product object ot database

                        return redirect('extract')
                else:
                    # raise product already extracted error
                    return render(request,'core/extract.html', {'error':'Ten produkt nie posiada opinii'})
            else:
                # raise invalid id error
                return render(request,'core/extract.html', {'error':'ID nieprawidłowe'})
        # raise id required error
        return render(request,'core/extract.html', {'error':'Musisz podać ID produktu żeby pobrać opinię'})
    else:
        return render(request, 'core/extract.html')

@login_required()
def products(request):
    if request.method == 'POST':
        id_ = request.POST['product_id']
        data = serialize('json', Opinion.objects.filter(user=request.user,product_id=id_))
        response = HttpResponse(data, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="opinie.json"'
        response['Content-Length'] = len(response.content)
        return response
    else:
        products = Product.objects.filter(user=request.user)
        return render(request,'core/products.html', {'products':products})
    
def charts(request,**kwargs):
    # all opinions to selected product
    recomended = Opinion.objects.filter(user=request.user,product_id=kwargs['slug'],recomendation='Polecam')
    unrecomended = Opinion.objects.filter(user=request.user,product_id=kwargs['slug'],recomendation='Nie polecam')
    opinions = Opinion.objects.filter(user=request.user,product_id=kwargs['slug'],)

    stars=[0,0,0,0,0,0]
    for opinion in opinions:
        rate = opinion.stars
        stars[rate] += 1

    data = [len(recomended),len(unrecomended)]
    labels = ['Polecam','Nie polecam']
    return render(request, 'core/charts.html',{
        'stars': stars,
        'recomendations': data,
        'rec_labels': labels,
        'slug': kwargs['slug']
    })


    