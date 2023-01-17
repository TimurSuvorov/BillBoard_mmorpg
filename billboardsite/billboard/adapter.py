from allauth.account.adapter import DefaultAccountAdapter
from django.utils.crypto import get_random_string


class DefaultAccountAdapterCustom(DefaultAccountAdapter):

    def generate_emailconfirmation_key(self, email):
        super(DefaultAccountAdapterCustom, self).generate_emailconfirmation_key(email)
        key = get_random_string(6, allowed_chars='1234567890').lower()
        return key
