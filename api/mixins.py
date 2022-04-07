from rest_framework import permissions

from .permissions import EditorPermission

class EditorPermissionMixin():
    permission_classes = [permissions.IsAdminUser, EditorPermission]

