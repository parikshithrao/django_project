from django.shortcuts import render
#from django.http import HttpResponse, JsonResponse
from .models import Article
from .serializers import ArticleSerializer
from rest_framework.parsers import JSONParser
# from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404

from rest_framework import mixins
from rest_framework import generics

#Generic based views

class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class ArticleDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


#Generic class based API views using mixins
class ArticleGenericView(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self,request,*args, **kwargs):
        return self.list(request)

    def post(self, request,*args, **kwargs):
        return self.create(request)

class ArticleDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


#class based API views
class ArticleAPIView(APIView):
    def get(self,request):
        articles = Article.objects.all() 
        serializer = ArticleSerializer(articles, many = True)
        return Response(serializer.data)

    def post(self,request):
        serializer = ArticleSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArticleAPIDetail(APIView):
    def get_article(self,pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise Http404

    def get(self,pk,request):
        article = self.get_article(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
         
    def put(self,request,pk):
        article = self.get_article(pk)
        serializer = ArticleSerializer(article, data = request.data)
        return Response(serializer.data, status = status.HTTP_204_NO_CONTENT )

    def delete(self,request,pk):
        article = self.get_article(pk)
        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)






# Create your views here.

# @csrf_exempt
@api_view(['GET', 'POST'])
def article_display(request):
    if request.method == "GET":
        articles = Article.objects.all() 
        serializer = ArticleSerializer(articles, many = True)
        return Response(serializer.data)

    elif request.method == "POST":
        #data = JSONParser().parse(request)
        serializer = ArticleSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status = 200)

    elif request.method == 'PUT':
        # data = JSONParser().parse(request)
        serializer = ArticleSerializer(article, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)