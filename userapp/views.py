from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserDetailSerializer, RegisterSerializer


class UserDetailPermission(BasePermission):

    message = 'You are only allowed to view your own details' 

    def has_object_permission(self, request, view, obj):       
        return obj.email == request.user.email


class UserDetailsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (UserDetailPermission, )
    serializer_class=UserDetailSerializer
    queryset= User.objects.all()


class RegistrationView(generics.GenericAPIView):
    
    permission_classes = (permissions.AllowAny,  )
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    