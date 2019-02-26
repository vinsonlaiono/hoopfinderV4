from django.db import models
# from django.core.validators import RegexValidator
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # First name validates length
        if len(postData['fname']) < 2:
            errors["firstname"] = "First name must be at least 2 characters"
            print(errors["firstname"])
        # Last name validates length
        if len(postData['lname']) < 2:
            errors["lastname"] = "Last name must be at least 2 characters"
            print(errors["lastname"])
        # Email validates length
        if len(postData['email']) < 1:
            errors["email"] = "Email cannot be empty"
            print(errors["email"])
        email_check  = User.objects.filter(email = postData['email'])
        # Email validate if email exits
        if email_check:
            errors["email_check"] = "Email already exits"
            print(errors["email_check"])
        # Email validates valid email
        elif not EMAIL_REGEX.match(postData['email']):
            errors['valid_email'] = "Please enter a valid email"
            print(errors['valid_email'])
        # Password check length of password
        if len(postData['password']) < 8:
            errors["password"] = "Password must contain at least 9 characters"
            print(errors["password"])
        # Password check matching password
        if postData['password'] != postData['confpassword']: 
            errors['confpassword'] = "Passwords do not match"
        return errors 

    def login_validator(self, postData):
        errors = {}
        email = postData['email']
        users = User.objects.filter(email=email)
        if len(users) == 0:
            errors['failed'] = "failed to login"
            print(errors['failed'])
        else:
            user = users[0]
            print(user.password)
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                print("password match")
            else:
                print('--------faild to login password does not match')
                errors['login'] = "Failed to login"
        return errors 

# build a validator for adding new courts

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    # users player information
    position = models.CharField(max_length=255, default=" ")
    age = models.CharField(max_length=255, default=" ")
    feet = models.CharField(max_length=255, default=" ")
    inches = models.CharField(max_length=255, default=" ")
    city = models.CharField(max_length=255, default=" ")
    state = models.CharField(max_length=255, default=" ")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Courts(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=75)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=5)
    imagelink = models.CharField(max_length=100)
    checked_in_user = models.ForeignKey(User, related_name="checked_into")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Court_Review(models.Model):
    court_review = models.TextField()
    rating = models.IntegerField()
    court_reviewed = models.ForeignKey(Courts, related_name="court_reviews")
    court_review_by = models.ForeignKey(User, related_name="reviewed_courts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserReviews(models.Model):
    review = models.TextField()
    reviewed_user = models.ForeignKey(User, related_name="personal_reviews")
    reviewed_by = models.ForeignKey(User, related_name="user_reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
