from django.urls import path

from . import views

urlpatterns =[
    # path('',views.put_names),
    path('',views.home),
    path('recommend/', views.recommendation_view, name='recommendation_view'),
    path('details/<str:movie_title>/', views.movie_detail, name='movie_detail'),
   
]