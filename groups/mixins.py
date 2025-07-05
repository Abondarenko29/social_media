from django.core.exceptions import PermissionDenied


class UserIsOwnerMixin:
    def dispath(self, request, *args, **kwargs):
        owner = self.get_object().owner
        if request.user != owner:
            raise PermissionDenied
        return super().dispath(request, *args, **kwargs)
