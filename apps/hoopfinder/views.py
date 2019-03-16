from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.http import JsonResponse
from django.views import View
import json, requests

# MAKE AN EDIT USER page
# MAKE SURE THE DATABASE IS ALL CONNECTED TO EACH OTHER
# MAKE SURE THE THEME IS ALL GOOD TO GO BY FRIDAY MORNING
class Papayas(View):
    def get(self, request):        
        return JsonResponse({'status': 'ok'})
    def post(self, request):        
        return JsonResponse({'status': 'ok'})

class PapayaDetails(View):
    def get(self, request, papaya_id):        
        return JsonResponse({'status': 'ok'})
    def put(self, request, papaya_id):        
        return JsonResponse({'status': 'ok'})
    def delete(self, request, papaya_id):        
        return JsonResponse({'status': 'ok'})

# -----------------------------------
#  RENDER LANDING PAGE
#------------------------------------
def index(request):
    return render(request, "hoopfinder/landing.html")
# -----------------------------------
#  RENDER NEW_LANDING PAGE
#------------------------------------
def home(request):
    if 'userid' not in request.session:
        request.session['userid'] = 0
    if 'courtid' not in request.session:
        request.session['courtid'] = 0
    return render(request, "hoopfinder/new_landing.html")
# -----------------------------------
#  RENDER HOME PAGE
#------------------------------------
def home_test(request):
    if 'userid' not in request.session:
        request.session['userid'] = 0
    if 'courtid' not in request.session:
        request.session['courtid'] = 0
    return render(request, "hoopfinder/landing1.html")

# -----------------------------------
#  RENDER MAP PAGE
#------------------------------------
def map(request):
    loggedInUser = User.objects.get(id=request.session['userid'])
    context= {
        'loggedInUser' : loggedInUser
    }
    return render(request, "hoopfinder/maps.html", context)

# -----------------------------------
#  RENDER USER_DASHBOARD PAGE
#------------------------------------
def userdashboard(request): 
    return render(request, "hoopfinder/userbootstrap.html")

#------------------------------------
# ---------- SHOW ALL COURTS ---------
#------------------------------------
def courts(request):
    all_courts = Courts.objects.all()
    loggedInUser = User.objects.get(id=request.session['userid'])
    context = {
        "all_courts": all_courts,
        "loggedInUser": loggedInUser,
    }
    return render(request, "hoopfinder/courts1.html", context)
#------------------------------------
# ----- SHOW REGISTRATION -----------
#------------------------------------
def registration(request):
    return render(request, "hoopfinder/registration.html")

#------------------------------------
# POST REQUEST FOR REGISTRATION 
#------------------------------------
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
            
            # change this to userdashboard done
            return redirect('/user/'+str(request.session['userid']))
#------------------------------------
# SHOW LOGIN PAGE 
#------------------------------------    
def login(request):
    return render(request, "hoopfinder/login.html")

#------------------------------------
# POST REQUEST FOR LOGIN 
#------------------------------------    
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
            # change this to user dashboard done
            print("youre logged in " + user1.first_name)
            return redirect('/user/'+str(user1.id))
# ------------------------------------
# LOG USER OUT AND CLEAR SESSION
#------------------------------------
def logout(request):
    request.session.clear()
    return redirect('/home')

# ------------------------------------
# SHOW NEW COURT PAGE 
#------------------------------------
def new_court(request):
    return render(request, "hoopfinder/new_court.html")
# ------------------------------------
# POST REQUEST TO CREATE NEW COURT
#------------------------------------
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
# -----------------------------------
#  RENDER PAGE TO SHOW ONE COURT
#------------------------------------
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
    loggedInUser = User.objects.get(id=request.session['userid'])


    context = {
        # "city": json_data['sys'][0]['name'],
        "ftemperature": ftemperature,
        "description": json_data['weather'][0]['description'],
        "icon": json_data['weather'][0]['icon'],
        "court": court,
        "reviews": reviews,
        "checkedinusers": checkedinusers,
        "user": user,
        "loggedInUser": loggedInUser
    }

    return render(request, "hoopfinder/show_court1.html", context)
# -----------------------------------
#  POST REQUEST TO CREATE NEW REVIEW
#------------------------------------
def review_court(request):
    if request.method == 'POST':
        rating1 = request.POST['optrating']
        rate = int(rating1)

        print("it went to review_court")
        courtreview = request.POST['courtreview']
        print(courtreview)
        court = Courts.objects.get(id = request.session['courtid'])
        user = User.objects.get(id = request.session['userid'])
        review = Court_Review.objects.create(court_review = courtreview, rating = rate, court_reviewed = court, court_review_by = user)
        id = request.session['userid']
        return redirect('/courts/' + str(request.session['courtid']))

