import six

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import get_random_string

from InvestmentFund.models import Services

def HashCode(length):
    xChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    xCode = get_random_string(length=length, allowed_chars=xChars)
    while Services.objects.filter(sCode=xCode).exists():
        xCode = get_random_string(length=length, allowed_chars=xChars)
    return xCode

class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.is_active))


gToken = TokenGenerator()