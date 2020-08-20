"""Admin overrides for the fun-mooc site."""
from django.contrib import admin, auth
from django.contrib.auth.admin import UserAdmin
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

import cms.cache.page
from filer.admin import clipboardadmin
from filer.admin.clipboardadmin import ajax_upload as filer_ajax_upload
from filer.models.virtualitems import FolderRoot

from .cache import set_page_cache


class CustomUserAdmin(UserAdmin):
    """
    Override the user admin to customize its behavior.
    The original user admin is unregistered below in order to make place for this custom admin.
    """

    def get_readonly_fields(self, request, obj=None):
        """Make the superuser field readonly for staff users that are not superuser themselves."""
        extra_readonly_fields = (
            ("is_superuser",) if not request.user.is_superuser else ()
        )
        return self.readonly_fields + extra_readonly_fields


@csrf_exempt
def ajax_upload(request, folder_id=None):
    """Disallow unsorted uploads."""
    if folder_id is None:
        return JsonResponse({"error": _("Unsorted uploads are not allowed.")})

    return filer_ajax_upload(request, folder_id=folder_id)


clipboardadmin.ajax_upload = ajax_upload
FolderRoot.virtual_folders = lambda o: []

user_model = auth.get_user_model()
admin.site.unregister(user_model)
admin.site.register(user_model, CustomUserAdmin)

# Django CMS disables page cache for authenticated users
# (See https://github.com/divio/django-cms/blob/3.7.4/cms/cache/page.py#L38)
#
# In our case, since most of our users will be authenticated and be served the
# same content, this is a problem. That's why we are monkey patching the
# function `cms.cache.page.set_page_cache`.
# All non-staff users will benefit from page cache.

cms.cache.page.set_page_cache = set_page_cache
