from django.urls import path


from . import views

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article-list'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('update/<int:pk>/', views.ArticeUpdateView.as_view(), name = 'article-update'),
    path('create/', views.ArticleCreateView.as_view(), name = 'article-create'),
    path('<str:slug>/<int:pk>', views.ArticleRetrieveUpdateDestroyView.as_view(), name = 'article-RUD')
]
