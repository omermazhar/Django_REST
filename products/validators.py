from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Product


def validate_title(value):
    if " " in value.lower():
        raise serializers.ValidationError(f"'{value}'" + " contains whitespaces")
    return value


unique_product_title = UniqueValidator(queryset=Product.objects.all(), lookup='iexact')