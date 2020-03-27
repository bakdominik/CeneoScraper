from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Opinion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.IntegerField()
    opinion_id = models.IntegerField()
    author = models.CharField(max_length=255)
    recomendation = models.BooleanField()
    stars = models.IntegerField()
    confirmed_by_purchase = models.BooleanField()
    issue_date = models.DateField(blank=True,null=True)
    purchase_date = models.DateField(blank=True,null=True)
    usefull = models.IntegerField()
    useless = models.IntegerField()
    content = models.CharField(max_length=500)
    cons = models.CharField(max_length=255,blank=True,null=True)
    pros = models.CharField(max_length=255,blank=True,null=True)

class Product(models.Model):
    product_id = models.IntegerField()
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    opinions = models.IntegerField()
    mean_stars = models.FloatField()
    pros = models.IntegerField()
    cons = models.IntegerField()
    
    def __str__(self):
        return self.name
    