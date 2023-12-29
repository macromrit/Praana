from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),#passing dynamic value as we may have multiple rooms
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),

    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>/', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),

    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    
    # no need of user id as its gonna be the user logged in
    path('update-user/', views.updateUser, name="update-user"),
    
    # for all topics
    path('topics/', views.topicsPage, name="topics"),

    # for all topics
    path('activities/', views.activityPage, name="activity"),

    # create articles
    path('create-article/', views.create_article, name="create-article"),

    # chat bot
    path('chat-with-praana/', views.home_bot, name='chat-bot'),

    # precription
    path('precription-generator/', views.prescription_generator, name="prescription-generator")


]
