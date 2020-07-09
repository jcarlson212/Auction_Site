from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=30, unique=True)
    def __str__(self):
        return self.username + ", " + self.email


class Auction(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    startingBidAmount = models.FloatField()
    currentAmount = models.FloatField(null=True)
    userPosted = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, blank=True)
    time = models.TimeField(auto_now=True, blank=True)
    imageURL = models.URLField(null=True)
    category = models.CharField(max_length=30, null=True)
    def __str__(self):
        return self.title + ", " + self.description + ", " + str(self.startingBidAmount)


class Bid(models.Model):
    userPosted = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, blank=True)
    def __str__(self):
        return "bid: " + str(self.amount) + ", " + str(self.date)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    comment = models.CharField(max_length=300)
    date = models.DateField(auto_now_add=True, blank=True)
    def __str__(self):
        return "comment: " + self.comment + ", " + str(self.date)


allUsers = User.objects.all()
print(allUsers)