"""
Based on django documents, we must use AUTH_USER_MODEL when using 'user model' as foreign key or in signals but not
get_user_model method:
https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#django.contrib.auth.get_user_model
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings                    # WE SHOULD USE THIS COMMAND INSTEAD OF get_user_model
# from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from rest_framework.authtoken.models import Token

import decimal
import re


# @receiver(pre_save, sender=get_user_model())  <==> THIS IS WRONG! USE BELOW COMMAND INSTEAD:
@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def validate_user_discount_percent(sender, instance, **kwargs):
    """Count user account discount"""
    if instance.discount_percent > 100:
        raise ValidationError(_('discount percent could not be more than 100'))

    elif instance.discount_percent < 0:
        raise ValidationError(_('discount percent could not be less than 0'))


@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def count_user_score_and_profile_discount(sender, instance, **kwargs):
    """Count user account score"""
    def score_count_helper(instance_score, discount_multiplier):
        """Helper function for DRY"""
        instance.discount_value += decimal.Decimal(10000 * discount_multiplier)
        instance.score_lifetime += instance_score
        instance.score = 0
    score = instance.score
    if 500 <= score <= 1000:
        score_count_helper(score, 1)
    elif 1000 < score <= 1500:
        score_count_helper(score, 2)
    elif instance.score > 1500:
        score_count_helper(score, 3)


@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def fill_slug_field(sender, instance, **kwargs):
    """Fill slug field for user"""
    if not instance.slug:
        instance.slug = slugify(instance.username)


# This signal will used for 'DRF based authentication':
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """Create Authentication token for newly created user"""
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def fill_phone_email_on_username(sender, instance=None, created=False, **kwargs):
    """If username is based on phone or email, fill another field accordingly"""
    if created:
        regex_email = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        regex_phone =  re.compile(r'09[0-3][0-9]-?[0-9]{3}-?[0-9]{4}')
        if re.fullmatch(regex_email, instance.username):
            instance.email = instance.username
            instance.save()
        elif re.fullmatch(regex_phone, instance.username):
            instance.phone = instance.username
            instance.save()
