import random
import string

from django.core.exceptions import FieldError


def random_string_generator(size=7, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size)).upper()


def id_generator(instance):
    model_name_field_id = random_string_generator()

    ModelClass = instance.__class__

    try:
        if ModelClass.objects.filter(fulfillment_id=model_name_field_id).exists():
            return id_generator(instance)
        else:
            return model_name_field_id
    except FieldError:
        pass

    try:
        if ModelClass.objects.filter(order_id=model_name_field_id).exists():
            return id_generator(instance)
        else:
            return model_name_field_id
    except FieldError:
        pass

    try:
        if ModelClass.objects.filter(product_id=model_name_field_id).exists():
            return id_generator(instance)
        else:
            return model_name_field_id
    except FieldError:
        pass