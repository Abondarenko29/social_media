from django.core.exceptions import PermissionDenied


class UserIsOwnerMixin:
    def dispatch(self, request, *args, **kwargs):
        owner = self.get_object().owner
        if request.user != owner:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class UserIsAuthorMixin:
    def dispatch(self, request, *args, **kwargs):
        author = self.get_object().author
        if request.user != author:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
