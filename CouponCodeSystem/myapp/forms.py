from django import forms
from .models import Coupon
from django.db import models
from django.forms import ModelForm


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = (
            'promo_code',
            'discount',
            'discounttype',
            'start_date',
            'end_date',
            'max_limit',
            'per_user_limit'
        )
