from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from .models import User,New_Listing,get_categories,New_Bid,New_Comment,WatchList,Winner

class NewListForm(forms.Form):
    title = forms.CharField(label = "Enter your listing title:",max_length = 64)
    description = forms.CharField(label = "Item descrition:",widget=forms.Textarea())
    starting_bid = forms.FloatField(label = "Starting Bid:")
    url_image = forms.URLField(label = "URL with an image of the item" , required=False)
    category_choices = get_categories()
    category = forms.ChoiceField(label = "Category of the item",required=False,choices = category_choices)

class NewBidAdd(forms.Form):
    bid_value = forms.FloatField(label="Enter bid value:")
    user_id = forms.CharField(widget = forms.HiddenInput())

class NewComment(forms.Form):
    title = forms.CharField(label = "Comment title:",max_length = 64)
    body = forms.CharField(label = "Comment body:",widget=forms.Textarea())
    user_id = forms.CharField(widget = forms.HiddenInput())
    listing_id = forms.CharField(widget = forms.HiddenInput())


def index(request):
    Listings = New_Listing.objects.all().values()
    Users = User.objects.all().values()
    message = None
    if request.method == 'POST':
        Comment = NewComment(request.POST)
        if Comment.is_valid():
            title = Comment.cleaned_data['title']
            body = Comment.cleaned_data['body']
            user_id = Comment.cleaned_data['user_id']
            listing_id = Comment.cleaned_data['listing_id']
            AddComment = New_Comment(
                user_id = User.objects.get(id=user_id),
                listing_id = New_Listing.objects.get(listing_id=listing_id),
                title = title,
                body = body
            )
            AddComment.save()       
            message = "Your comment has been added!"
    return render(request, "auctions/index.html",{
        "categories":categories,
        "message": message,
        "Listings": Listings,
        "Users" : Users
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
                "mesage": "Invalid username and/or password."
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

@login_required
def new_listing(request):
    Listings = New_Listing.objects.all().values()
    if request.method == 'POST':
        form = NewListForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            starting_bid = form.cleaned_data['starting_bid']
            url_image = form.cleaned_data['url_image']
            category = form.cleaned_data['category']
            Listing = New_Listing(
                title=title,
                user=User.objects.get(id=request.user.id),
                description=description,
                bid=starting_bid,
                last_bid = 0,
                url_image=url_image,
                category=category
            )
            Listing.save()
        message="Your listing has been succesfully created!"
        Listings = New_Listing.objects.all().values()
        return render(request, 'auctions/index.html', {
            'message': message,
            "Listings":Listings
        })
    else:
        form = NewListForm()
        return render(request, 'auctions/new_listing.html', {
            'form': form,
            })

@login_required
def listing(request,listing_name):
    Users = User.objects.all().values()
    View_Listing = New_Listing.objects.filter(title=listing_name).values()[0]
    View_Comments = New_Comment.objects.filter(listing_id=View_Listing['listing_id']).values()
    in_watchlist = None
    try:
        in_watchlist = WatchList.objects.get(user_id = request.user.id,listing_id = View_Listing['listing_id'])
    except:
        in_watchlist = None
    message = None
    if request.method == 'POST':
        New_Bids = NewBidAdd(request.POST)
        if New_Bids.is_valid():
            bid_value = New_Bids.cleaned_data['bid_value']
            if bid_value < View_Listing['bid']:
                message="Suma invalida! Introdu o suma mai mare!"
            else:
                user_id = New_Bids.cleaned_data['user_id']
                BidAdd = New_Bid(
                    listing_id = New_Listing.objects.get(listing_id = View_Listing['listing_id']),
                    user_id = user_id,
                    new_bid = bid_value
                )
                BidAdd.save()
                message="Your bid has been succesfully added!"
                UpdateListing = New_Listing.objects.get(listing_id=View_Listing['listing_id'])
                UpdateListing.last_bid = View_Listing['bid']
                UpdateListing.bid = bid_value
                UpdateListing.save()
        else:
            winner = None
            winner_id = None
            last_bid = None
            if(View_Listing['last_bid'] == 0):
                winner = request.user.username
                winner_id = request.user.id
                max_bid = View_Listing['bid']
            else:
                max_bid = New_Bid.objects.filter(listing_id=View_Listing['listing_id']).aggregate(Max('new_bid'))['new_bid__max']
                winner_id = New_Bid.objects.get(new_bid=max_bid,listing_id=View_Listing['listing_id']).user_id
                winner = User.objects.get(id=winner_id).username
            UpdateListing = New_Listing.objects.get(listing_id=View_Listing['listing_id'])
            UpdateListing.closed = 1
            UpdateListing.save()
            NewWin = Winner(
                user_id = User.objects.get(id=winner_id),
                listing_id = New_Listing.objects.get(listing_id=View_Listing['listing_id']),
                price = max_bid
            )
            NewWin.save()
            message = str(winner) + " has won the auction at " + str(max_bid) + "$!!"
    View_Listing = New_Listing.objects.filter(title=listing_name).values()[0]      
    New_Bids = NewBidAdd()
    Comment = NewComment()
    if(View_Listing['closed'] == 1):
        Get_win = Winner.objects.get(listing_id = View_Listing['listing_id'])
        winner = User.objects.get(username=Get_win.user_id)
        if(request.user.id == winner.id):
            message = "You won the auction at " + str(Get_win.price) + "$!!"
    return render(request, 'auctions/listing.html',{
        "message": message,
        'in_watchlist': in_watchlist,
        "Comment": Comment,
        "form": New_Bids,
        "View_Comments": View_Comments,
        "Listing": View_Listing,
        "Users": Users
    })

@login_required
def watchlist(request,user):
    WL = []
    user_id = request.user.id
    View_watchlist = WatchList.objects.filter(user_id=user_id).all().values()
    for listing in View_watchlist:
            WL.append(New_Listing.objects.get(listing_id=listing['listing_id_id']))
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        in_watchlist = request.POST['in_watchlist']
        if(in_watchlist):
            del_watchlist = WatchList.objects.filter(user_id = user_id,listing_id = listing_id)
            del_watchlist.delete()
            message = "Listing removed from watchlist"
            return render(request, 'auctions/watchlist.html', {
                "watchlist": WL,
                'message':message
            })
        elif(in_watchlist == ""):
            #add
            addWatchlist = WatchList(
            listing_id = New_Listing.objects.get(listing_id=listing_id),
            user_id = User.objects.get(id=user_id)
            )
            addWatchlist.save()
            message = "Listing added to watchlist!"
            return render(request, 'auctions/watchlist.html', {
                "watchlist": WL,
                'message':message
            })
    else:
        return render(request, 'auctions/watchlist.html',{
            "watchlist": WL
        })


@login_required
def categories(request):
    choices = get_categories()
    categories = [item[1] for item in choices]
    return render(request, "auctions/categories.html",{
        "choices": categories
    })

@login_required
def category(request,ctg):
    choices = get_categories()
    category_choice = None
    for code,name in choices:
        if ctg == name:
            category_choice = code
            break
    category_listings = New_Listing.objects.filter(category=code).values()
    return render(request, "auctions/category.html",{
        "name": ctg,
        "Listings": category_listings
    })
