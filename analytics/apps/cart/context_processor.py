from django.contrib.auth import get_user_model
from .models import Cart


User = get_user_model()

def cart_context(request):
    try:
        cart = Cart.objects.get(user=request.user)
        return {'cart': cart}

    # All possible exception:

    except Cart.DoesNotExist or User.DoesNotExist:
        return {'cart': None}

    except User.DoesNotExist:
        return {'cart': None}

    except TypeError:
        return {'cart': None}


"""
Then add this line to the settings.TEMPLATES.context_processors:
    'cart.context_processor.cart_context'
"""
