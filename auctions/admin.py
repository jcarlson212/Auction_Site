from django.contrib import admin
from .models import User, Bid, Auction, Comment, WatchListEntry, Category

# Register your models here.
admin.site.register(User)
admin.site.register(Auction)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(WatchListEntry)
admin.site.register(Category)
