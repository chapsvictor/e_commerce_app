from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  UserDetailsViewSet, RegistrationView



app_name= 'userapp'


router=DefaultRouter()
router.register('users',  UserDetailsViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('registration/', RegistrationView.as_view(), name='register'),
   
]
