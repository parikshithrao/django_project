from django.urls import path
from .views import article_detail, article_display

urlpatterns = [
    path('article/', article_display),
    path('detail/<int:pk>', article_detail)
]