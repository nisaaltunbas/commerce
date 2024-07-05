from django.contrib.auth.models import AbstractUser
from django.db import models

class Category(models.Model):
    ctgName = models.CharField(max_length=100)

    def __str__(self):
        return self.ctgName

class User(AbstractUser):
    pass

class Bid(models.Model):
    bid = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userBid")

    def __str__(self):
        return str(self.bid)
    
   

class Listing(models.Model):
    title=models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    price=models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bidPrice")
    image_url = models.CharField(max_length=1000)
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, 
    related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="userWatchlist")

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userCom")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listingCom")
    message = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.author} comment on {self.listing}"
    
