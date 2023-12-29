from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User, Article

# importing built-in user model
# from django.contrib.auth.models import User

class MyUserCreationForm(UserCreationForm): # since the User model has beem customized we have to have a seperate form structure for user registration hence this one comes handy
    class Meta:
        model = User
        fields = ['name', 'email', 'username', 'password1', 'password2']


class RoomForm(ModelForm):
    class Meta: # metadata -> information that explains data
        model = Room
        fields  = "__all__" # represent all fields | to hide values use a list with attributes ['name', 'body', ...]
        exclude = ["host", "participants"] # excluding un-necessary fields


class UserForm(ModelForm): 
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']
        # fields = "__all__"


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']