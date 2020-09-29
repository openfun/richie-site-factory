"""
This module contains cache-related utilities functions.
"""

from django.conf import settings
from django.http.response import HttpResponseBase
from django.utils.cache import get_max_age, patch_response_headers

from cms.views import details as django_cms_details


def patch_response_cache_ttl(response: HttpResponseBase, max_ttl: int):
    """"
    Patch the http response headers Cache-Control and Expires to
    limit the cache timeout to the specified argument max_ttl (in seconds).
    """
    max_age = get_max_age(response)
    if max_age is not None and max_age > max_ttl:
        if response.has_header("Expires"):
            # Remove the Expires response Header because patch_response_headers()
            # adds it only if it isn't already setI
            del response["Expires"]
        patch_response_headers(response, cache_timeout=max_ttl)


def details(request, *args, **kwargs):
    """
    This method redefines cms.views.details view.
    It allows to set a maximum TTL for the browser cache response header.
    See the setting CMS_MAX_BROWSER_CACHE_TTL for more information.
    """

    response = django_cms_details(request, *args, **kwargs)
    # The response returned by cms.views.detail is either a TemplateResponse or a BaseHttpResponse
    # In the case of a TemplateResponse, the rendering can be delayed and the cache headers not
    # set yet. That's why we have to add a post rendering-callback to patch the response headers.
    if hasattr(response, "is_rendered") and not response.is_rendered:
        response.add_post_render_callback(
            lambda r: patch_response_cache_ttl(r, settings.CMS_MAX_BROWSER_CACHE_TTL)
        )
    else:
        patch_response_cache_ttl(response, settings.CMS_MAX_BROWSER_CACHE_TTL)
    return response
