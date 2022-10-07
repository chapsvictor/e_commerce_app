from userapp.models import User
from django.test import TestCase


class UserTestCase(TestCase):

    """
    Test user creation
    """
    def setUp(self):
        email = 'testemail@yahoo.com'
        username = 'testusername'
        first_name = 'testfirstname'
        address="testaddress"
        contact="0903249609"
        password='12345'
        User.objects._create_user(email=email, 
                                                username=username, 
                                                first_name=first_name, 
                                                address=address, 
                                                contact=contact, 
                                                password=password, 
                                                is_active=True, 
                                                is_staff=False, 
                                                is_superuser=False
        )



    def test_create_user(self):
        test_user= User.objects.get(username= 'testusername')

        self.assertEquals(test_user.first_name, 'testfirstname')
        self.assertEquals(test_user.email, 'testemail@yahoo.com')
        self.assertEquals(test_user.username, 'testusername')
        self.assertEquals(test_user.address, "testaddress")
        self.assertEquals(test_user.contact, "0903249609")
        self.assertNotEqual(test_user.password, '12345')
        self.assertTrue(test_user.is_active)
        self.assertFalse(test_user.is_staff)
        self.assertFalse(test_user.is_superuser)


class SuperUserTestCase(TestCase):

    """
    Test super_user creation
    """

    def setUp(self):
        email = 'supertestemail@yahoo.com'
        username = 'supertestemail'
        first_name = 'supertestfirstname'
        address="testaddress"
        contact="0903249609"
        password='12345'

        User.objects.create_superuser(email=email, 
                                    username=username, 
                                    first_name=first_name, 
                                    address=address, 
                                    contact=contact, 
                                    password = password
        )


    def test_create_superuser(self):

        test_super_user=User.objects.get(email='supertestemail@yahoo.com')
        
        
        self.assertEquals(test_super_user.first_name,'supertestfirstname' )
        self.assertEquals(test_super_user.email, 'supertestemail@yahoo.com')
        self.assertEquals(test_super_user.first_name, 'supertestfirstname')
        self.assertEquals(test_super_user.address, "testaddress")
        self.assertEquals(test_super_user.contact, "0903249609")
        self.assertTrue(test_super_user.is_active)
        self.assertTrue(test_super_user.is_staff)
        self.assertTrue(test_super_user.is_superuser)
