# from django.http import JsonResponse # java script object notation -> format of how we can provide data

from rest_framework.decorators import api_view
from rest_framework.response import Response

from base.models import Room, Article

from .serializers import ArticleSerializer

# just returning data that users want from this api in JSON format
@api_view(['GET']) # list out methods allow to access this view
def getRoutes(request):
    routes = [
        "GET /api", # going to their home-page
        "GET /api/articles", # to get all rooms
        # "GET /api/rooms/:id", # to get a specific room
    ]

    return Response(routes) # safe means we can allow anthing to be turned to json data just than a python list

@api_view(['GET'])
def getArticles(request):
    # serialization -> its used to translate a datastructure/object to something that can be transmitted easily
    #                  then can be reconstructed

    # response can't convert python objects 
    # so we have to serialize it
    # i.e turn all the objects into json format
    print("its called")
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True) # converting object/objects to json format | many -> many objects if True else only one object
    return Response(serializer.data)


# if we wanna allow users open up a room in their website
# @api_view(['GET'])
# def getRoom(request, pk):
#     # serialization -> its used to translate a datastructure/object to something that can be transmitted easily
#     #                  then can be reconstructed


#     # response can't convert python objects 
#     # so we have to serialize it
#     # i.e turn all the objects into json format

#     room = Room.objects.get(id=pk)
#     serializer = RoomSerializer(room, many=False) # converting object/objects to json format | many -> many objects if True else only one object
#     return Response(serializer.data)