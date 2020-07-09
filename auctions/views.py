from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction, Bid, Comment


def index(request):
    auctions = sorted(Auction.objects.all(), key=lambda auction: auction.time, reverse=True)
    return render(request, "auctions/index.html", {
        "auctions": auctions
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


            auction.save()
            print(Auction.objects.all())
            return HttpResponse("success")
        else:
            return HttpResponse("failure")

    return render(request, "auctions/createListing.html")