from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django import forms

# Create your models here.

class Opinion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.IntegerField()
    opinion_id = models.IntegerField()
    author = models.CharField(max_length=255)
    recomendation = models.CharField(max_length=255)
    stars = models.IntegerField()
    confirmed_by_purchase = models.BooleanField()
    issue_date = models.DateField(blank=True,null=True)
    purchase_date = models.DateField(blank=True,null=True)
    usefull = models.IntegerField()
    useless = models.IntegerField()
    content = models.CharField(max_length=2000)
    cons = models.CharField(max_length=255,blank=True,null=True)
    pros = models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return self.content



class Product(models.Model):
    product_id = models.IntegerField()
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    opinions = models.IntegerField()
    mean_stars = models.DecimalField(max_digits=3, decimal_places=2)
    pros = models.IntegerField()
    cons = models.IntegerField()
    slug = models.SlugField()

    def __str__(self):
        return self.name
    
     # unique url of product
    def get_absolute_url(self):
        return reverse('opinions', kwargs={
            'slug': self.product_id,
        })

