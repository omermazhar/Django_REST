from random import random
from unittest.util import _MAX_LENGTH
from numpy import source
from rest_framework import serializers
from rest_framework.reverse import reverse

from api.serializers import UserPublicSerializer

from .models import Product
from . import validators


class ProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
            view_name='product-detail',
            lookup_field='pk',
            read_only=True
    )
    title = serializers.CharField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):

    owner = UserPublicSerializer(source='user', read_only=True)
    title = serializers.CharField(validators=[validators.validate_title, validators.unique_product_title])
    body = serializers.CharField(source='content')
    assigned_product = serializers.CharField()
    class Meta:
        model = Product
        fields = [
            'owner',
            'pk',
            'title',
            'body',
            'price',
            'sale_price',
            'public',
            'path',
            'assigned_product',
            'endpoint',
        ]
    def get_my_user_data(self, obj):
        return {
            "username": obj.user.username
        }
    def get_edit_url(self, obj):
        request = self.context.get('request') # self.request
        if request is None:
            return None
        return reverse("product-edit", kwargs={"pk": obj.pk}, request=request)
    def get_assigned_product(self):
        Product_Items = ['Tesla', 'Iphone', 'private jet', 'Macbook']
        return random.choice(Product_Items)

