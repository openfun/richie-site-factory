"""Admin overrides for the fun-mooc site."""
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from filer.admin import clipboardadmin
from filer.admin.clipboardadmin import ajax_upload as filer_ajax_upload
from filer.models.virtualitems import FolderRoot


@csrf_exempt
def ajax_upload(request, folder_id=None):
    """Disallow unsorted uploads."""
    if folder_id is None:
        return JsonResponse({"error": _("Unsorted uploads are not allowed.")})

    return filer_ajax_upload(request, folder_id=folder_id)


clipboardadmin.ajax_upload = ajax_upload
FolderRoot.virtual_folders = lambda o: []
