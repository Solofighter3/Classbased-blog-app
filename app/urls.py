
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include
from .views import index,createblog,updateview,deleteview,detailview,Yourblogs,feedbacks
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('',index.as_view(),name="index"),
    path('Yourblogs/',Yourblogs.as_view(),name="Yourblogs"),
    path('feedback/',feedbacks.as_view(),name="feedback"),
    path('addblog/',createblog.as_view(),name="addblog"),
    path('update/<int:pk>/',updateview.as_view(),name="update"),
    path('delete/<int:pk>/',deleteview.as_view(),name="delete"),
     path('detail/<int:pk>',login_required(detailview.as_view()),name="detail"),
]
