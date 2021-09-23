import datetime
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
# from django.db.models.query import ValuesQuerySet
from django.db.utils import DatabaseError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from operator import itemgetter
from django.core import serializers
from django import forms
from django.http import JsonResponse, HttpResponseBadRequest
from django.db.models import Q


from .models import User, Post, Follow, EditForm, Like



class newEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="write your entry here")

def index(request):
    allposts = Post.objects.all().order_by('-time_added') 
    for post in allposts:
        post.likes = Like.objects.filter(post=post).count()
        post.save() 
    vals = allposts.values_list('id', 'user', 'user_name', 'post', 'time_added', 'likes')
    smem = Like.objects.filter(liker=request.user.id) 
    smeg = smem.values_list('post')
    liked_posts = []
    for i in smeg:
        liked_posts.append(i[0])
    print("liked posts", liked_posts)
    #get a push all liked post numbers to a format where the in operator can be used. 
    paginator = Paginator(vals, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    hello = vals[3]
    print("hello there: ", hello)
    form = EditForm({'id': vals[0], 'post': hello})
 

  
    return render(request, "network/index.html", {
        "vals": vals,
        "page_obj": page_obj,
        "form": form,
        "liked_posts": liked_posts
      
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required()
def submit_post(request):
    postie = " "
    if request.method == "POST":
        postie = Post()
        postie.post = request.POST.get('submitto')
        postie.user = request.user
        postie.user_name = request.user.username
        postie.time_added = datetime.datetime.now()
        postie.save()
        return redirect(request.META['HTTP_REFERER']) 

def load_profile(request, id):
    #to-do query Posts database for all posts for the user with the ID passed in
    form = EditForm()
    profileposts = Post.objects.filter(user=id).order_by('-time_added')
    # If profileposts isn't null / empty then process as below and feed into render section
    #gets all the posts from the user id passed into the function
    for post in profileposts:
        post.likes = Like.objects.filter(post=post).count()
        post.save() 
    valus = profileposts.values_list('id', 'user', 'user_name', 'post', 'time_added', 'likes') #displays all the informatin about the above posts 
    user1 = User.objects.filter(id=id)
    user_1 = user1.values_list('id', 'username')
    followz = Follow.objects.filter(follower=id) #gets all of the instances of a follow where the follower matches ID passed into function
    follow_values = followz.values_list('followee_id') #processes the ID of the above 
    my_list = []
    for i in follow_values: #this loop takes the ID of all users followed by the user whose profile page u are on and prints out ID & username
        fv = User.objects.filter(id=i[0])
        followers = fv.values_list('id', 'username')
        my_list.append(followers)
    fol = Follow.objects.filter(followee=id)
    followed_by = fol.values_list('follower_id')  
    followers_list = []
    for i in followed_by:
        fl = User.objects.filter(id=i[0])
        flos = fl.values_list('id', 'username')
        followers_list.append(flos)
    smem = Like.objects.filter(liker=request.user.id) 
    smeg = smem.values_list('post')
    liked_posts = []
    for i in smeg:
        liked_posts.append(i[0])    
    paginator = Paginator(valus, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    smoo = Follow.objects.filter(follower=request.user.id, followee=id).exists() 
    print("this is valus:", valus)
    print("this is pee peooo page_objs", page_obj)
    return render(request, "network/profilepage.html", {
        "form" : form,
        "valus": valus,
        "user_1": user_1,
        "my_list": my_list,
        "smoo": smoo,
        "followers_list": followers_list,
        "page_obj": page_obj,
        "profileposts" : profileposts,
        "liked_posts": liked_posts
    })

def follow(request, id):
    if request.method == "POST":
        following = Follow()
        user = User.objects.get(id=id)
        following.follower = request.user
        following.followee = user
        following.save()
        return redirect('load_profile', id=id) 

def unfollow(request, id):
    if request.method == "POST":
        Follow.objects.filter(follower=request.user.id, followee=id).delete()     
        return redirect('load_profile', id=id) 

login_required()
def load_following(request):
    flow = Follow.objects.filter(follower=request.user.id)
    following = flow.values_list('followee')
    following_list = []
    for i in following:
        fols = Post.objects.filter(user=i[0]).order_by('-time_added') 
        followings = fols.values_list('id', 'user', 'user_name', 'post', 'time_added', 'likes')
        following_list.append(followings)
    new_list = []
    for sublist in following_list:
        for item in sublist:
            new_list.append(item)    
    smem = Like.objects.filter(liker=request.user.id) 
    smeg = smem.values_list('post')
    liked_posts = []
    for i in smeg:
        liked_posts.append(i[0]) 
    hello = new_list
    paginator = Paginator(hello, 10)
    page_number = request.GET.get('page', 2)
    page_obj = paginator.get_page(page_number)
    print(page_obj, ": page obj")
    return render(request, "network/following.html", {
        "page_obj": page_obj,
        "hello": hello,
        "following_list": following_list,
        "following": following,
        "liked_posts": liked_posts
    })

def pages(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 3)
    page_obj = paginator.get_page(1)
    page_number = request.GET.get('page', 1)
    pge = paginator.get_page(page_number)
    return render(request, 'network/index.html', {
        'page_obj': page_obj,
    })

def edit_post(request, id):
    form = EditForm(request.POST) 
    if request.is_ajax and request.method == "POST":
        if form.is_valid():
            data = form.cleaned_data
            post = data['post']
            print("this is data", data)
            name = request.user.username
            likes = Post.objects.filter(pk=id)
            likez = likes.values_list('likes')
            print(likez[0][0])
            now = datetime.datetime.now()
            time_added = now.strftime("%d %b, %Y, %H:%M:%S")	
            Post.objects.filter(pk=id).update(post=post)
            return JsonResponse({"post": post,
            "name": name,
            "time_added": time_added,
            "likes": likez[0][0]
            }, status=200)
        else:
            return JsonResponse({"error": form.errors}, status=400) 
    return JsonResponse({"error": ""}, status=400)
 
def like(request, id):
        user = User.objects.get(id=request.session['_auth_user_id'])
        post = Post.objects.get(id=id)
        print(user, post)  
        if Like.objects.filter(liker=user, post=post).exists(): 
            like = Like.objects.get(post=post, liker=user)
            like.delete()
        else:
            like = Like()
            like.liker = user
            like.post = post 
            like.save()
        total_likes = Like.objects.filter(post=post).count()   
        print(total_likes, ": total likes")   
        likescount = {
        'total_likes': total_likes }
        return JsonResponse({"likescount": likescount}, status=200)  #serializes the data and sends it back to the page?



