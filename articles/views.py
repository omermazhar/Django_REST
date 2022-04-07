from rest_framework import generics
from .models import Article
from .serializers import ArticleSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ArticleDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


# Create/update operation using APIView

class ArticleCreateView(APIView):
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


class ArticeUpdateView(APIView):

    def patch(self, request, pk=None, *args, **kwargs):
        instance = Article.objects.get(id=pk)
        serializer = ArticleSerializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# delete,update and create, using RetriveUpdateDestryAPIView

class ArticleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
