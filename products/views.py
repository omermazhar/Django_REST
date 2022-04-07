from html5lib import serialize
from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from api.mixins import (
    EditorPermissionMixin,
    )

from .models import Product
from .serializers import ProductSerializer


class ProductListCreateAPIView(EditorPermissionMixin,generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Product.objects.filter(public=True, user=user)

        return queryset

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(user=self.request.user, content=content)


product_list_create_view = ProductListCreateAPIView.as_view()


class ProductDetailAPIView(
    EditorPermissionMixin,
    generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'pk'


product_detail_view = ProductDetailAPIView.as_view()


class ProductUpdateAPIView(
    EditorPermissionMixin,
    generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title


product_update_view = ProductUpdateAPIView.as_view()


class ProductDestroyAPIView(
    EditorPermissionMixin,
    generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


product_destroy_view = ProductDestroyAPIView.as_view()


# CRUD operations using mixins
class ProductMixinView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print("in create")
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        print("in perfrom create")
        # serializer.save(user=self.request.user)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = "nothing in content"
        serializer.save(content=content)


product_mixin_view = ProductMixinView.as_view()

@api_view(['GET', 'POST'])
def product_alt_view(self, request, pk=None, *args, **kwargs):
    method = request.method

    if method == "GET":
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True).data
        return Response(data)

    if method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None
            if content is None:
                content = title
            serializer.save(content=content)
            return Response(serializer.data)
        return Response({"invalid": "not good data"}, status=400)
