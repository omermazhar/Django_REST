from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.serializers import ProductSerializer

@api_view(['POST'])
def api_home(request, *args, **kwargs):

    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        instance = serializer.save()
        return Response(serializer.data)

    return Response({"invalid": "bad data"}, status=400)
