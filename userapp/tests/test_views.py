from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import force_authenticate
from ..models import * 
from ..serializers import *
from userapp.views import *


class UserDetailViewTest(APITestCase):
    """
    Test user detail view
    """
    @classmethod
    def setUp(cls):
        
        
        cls.user = User.objects.create_superuser(username='username2', email='email2@yahoo.com', password='12345')

   
    def test_list_read_all_users(self):
    
        response = self.client.get(reverse('userapp:user-list'))

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        
        self.assertIn(UserDetailSerializer(instance=self.user).data, response.data)
        
    def test_can_read_a_specific_user_detail(self):
        # force authenticate because user needs to be loggedin to view his detials
        self.client.force_authenticate(user=self.user)
        response=self.client.get(reverse('userapp:user-detail', args=[self.user.id]))
        
        self.assertEquals(status.HTTP_200_OK, response.status_code)


class RegistrationViewTest(APITestCase):
    """
    Test user Registration view
    """

    def test_can_register_new_user(self):
        register_url = reverse('userapp:register')
        test_user = {
                "username":'username3', 
                "email":'email22@yahoo.com', 
                'first_name':'myfristname',
                'password':'victor1996',
                'password2':'victor1996',
                'address':'testaddress',
                'contact':'09032849609'
                }

        response = self.client.post(register_url, test_user, format='json')
        print(response.data)

        created_user = User.objects.get(username=test_user['username'])
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEquals(response.data['email'], created_user.email)
        