# -----------------------------------
#  POST REQUEST TO CREATE USER REVIEW
#------------------------------------
def add_user_review(request):
    if request.method == 'POST':
        
        reviewer = User.objects.get(id = request.session['userid'])
        reviewed_user = User.objects.get(id = request.POST['reviewed_user'])
        id = request.POST['reviewed_user']
        review = request.POST['review']
        print(id, "this is the id ***************")

        UserReviews.objects.create(review = review, reviewed_user = reviewed_user, reviewed_by = reviewer)

        return redirect("/user/"+id)
# -----------------------------------
#  CHECK USER INTO COURT
#------------------------------------
def checkin(request):
    if request.method =='POST':
        id = request.session['userid']
        court = Courts.objects.get(id = request.session['courtid'])
        user = User.objects.get(id = request.session['userid'])
        # court.checked_in_user.add(user)
        # court.save()
        return redirect('/courts/' + str(id))

# Routes after cleanup ========================================================================================================

#-------------------
# Renders users page
#-------------------
def user_page(request, user_id):
    print("User id in session is: " + str(request.session['userid']))
    if request.session['userid'] == 0:
        return redirect('/home')
    else:
        loggedInUser = User.objects.get(id=request.session['userid'])
        user = User.objects.get(id = user_id)
        user_reviews = UserReviews.objects.filter(reviewed_user = User.objects.get(id = user_id)).order_by('-created_at')
        all_reviews = UserReviews.objects.order_by('-created_at')
        print(user_reviews, "***********************")
        context= {
            'user': user,
            'user_reviews': user_reviews,
            'loggedInUser' : loggedInUser,
            'all_reviews': all_reviews
        }
        return render(request, "hoopfinder/userbootstrap1.html", context)
# -----------------------------------
#  TEST PAGE FOR USER
#------------------------------------
def user_page_test(request, user_id):
    print("User id in session is: " + str(request.session['userid']))
    if request.session['userid'] == 0:
        return redirect('/home')
    else:
        loggedInUser = User.objects.get(id=request.session['userid'])
        user = User.objects.get(id = user_id)
        user_reviews = UserReviews.objects.filter(reviewed_user = User.objects.get(id = user_id)).order_by('-created_at')
        all_reviews = UserReviews.objects.order_by('-created_at')
        print(user_reviews, "rev: ***********************")
        context= {
            'user': user,
            'user_reviews': user_reviews,
            'loggedInUser' : loggedInUser,
            'all_reviews': all_reviews
        }
        return render(request, "hoopfinder/userbootstrap.html", context)
        
#-------------------
# Route to delete users reviews
#-------------------
def delete_player_review(request, id, userid):
    print("In post route to delete a users reviews")
    if request.method == 'GET':
        review = UserReviews.objects.get(id = id)
        print("users review to delete: ",  review)
        review.delete()
    return redirect('/user/' + userid)

#-------------------
# Renders page to show all users/hoopers
#-------------------
def userdashboard(request):
    loggedInUser = User.objects.get(id=request.session['userid'])
    all_users = User.objects.all()
    all_new_users = User.objects.order_by('-created_at')[:9]
    print(all_users, "***********************")
    context= {
        'loggedInUser' : loggedInUser,
        'all_users': all_users,
        'all_new_users': all_new_users
    }
    return render(request, "hoopfinder/usersNew.html", context)
#-------------------
# Renders page to show chat_room app
#-------------------
def chat_room(request, id):
    loggedInUser = User.objects.get(id=request.session['userid'])
    context= {
        'loggedInUser': loggedInUser,
    }
    return render(request, 'hoopfinder/messaging.html', context)

#-------------------
# AJAX call to get all reviews for users page
#-------------------

def ajaxReviews(request, user_id):
    print("User id in session is: " + str(request.session['userid']))
    if request.session['userid'] == 0:
        return redirect('/home')
    else:
        loggedInUser = User.objects.get(id=request.session['userid'])
        user = User.objects.get(id = user_id)
        user_reviews = UserReviews.objects.filter(reviewed_user = User.objects.get(id = user_id)).order_by('-created_at')
        all_reviews = UserReviews.objects.order_by('-created_at')
        print(user_reviews, "rev: ***********************")
        context= {
            'user': user,
            'user_reviews': user_reviews,
            'loggedInUser' : loggedInUser,
            'all_reviews': all_reviews
        }
        return render(request, 'hoopfinder/reviews.html', context)