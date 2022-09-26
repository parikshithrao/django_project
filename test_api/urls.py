from django.urls import path
from .views import ArticleDetail, ArticleGenericView, ArticleList, article_detail, article_display
from test_api import views

urlpatterns = [
    path('article/', views.ArticleAPIView.as_view()),
    path('detail/<int:pk>', views.ArticleAPIDetail.as_view()),
    path('generic/article/', views.ArticleGenericView.as_view()),
    path('generic/detail/<int:pk>', views.ArticleDetail.as_view()),
    path('article_list/', views.ArticleList.as_view()),
    path('article_detail/<int:id>', views.ArticleDetails.as_view())
]

