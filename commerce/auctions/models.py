from django.contrib.auth.models import AbstractUser
from django.db import models

def get_categories():
    CATEGORY_CHOICES = [
        ("None", "None"),
        ('New', 'New'),
        ('Used', 'Used'),
        ('Junk', 'Junk'),
        ]
    return CATEGORY_CHOICES
    
class User(AbstractUser):
    pass    

# Create the listing model
class New_Listing(models.Model):
    listing_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=256)
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    last_bid = models.DecimalField(max_digits=10, decimal_places=2)
    url_image = models.URLField()
    category_choices = get_categories()
    closed = models.DecimalField(max_digits=1, decimal_places=0,default=0)
    category = models.CharField(max_length=20, choices=category_choices)
    dateTime = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.title} created by {self.user.username}"

class WatchList(models.Model):
    watchlist_id = models.AutoField(primary_key=True)
    listing_id = models.ForeignKey(New_Listing, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    dateTime = models.DateTimeField(auto_now_add=True)

# Create the Bid model
class New_Bid(models.Model):
    bid_id = models.AutoField(primary_key=True)
    listing_id = models.ForeignKey(New_Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    new_bid = models.DecimalField(max_digits=10, decimal_places=2)
    dateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid {self.new_bid} by {self.user.username}"

class New_Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id  = models.ForeignKey(New_Listing, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    body = models.TextField(max_length=256) 
    dateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} with {self.body}"

class Winner(models.Model):
    win_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id  = models.ForeignKey(New_Listing, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    dateTime = models.DateTimeField(auto_now_add=True)