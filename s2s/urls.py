from django.urls import path, include
from s2s.views import ModelViewSet

model_list = ModelViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
model_details = ModelViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path("<str:model>/", model_list, name="s2s_model_list"),
    path("<str:model>/<str:id>", model_details , name="s2s_model_details"),
]