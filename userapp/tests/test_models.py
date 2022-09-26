from userapp.models import User
import unittest



class UserTestCase(unittest.TestCase):

    """
    Test user creation
    """

    def test_create_user(self):
        email = 'testemail@yahoo.com'
        username = 'testemail'
        first_name = 'testfirstname'
        address="testaddress"
        contact="0903249609"
        password='12345'


        test_user = User.objects.create(email=email, username=username, first_name=first_name, address=address, contact=contact, password=password)

        self.assertTrue(test_user)
        self.assertEquals(test_user.first_name, 'testfirstname')
        self.assertEquals(test_user.password, '12345')
        self.assertEquals(test_user.email, 'testemail@yahoo.com')
        self.assertEquals(test_user.first_name, 'testfirstname')
        self.assertEquals(test_user.address, "testaddress")
        self.assertEquals(test_user.contact, "0903249609")
        self.assertTrue(test_user.is_active)
        self.assertFalse(test_user.is_staff)
        self.assertFalse(test_user.is_superuser)


        test_user.delete()
        
    


class SuperUserTestCase(unittest.TestCase):

    """
    Test super_user creation
    """

                
    def test_create_superuser(self):
        email = 'supertestemail@yahoo.com'
        username = 'supertestemail'
        first_name = 'supertestfirstname'
        address="testaddress"
        contact="0903249609"
        password='12345'

        test_super_user=User.objects.create_superuser(email=email, username=username, first_name=first_name, address=address, contact=contact, password = password)

    
        self.assertTrue(test_super_user)
        self.assertEquals(test_super_user.first_name,'supertestfirstname' )
        self.assertEquals(test_super_user.email, 'supertestemail@yahoo.com')
        self.assertEquals(test_super_user.first_name, 'supertestfirstname')
        self.assertEquals(test_super_user.address, "testaddress")
        self.assertEquals(test_super_user.contact, "0903249609")
        self.assertTrue(test_super_user.is_active)
        self.assertTrue(test_super_user.is_staff)
        self.assertTrue(test_super_user.is_superuser)

        test_super_user.delete()



if __name__ == '__main__':
    unittest.main()
