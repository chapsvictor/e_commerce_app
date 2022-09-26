import functools
from django.contrib import messages

def authenticate_user(viwe_func):

    """
    this decorator is to validate that the user is the owner of the product or order
    """
