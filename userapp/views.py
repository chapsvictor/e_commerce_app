from .models import User
from .serializers import UserRegisterSerializer, UserDetailSerializer
from rest_framework import viewsets


class UserDetailViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class=UserDetailSerializer
    queryset= User.objects.all()



class UserRegistrationViewSet(viewsets.ModelViewSet):
    serializer_class=UserRegisterSerializer
    queryset=User.objects.all()
