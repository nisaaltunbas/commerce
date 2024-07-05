from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User,Category,Listing,Comment,Bid


def index(request):
    activeListings = Listing.objects.filter(isActive = True)
    allCategories = Category.objects.all()
    return render(request, "auctions/index.html",{
        "listings": activeListings,
        "categories" : allCategories
    })

def listing(request,id):
    listingData = Listing.objects.get(pk=id)
    isLstInWatchList = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.owner.username
    return render(request,"auctions/listing.html",{
        "listing" : listingData,
        "isLstInWatchList":isLstInWatchList,
        "allComments" : allComments,
        "isOwner": isOwner
    })

def closeAuction(request,id):
    listingData = Listing.objects.get(pk=id)
    listingData.isActive = False
    listingData.save()
    isLstInWatchList = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.owner.username

    return render(request,"auctions/listing.html",{
        "listing" : listingData,
        "isLstInWatchList":isLstInWatchList,
        "allComments" : allComments,
        "update": True,
        "isOwner": isOwner,
        "message": "Congrulations, your auction is closed!"
    })

def addBid(request,id):
    newBid = request.POST['newBid']
    listingData = Listing.objects.get(pk=id)
    isLstInWatchList = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.owner.username
    if float(newBid) > listingData.price.bid:
        updateBid = Bid(user=request.user, bid=float(newBid))
        updateBid.save()
        listingData.price = updateBid
        listingData.save()
        return render(request, "auctions/listing.html",{
            "listing":listingData,
            "message":"Bid was updated successfully",
            "update":True,
            "isOwner": isOwner,
            "isLstInWatchList":isLstInWatchList,
            "allComments" : allComments
        })
    else:
         return render(request, "auctions/listing.html",{
            "listing":listingData,
            "message":"Bid updated failed",
            "update":False,
            "isLstInWatchList":isLstInWatchList,
            "isOwner": isOwner,
            "allComments" : allComments
         })

def displayWatchlist(request):
    listings = currentUser.userWatchlist.all()
    currentUser = request.user
    return render(request, "auctions/watchlist.html", {
        "listings" : listings
    })

def addCom(request, id):
    currentUser = request.user
    listingData = Listing.objects.get(pk=id)
    message = request.POST['newCom']

    newCom = Comment(
        author = currentUser,
        listing=listingData,
        message = message
    )

    newCom.save()

    return HttpResponseRedirect(reverse("listing",args=(id, )))



def removeWatchlist(request, id):
    currentUser = request.user
    listingData = Listing.objects.get(pk=id)
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing",args=(id, )))

def addWatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing",args=(id, )))

def displayCategory(request):
    if request.method == "POST":
        categoryForm = request.POST['category']
        category = Category.objects.get(ctgName = categoryForm)
        activeListings = Listing.objects.filter(isActive = True,category = category)
        allCategories = Category.objects.all()
        return render(request, "auctions/index.html",{
            "listings": activeListings,
            "categories" : allCategories
    })
    

def create_listing(request):
    if request.method == "GET":
        allCategories = Category.objects.all()
        return render(request,"auctions/create.html",{
            "categories" : allCategories
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        imageUrl = request.POST["imageurl"]
        price = request.POST["price"]
        category = request.POST["category"]

        currentUser = request.user

        categoryData = Category.objects.get(ctgName = category)

        bid = Bid(bid=float(price), user=currentUser)
        bid.save()

        newListing = Listing(
            title = title,
            description = description,
            image_url = imageUrl,
            price = bid,
            category = categoryData,
            owner = currentUser
        )
        newListing.save()
        return HttpResponseRedirect(reverse(index))
        

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
