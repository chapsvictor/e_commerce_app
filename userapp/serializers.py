from e_commerce import settings
from rest_framework import serializers
from userapp.models import User
from django.contrib.auth import get_user_model

User=get_user_model()

class UserDetailSerializer(serializers.ModelSerializer):
    '''
    user model w/o password
    '''

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'address', 'contact')
        read_only_fields = ('email', )





class UserRegisterSerializer(serializers.ModelSerializer):
    """A serializer for user profile objects."""

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['id',  'email', 'username','first_name', 'address', 'contact', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}





    def create(self, validated_data):
        user=User(
            email=validated_data['email'],
            username=validated_data['username'], 
            first_name=validated_data['first_name'],
            address=validated_data['address'],
            contact=validated_data['contact']
        )
        
        password =validated_data['password']
        password2 =validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'passwords must match.'})
        user.set_password(validated_data['password'])
        user.save()
        return user

    # def save(self):
    #     user=User(
    #         email=self.validated_data['email'],
    #         username=self.validated_data['username'], 
    #         first_name=self.validated_data['first_name'],
    #         address=self.validated_data['address'],
    #         contact=self.validated_data['contact'],

    #     )
        
    #     password = self.validated_data['password']
    #     password2 = self.validated_data['password2']

    #     if password != password2:
    #         raise serializers.ValidationError({'password': 'passwords must match.'})
    #     user.set_password(self.validated_data['password2'])
    #     user.save()
    #     return user
