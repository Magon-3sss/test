from django.http import HttpResponseForbidden


class CanAccessViewMixin:
    def has_permission(self):
        return self.request.user.has_permission('can_access_view')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return HttpResponseForbidden()

        return super().dispatch(request, *args, **kwargs)
