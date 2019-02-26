from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import json
import requests

# Create your views here.

# MAKE AN EDIT USER page
# MAKE SURE THE DATABASE IS ALL CONNECTED TO EACH OTHER
# MAKE SURE THE THEME IS ALL GOOD TO GO BY FRIDAY MORNING

def index(request):
    return render(request, "hoopfinder/landing.html")

def home(request):
    if 'userid' not in request.session:
        request.session['userid'] = 0
    if 'courtid' not in request.session:
        request.session['courtid'] = 0
    return render(request, "hoopfinder/new_landing.html")

def map(request):
    return render(request, "hoopfinder/maps.html")
    
def userdashboard(request): 
    
    return render(request, "hoopfinder/userbootstrap.html")

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
            #BCRYPT
            pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            #create an account and push it to the database
            user2 = User.objects.create(first_name = request.POST['fname'], 
                                        last_name = request.POST['lname'], 
                                        email = request.POST['email'], 
                                        password = pw)
            request.session['userid'] = user2.id
            
            # change this to userdashboard
            return redirect('/user/'+str(request.session['userid']))

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
    court = Courts.objects.get(id = id)
    user = User.objects.get(id = request.session['userid'])
    request.session['courtid'] = court.id
    api_address = "http://api.openweathermap.org/data/2.5/weather?appid=49a76676e913deb3805b87568bba047f&zip="+ court.zipcode
    json_data = requests.get(api_address).json()
    temperature = json_data['main']['temp']
    ftemperature = (temperature*9)/5 - 459.67
    reviews = Court_Review.objects.filter(court_reviewed = court)
    checkedinusers = User.objects.filter(checked_into = court)

    context = {
        # "city": json_data['sys'][0]['name'],
        "ftemperature": ftemperature,
        "description": json_data['weather'][0]['description'],
        "icon": json_data['weather'][0]['icon'],
        "court": court,
        "reviews": reviews,
        "checkedinusers": checkedinusers,
        "user": user,
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
        id = request.session['userid']
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

def checkin(request):
    if request.method =='POST':
        id = request.session['userid']
        court = Courts.objects.get(id = request.session['courtid'])
        user = User.objects.get(id = request.session['userid'])
        # court.checked_in_user.add(user)
        # court.save()
        return redirect('/courts/' + str(id))

# Routes after cleanup

#-------------------
# Renders users page
#-------------------
def user_page(request, user_id):
    print("User id in session is: " + str(request.session['userid']))
    if request.session['userid'] == 0:
        return redirect('/home')
    else:
        user = User.objects.get(id = user_id)
        user_reviews = UserReviews.objects.filter(reviewed_user = User.objects.get(id = user_id)).order_by('-created_at')
        
        print(user, "***********************")
        context= {
            'user': user,
            'user_reviews': user_reviews,
        }
        return render(request, "hoopfinder/userbootstrap.html", context)
#-------------------
# Post route to delete users reviews
#-------------------
def delete_player_review(request, id, userid):
    print("In post route to delete a users reviews")
    if request.method == 'GET':
        review = UserReviews.objects.get(id = id)
        print("users review: ",  review)
        review.delete()
    return redirect('/user/' + userid)