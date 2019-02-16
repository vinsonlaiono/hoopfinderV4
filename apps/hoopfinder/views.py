from django.shortcuts import render, redirect
from .models import *
from django.db import models
from django.contrib.auth.models import User
import json
# import request, random

def index(request):
    return render(request, "hoopfinder/landing.html")

def home(request):
    if 'userid' not in request.session:
        request.session['userid'] = 0
    if 'courtid' not in request.session:
        request.session['courtid'] = 0
    # current_user = User.objects.get(id = request.session['userid'])
    # context={
    #     'user': current_user
    # }
    # return render(request, "hoopfinder/newMain.html", context )
    return render(request, "hoopfinder/newMain.html")

def map(request):
    return render(request, "hoopfinder/maps.html")
    
def userdashboard(request):
    all_users = User.objects.all()
    print(all_users, "***********************")
    context= {
        'all_users': all_users
    }
    return render(request, "hoopfinder/usersNew.html", context)

def user_page(request, user_id):
    user = User.objects.get(id = user_id)
    current_user = User.objects.get(id = request.session['userid'])
    user_name = user.first_name
    print(user, "***********************")

    user_reviews = UserReviews.objects.filter(reviewed_user = User.objects.get(id = user_id))

    #first try to add friends
    # friends = user.users_friends.all()
    # friends_count = len(user.users_friends.all())

    # second try to add friends
    friend = Friend.objects.get(current_user = user_id)
    friends = friend.users.all()
    friends_count = len(friend.users.all())


    context= {
        'user': user,
        'friends': friends,
        'user_reviews': user_reviews,
        'friends_count': friends_count,
        'current_user': current_user
    }
    return render(request, "hoopfinder/userbootstrap.html", context)

def add_friend(request, user_id):

    current_user = User.objects.get(id = user_id)
    new_friend = User.objects.get(id = request.session['userid'])
    friend_manage = Friend.make_friend(Friend, current_user, new_friend)
    friend_manage_reverse = Friend.make_friend(Friend, new_friend, current_user)
    # friend_manage = Friend(friend = friend, friended_by = friended_by) the old query to add a friend
    # friend_manage.save()
    # friend_manage_reverse.save()


    return redirect('/user/' + user_id)

def users(request):
    return render(request, "hoopfinder/user_dashboard.html")

def courts(request):
    all_courts = Courts.objects.all()
    context = {
        "all_courts": all_courts
    }
    return render(request, "hoopfinder/courts.html", context)

def registration(request):
    return render(request, "hoopfinder/registration.html")

def register(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/registration')
        else:
            request.session['first_name'] = request.POST['first_name']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']

            #BCRYPT
            pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            confpassword = request.POST['confpassword']
           
            #create an account and push it to the database
            user2 = User.objects.create(first_name = first_name, last_name =last_name, email = email, password = pw)
            request.session['userid'] = user2.id
            
            # change this to userdashboard
            return redirect('/home')


def login(request):
    return render(request, "hoopfinder/login.html")

def login_post(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST) 
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            user1 = User.objects.get(email=request.POST['email'])
            request.session['userid'] = user1.id
            # change this to user dashboard
            print("youre logged in " + user1.first_name)
            return redirect('/user/'+str(user1.id))

def logout(request):
    request.session.clear()
    return redirect('/home')

def new_court(request):
    return render(request, "hoopfinder/new_court.html")

def add_court(request):
    if request.method == 'POST':
        name = request.POST['court_name']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zipcode = request.POST['zipcode']
        imagelink = request.POST['imagelink']        ######change this to a real file upload later##########

        Courts.objects.create(name = name, address = address, city = city, state = state, zipcode = zipcode, imagelink = imagelink)
        print("1 court is added")
    return redirect('/courts')

def show_court(request, id):
    if request.session['userid'] == 0:
        return redirect('/login')
    court = Courts.objects.get(id = id)
    user = User.objects.get(id = request.session['userid'])
    request.session['courtid'] = court.id
    api_address = "http://api.openweathermap.org/data/2.5/weather?appid=49a76676e913deb3805b87568bba047f&zip="+ court.zipcode
    json_data = requests.get(api_address).json()
    temperature = json_data['main']['temp']
    ftemperature = (temperature*9)/5 - 459.67
    reviews = Court_Review.objects.filter(court_reviewed = court).order_by('-created_at')
    # checkedinusers = User.objects.filter(checked_into = court)
    created_events = Event.objects.filter(court = id)

    context = {
        # "city": json_data['sys'][0]['name'],
        "ftemperature": ftemperature,
        "description": json_data['weather'][0]['description'],
        "icon": json_data['weather'][0]['icon'],
        "court": court,
        "reviews": reviews,
        # "checkedinusers": checkedinusers,
        "user": user,
        "created_events": created_events
    }

    return render(request, "hoopfinder/show_court.html", context)


def review_court(request):
    if request.method == 'POST':
        rating1 = request.POST['optrating']
        if rating1 == "1":
            rate = 1
        if rating1 == "2":
            rate = 2
        if rating1 == "3":
            rate = 3
        if rating1 == "4":
            rate = 4
        if rating1 == "5":
            rate = 5

        print("it went to review_court")
        courtreview = request.POST['courtreview']
        print(courtreview)
        court = Courts.objects.get(id = request.session['courtid'])
        user = User.objects.get(id = request.session['userid'])
        review = Court_Review.objects.create(court_review = courtreview, rating = rate, court_reviewed = court, court_review_by = user)
        id = request.session['courtid']
        return redirect('/courts/' + str(id))

def checkin(request):
    if request.method =='POST':
        id = request.session['userid']
        court = Courts.objects.get(id = request.session['courtid'])
        user = User.objects.get(id = request.session['userid'])
        # court.checked_in_user.add(user)
        # court.save()
        return redirect('/courts/' + str(id))

def add_user_review(request):
    if request.method == 'POST':
        
        reviewer = User.objects.get(id = request.session['userid'])
        reviewed_user = User.objects.get(id = request.POST['reviewed_user'])
        id = request.POST['reviewed_user']
        review = request.POST['review']
        print(id, "this is the id ***************")

        UserReviews.objects.create(review = review, reviewed_user = reviewed_user, reviewed_by = reviewer)

        return redirect("/user/"+id)

def delete_player_review(request, id, userid):
    if request.method == 'POST':
        review = UserReviews.objects.get(id = id)
        print("users review: " + review)
        review.delete()
    return redirect('/user/' + userid)
    # return redirect('/user/' + str(request.session['userid']))

def delete_review(request, id):
    if request.method == 'POST':
        review = Court_Review.objects.get(id = id)
        review.delete()
    return redirect('/courts/' + str(request.session['courtid']))

def delete_court(request, id):
    if request.method == 'POST':
        court = Courts.objects.get(id = id)
        court.delete()
    return redirect('/courts')

def add_event_process(request, court_id):
    if request.method == 'POST':
        user = User.objects.get(id = request.session['userid'])
        court = Courts.objects.get(id = court_id)
        name = request.POST['title']
        date = request.POST['date']
        time = request.POST['time']

        Event.objects.create(name = name, date = date, time = time, court = court, created_by = user)

        return redirect('/courts/'+ court_id)

def show_event(request, event_id):
    event = Event.objects.get(id = event_id)

    context = {
        'event': event,

    }

    return render(request, "hoopfinder/events.html", context)
