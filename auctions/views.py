from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Auction, Bid, Comment, WatchListEntry, Comment, Category


def index(request):
    auctions = sorted(Auction.objects.filter(isActive=True), key=lambda auction: auction.time, reverse=True)
    
    auction_price = []
    for auction in auctions:
        bids = Bid.objects.filter(auction=auction)
        if len(bids) == 0:
            auction_price.append([auction, auction.startingBidAmount])
        else:
            largest = bids[0]
            for bid in bids:
                if bid.amount > largest.amount:
                    largest = bid
            auction_price.append([auction, largest.amount])


    return render(request, "auctions/index.html", {
        "auction_price": auction_price
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

@login_required
def comment(request):
    if request.method == "POST":
        userid = request.POST["userid"]
        auctionid = request.POST["auctionid"]
        user = User.objects.get(id=userid)
        auction = Auction.objects.get(id=auctionid)
        newComment = Comment(user=user, auction=auction, comment=request.POST["comment"])
        newComment.save()
        return HttpResponse("success")
    else:
        return HttpResponse("No GET method allowed")

def createListing(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            current_user = User.objects.filter(username=request.user.username)[0]
            auction = Auction(
                title=request.POST["title"],
                description=request.POST["description"],
                startingBidAmount=request.POST["startingBidAmount"],
                userPosted=current_user
            )
            if request.POST["imageURL"] != '':
                if request.POST["category"] != '':
                    auction = Auction(
                        title=request.POST["title"],
                        description=request.POST["description"],
                        startingBidAmount=request.POST["startingBidAmount"],
                        userPosted=current_user,
                        imageURL= request.POST["imageURL"],
                        category=request.POST["category"]
                    )
                    #see if we add the category
                    categories = Category.objects.all()
                    doNotAdd = False
                    for c in categories:
                        if c.name == auction.category:
                            doNotAdd = True
                    if not doNotAdd:
                        #add the category
                        newC = Category(name=auction.category)
                        newC.save()
                else:
                    auction = Auction(
                        title=request.POST["title"],
                        description=request.POST["description"],
                        startingBidAmount=request.POST["startingBidAmount"],
                        userPosted=current_user,
                        imageURL= request.POST["imageURL"]
                    )

            elif request.POST["category"] != '':
                auction = Auction(
                    title=request.POST["title"],
                    description=request.POST["description"],
                    startingBidAmount=request.POST["startingBidAmount"],
                    userPosted=current_user,
                    category=request.POST["category"]
                )
                #see if we add the category
                categories = Category.objects.all()
                doNotAdd = False
                for c in categories:
                    if c.name == auction.category:
                        doNotAdd = True
                if not doNotAdd:
                    #add the category
                    newC = Category(name=auction.category)
                    newC.save()


            auction.save()

                

            print(Auction.objects.all())
            return HttpResponse("success")
        else:
            return HttpResponse("failure")

    return render(request, "auctions/createListing.html")

def category(request, name):
    c = Category.objects.filter(name=name)[0]
    auctions = sorted(Auction.objects.filter(category=c.name), key=lambda auction: auction.time, reverse=True)
    return render(request, "auctions/category.html",{
        "category": c,
        "auctions": auctions
    })


def listing(request, id):
    auction = Auction.objects.get(id=id)
    comments = Comment.objects.filter(auction=auction)
    isWatched = False
    isPoster = False
    isWinner = False 
    if request.user.is_authenticated:
        current_user = User.objects.filter(username=request.user.username)[0]

        if auction.userPosted.username == current_user.username:
            isPoster = True
        
        bids = Bid.objects.filter(auction=auction)

        if len(WatchListEntry.objects.filter(user=current_user).filter(auction=auction)) > 0:
            isWatched = True

        if len(bids) > 0:
            #find largest bid
            largest = bids[0]
            for i in range(0, len(bids)):
                if bids[i].amount > largest.amount:
                    largest = bids[i]

            if auction.isActive == False:
                users_bids = Bid.objects.filter(auction=auction).filter(userPosted=current_user)

                if len(users_bids) > 0:
                    for bid in users_bids:
                        if bid.amount == largest.amount:
                            isWinner = True
                            break
            return render(request, "auctions/listing.html", {
                "auction": auction,
                "isWatched": isWatched,
                "largestAmount": largest.amount,
                "isPoster": isPoster,
                "comments": comments,
                "isWinner": isWinner
            }) 
        
        return render(request, "auctions/listing.html", {
            "auction": auction,
            "isWatched": isWatched,
            "isPoster": isPoster,
            "comments": comments,
            "isWinner": isWinner
        })
        
    return render(request, "auctions/listing.html", {
        "auction": auction,
        "isWatched": isWatched,
        "isPoster": isPoster,
        "comments": comments,
        "isWinner": isWinner
    })

@login_required
def watchlist(request):
    if request.method == "POST":
        userid = request.POST["userid"]
        auctionid = request.POST["auctionid"]
        user = User.objects.get(id=userid)
        auction = Auction.objects.get(id=auctionid)
        if len(WatchListEntry.objects.filter(user=user).filter(auction=auction)) == 0:
            #we then add it to the watchlist
            newEntry = WatchListEntry(
                user=user,
                auction=auction
            )
            newEntry.save()
            return HttpResponse("Added new watchlist entry")
        else:
            #we remove it
            WatchListEntry.objects.filter(user=user).filter(auction=auction).delete()

            return HttpResponse("Deleted")
    elif request.method == "GET":
        if request.user.is_authenticated:
            current_user = User.objects.filter(username=request.user.username)[0]
            watched = WatchListEntry.objects.filter(user=current_user)
            auctions = []
            for w in watched:
                auctions.append(w.auction)
            auctions = sorted(auctions, key=lambda auction: auction.time, reverse=True)
            auction_price = []
            for auction in auctions:
                bids = Bid.objects.filter(auction=auction)
                if len(bids) == 0:
                    auction_price.append([auction, auction.startingBidAmount])
                else:
                    largest = bids[0]
                    for bid in bids:
                        if bid.amount > largest.amount:
                            largest = bid
                    auction_price.append([auction, largest.amount])
            return render(request, "auctions/watchlist.html", {
                "auction_price": auction_price
            })
        else:
            return HttpResponse("User not signed in...")
    else:
        return HttpResponse("page does not exist")

@login_required
def bid(request):
    if request.method == "POST":
        userid = request.POST["userid"]
        auctionid = request.POST["auctionid"]
        user = User.objects.get(id=userid)
        auction = Auction.objects.get(id=auctionid)

        if auction.isActive:
            amount = request.POST["amount"]
            bids = Bid.objects.filter(auction=auction)
            if auction.startingBidAmount > float(amount):
                return HttpResponse("Error: Bid not larger than starting bid")
            if len(bids) > 0:
                for bid in bids:
                    if bid.amount >= float(amount):
                        return HttpResponse("Error: Bid not larger than the current bid")
            
            newBid = Bid(userPosted=user, amount=amount, auction=auction)
            newBid.save()
            return HttpResponse("New bid made")
        else:
            return HttpResponse("Auction is closed. No more bids are accepted")
    else:
        return HttpResponse("page does not exist")

@login_required
def close(request):
    if request.method == "POST":
        userid = request.POST["userid"]
        auctionid = request.POST["auctionid"]
        auction = Auction.objects.get(id=auctionid)
        user = User.objects.get(id=userid)
        if user == auction.userPosted:
            auction.isActive = False
            auction.save()
            return HttpResponse("Auction closed")
        else:
            return HttpResponse("You are not the person that posted this bid!")

    return HttpResponse("Error: no get requests")