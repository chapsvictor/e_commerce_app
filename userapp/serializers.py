from allauth.account.adapter import get_adapter
from django.contrib.auth import get_user_model
from e_commerce import settings
from rest_framework import serializers
from userapp.models import User


User=get_user_model()

class UserDetailSerializer(serializers.ModelSerializer):
    '''
    user model w/o password
    '''
    
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'address','contact', 'signup_date')
        extra_kwargs = {'password': {'write_only': True}}


class RegisterSerializer(serializers.ModelSerializer):
    """A serializer for user profile objects."""

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['id',  'email', 'username','first_name', 'address', 'contact', 'password', 'password2', 'signup_date']
        extra_kwargs = {'password': {'write_only': True}}



    def validate_password(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                ("The passwords do not match")) 
        return data

    def create(self, validated_data):
        user=User(
            email=validated_data['email'],
            username=validated_data['username'], 
            first_name=validated_data['first_name'],
            address=validated_data['address'],
            contact=validated_data['contact']

        )
        
        password = validated_data['password']        
        user.set_password(validated_data['password'])
        user.save()
        return user
