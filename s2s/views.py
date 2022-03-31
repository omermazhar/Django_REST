from rest_framework import viewsets, serializers, filters
from rest_framework_api_key.permissions import HasAPIKey
from django.db import models
from django.apps import apps
from django_filters.rest_framework import DjangoFilterBackend


class ModelViewSet(viewsets.ModelViewSet):
    permission_classes = (HasAPIKey,)
    permission_classes = ()
    authentication_classes = ()
    lookup_field = "id"

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering = ("-id")

    @property
    def filterset_fields(self):
        app_label, model_name = self.kwargs["model"].split(".")

        model_cls = apps.get_model(app_label, model_name)
        if issubclass(model_cls, models.Model):
            fieldset = {field.name: ["exact"] for field in [field for field in model_cls._meta.get_fields() if field.get_internal_type() != "JSONField"]}
            return fieldset
        else:
            return {}

    @property
    def ordering_fields(self):
        app_label, model_name = self.kwargs["model"].split(".")

        model_cls = apps.get_model(app_label, model_name)
        if issubclass(model_cls, models.Model):
            ordering_fields = [field.name for field in model_cls._meta.get_fields()]
            return ordering_fields
        else:
            return []

    def get_queryset(self):
        app_label, model_name = self.kwargs["model"].split(".")

        model_cls = apps.get_model(app_label, model_name)
        if issubclass(model_cls, models.Model):
            return model_cls.objects.all()
        else:
            return []

    def model_create(self, validated_data):
        app_label, model_name = self.kwargs["model"].split(".")

        model_cls = apps.get_model(app_label, model_name)
        if issubclass(model_cls, models.Model):
            model_list = [model_cls(**item) for item in validated_data]
            return model_cls.objects.bulk_create(model_list)
        return []

    def get_serializer_class(self, *args, **kwargs):
        app_label, model_name = self.kwargs["model"].split(".")

        model_cls = apps.get_model(app_label, model_name)
        if issubclass(model_cls, models.Model):
            ListSerializer = type("ListSerializer", (serializers.ListSerializer,), {
                "create": self.model_create,
            })

            Serializer = type("ModelSerializer", (serializers.ModelSerializer,), {
                "Meta": type("Meta", (), {
                    "fields": "__all__",
                    "model": model_cls,
                    "list_serializer_class": ListSerializer,
                })
            })
            return Serializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        if self.action == "create":
            kwargs['many'] = isinstance(kwargs['data'], list)
        return serializer_class(*args, **kwargs)