from django.shortcuts import render, redirect

from django.http import HttpResponse

# importing models for dealing with db
from .models import Room, Topic, Message, User, Article

# for implementing constructed forms
from .forms import RoomForm, ArticleForm

from django.db.models import Q # for searching -> Qlookup -> to add in and or statements in our search resource

# user model -> built-in
# from django.contrib.auth.models import User

# for flash messages
from django.contrib import messages

# for authentication
from django.contrib.auth import authenticate, login, logout

# importing this decorator to restrict pages from non-logged users
from django.contrib.auth.decorators import login_required

# importing user creation form 
# from django.contrib.auth.forms import UserCreationForm

from .forms import MyUserCreationForm

# user updation form
from .forms import UserForm

# Create your views here.

# rooms = [
#     {"id": 1, "name": "Let's Learn Python"},
#     {"id": 2, "name": "Design with me"},
#     {"id": 3, "name": "FrontEnd Developers"},

# ]

def loginPage(request): # dont use just login as its name as we have a built-in function which would clash
    page="login"

    if request.user.is_authenticated: # if user is logged he/she musn't be allowed
        return redirect('home')

    if request.method == "POST":
        email = request.POST.get('email').casefold() # having username all lowercase
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            # this one is taken as a default "message" variable in templates
            messages.error(request, "User doesn't exists")

        # user authentication
        user = authenticate(request,email=email, password=password) # if it doesnt match an error's thrown it gives a None

        if user is not None:
            login(request, user)
            return redirect('home')
        else: # if invalid username or password
            messages.error(request, "Ooopsy Password went wrong!!!")


    context = {"page": page}
    return render(request, 'base/login_register.html', context)



def logoutUser(request):
    # a normal get request

    # getting the user logged out
    logout(request) # deleting the token (session one's)

    return redirect('home')



def registerPage(request):
    # page="register"

    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST) # password and username and stuff
        
        if form.is_valid(): # if details fed were valid then process it
            user = form.save(commit=False) # not commiting it as some work has to be done
            user.username = user.username.casefold() # as mentioned above username is processed to all lower
            user.save() # after processing user's saved

            # now logging user in
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occurred during registration")

    # context={'page': page}
    context = {"form": form}

    return render(request, 'base/login_register.html', context)



def home(request):

    print(request.GET.get('q'))
    # inline if statement
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    # model manager # contains checks whether atleast letters specified are part of given attributes that the whole word | "i" stands for insensitive
    rooms = Article.objects.filter(
        Q(title__icontains=q) | # topic__name__icontains -> in topic search using attribute name
        Q(content__icontains=q)
        ) # saying search/filter from topic for the given value

    room_count = rooms.count() # count is  faster than len method

    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    )


    context = {"rooms": rooms,
                "room_count": room_count, "room_messages": room_messages}

    return render(request, 'base/home.html', context)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# LEGACY 
def room(request, pk):
    
    # model manager
    room = Room.objects.get(id=pk) # using pk as id to grab data
    room_messages = room.message_set.all().order_by('-created') # asking to give us the set of messages in table message(all lowercase here) _set.all() -> give everything related to this room

    participants = room.participants.all()
    
    if request.method == 'POST':
        message = Message.objects.create( # creating a new row / object in model Message

            user = request.user,
            room=room,
            body=request.POST.get('body'),

        )
        
        # adding a user to a room while he is dropping a comment
        room.participants.add(request.user) # .remove() is also there

        return redirect("room", pk=room.id)

    context = {"room": room, "room_messages": room_messages, "participants": participants}
    return render(request, 'base/room.html', context)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++|


def userProfile(request, pk):
    user = User.objects.get(id=pk) # getting the user specified
    rooms = user.article_set.all() # getting all articles that the user specified has made
    # room_message = user.message_set.all() # getting all messages that the user has made
    # topics = Topic.objects.all() # getting all topics that the user specified
    context = {'user': user, 'rooms': rooms}
    return render(request, 'base/profile.html', context)


# LEGACY
@login_required(login_url='login') # redirecting the user to login
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all() # getting all topics to give an option

    if request.method == "POST":
            topic_name = request.POST.get('topic')
            
            # if topic name exists created will be False else it will be True
            topic, created = Topic.objects.get_or_create(name=topic_name)
            
            # object topic is held in variable topic abv
            Room.objects.create(
                host=request.user,
                topic=topic,
                name=request.POST.get('name'),
                description=request.POST.get('description'),

            )

            # form = RoomForm(request.POST)
            # if form.is_valid():
            #     room = form.save(commit=False) # dont commit it now
            #     room.host = request.user # adding the host automatically when user is created
            #     room.save()# saves the model/row in database
            
            return redirect('home') # corresponds to the name value give at file path in urls

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)





