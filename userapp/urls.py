from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  UserDetailViewSet, UserRegistrationViewSet



app_name= 'userapp'


router=DefaultRouter()
router.register('user_detail',  UserDetailViewSet, basename='user_detail_view')
router.register('user_registration', UserRegistrationViewSet, basename='user_registration_view')

urlpatterns = [
    path('',include(router.urls)),
   
]