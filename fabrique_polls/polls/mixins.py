from rest_framework import viewsets, permissions

from .permissions import IsAdminUserOrReadOnly


class PermissionMixin(viewsets.ModelViewSet):
    action_permissions = {'list': [permissions.AllowAny],
                          'create': [IsAdminUserOrReadOnly],
                          'destroy': [IsAdminUserOrReadOnly],
                          'retrieve': [permissions.AllowAny],
                          'update': [IsAdminUserOrReadOnly],
                          'partial_update': [IsAdminUserOrReadOnly]} # patch

    def get_permissions(self):
        return [permission() for permission in self.action_permissions[self.action]]