# _________________________________

from .summarizer import summarize
from .mailings import pres_mail
@login_required(login_url='login')
def create_article(request):
    form = ArticleForm()

    if request.method == "POST":

        # object topic is held in variable topic abv
        Article.objects.create(
            author = request.user,
            title = request.POST.get('title'),
            content = summarize.summarize_it(request.POST.get('content')),
        )

        # all users
        users = User.objects.all()

        for user in users:
            pres_mail.send_email(user.email, "New Article HIT❗❗❗", F"Check out this article on '{request.POST.get('title')}' just a half a minute read 😊")

        return redirect('home') # corresponds to the name value give at file path in urls

    context = {'form': form}
    return render(request, 'base/article_form.html', context)

#________________________________________________




# ________________________________-
# LEGACY
@login_required(login_url='login') # redirecting the user to login
def updateRoom(request, pk):
    # model manager
    room = Room.objects.get(id=pk) 
    topics = Topic.objects.all() # getting all topics to give an option
    form = RoomForm(instance=room) # the room is fetched with pre-filled values of it

    if request.user != room.host: # if the user tryna edit update room is not the owner then thow this error
        return HttpResponse("Your aren't allowed here!!")


    if request.method == "POST":
        topic_name = request.POST.get('topic')
            
        # if topic name exists created will be False else it will be True
        topic, created = Topic.objects.get_or_create(name=topic_name)
        # form = RoomForm(request.POST, instance=room) # room value to be updated is given else a new room instance would be created
        # if form.is_valid():
        #     form.save()
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)


# LEGACY
@login_required(login_url='login') # redirecting the user to login
def deleteRoom(request, pk):
    # model manager
    room = Room.objects.get(id=pk)

    if request.user != room.host: # if the user tryna edit update room is not the owner then thow this error
        return HttpResponse("Your aren't allowed here!!")

    if request.method == "POST":
        room.delete() # deleteing the row grabbed
        return redirect('home')
    context = {'obj': room}
    return render(request, 'base/delete.html', context)


# LEGACY
@login_required(login_url='login') # redirecting the user to login
def deleteMessage(request, pk):
    # model manager
    message = Message.objects.get(id=pk)

    if request.user != message.user: # if the user tryna edit update room is not the owner then thow this error
        return HttpResponse("Your aren't allowed here!!")

    if request.method == "POST":
        message.delete() # deleteing the row grabbed
        return redirect('home')
    
    context = {'obj': message}
    return render(request, 'base/delete.html', context)



@login_required(login_url='login')
def updateUser(request):
    
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user) # request.FILES will send all files to our db for submission and process it while updation or submission maybe

        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    context =  {'form': form}

    return render(request,'base/update-user.html', context)


# LEGACY
def topicsPage(request):

    print(request.GET.get('q'))
    # inline if statement
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics': topics}
    return render(request, 'base/topics.html', context)



def activityPage(request):
    room_messages = Message.objects.all()
    context= {'room_messages': room_messages}
    return render(request, 'base/activity.html', context)


# _________________________________
from .chat_base import chat_test

# accepts a tuple (query/result, 1|0) --> 1-bot || 0-user
queries = [("Hey! Its Praana, your AI assistant here to resolve queries on Healthcare/Medical related issues/statements :)", 1)] # using a global list to store user queries

@login_required(login_url='login')
def home_bot(request):
    context = {}

    if request.method == 'GET':
        # if parameter got send it, else put return None which will be caught while processing

        print("HELLo")

        user_query = request.GET.get("user-query", None)

        if user_query:
            queries.append((user_query, 0)) # query posed by the user
            queries.append((chat_test.mainCall(query=user_query), 1)) # response from the bot

        context["user_query"] = queries# reversing it for a reverse-vertical scroll

    return render(request, 'base/chat.html', context)


# ______________________________________________
from .chat_base import chat_test
from .mailings import pres_mail

@login_required(login_url='login')
def prescription_generator(request):
    context = {"Emailed":False}

    if request.method == "POST":
        user = request.user

        symptoms = request.POST.get("symptoms")

        if symptoms:
            prescription = chat_test.generate_prescription(symptoms)
            
            pres_mail.send_prescription(user.name, symptoms, prescription, user.email)

            print(symptoms)

            context["Emailed"] = True

    return render(request, "base/prescription.html", context)
