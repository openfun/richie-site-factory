"""
This module contains cache-related utilities functions.
"""

from datetime import timedelta

from django.utils.cache import (
    add_never_cache_headers,
    patch_response_headers,
    patch_vary_headers,
)
from django.utils.timezone import now

from cms.cache import _get_cache_version, _set_cache_version
from cms.cache.page import _page_cache_key
from cms.constants import EXPIRE_NOW, MAX_EXPIRATION_TTL
from cms.toolbar.utils import get_toolbar_from_request
from cms.utils.conf import get_cms_setting


def set_page_cache(response):
    """
    This method redefines cms.cache.page.set_page_cache to allow
    Django CMS page cache for non-staff logged-in users
    """

    from django.core.cache import cache

    request = response._request
    toolbar = get_toolbar_from_request(request)
    is_staff = request.user.is_staff

    if is_staff or toolbar._cache_disabled or not get_cms_setting("PAGE_CACHE"):
        add_never_cache_headers(response)
        return response

    # This *must* be TZ-aware
    timestamp = now()

    placeholders = toolbar.content_renderer.get_rendered_placeholders()
    # Checks if there's a plugin using the legacy "cache = False"
    placeholder_ttl_list = []
    vary_cache_on_set = set()
    for ph in placeholders:
        # get_cache_expiration() always returns:
        #     EXPIRE_NOW <= int <= MAX_EXPIRATION_IN_SECONDS
        ttl = ph.get_cache_expiration(request, timestamp)
        vary_cache_on = ph.get_vary_cache_on(request)

        placeholder_ttl_list.append(ttl)
        if ttl and vary_cache_on:
            # We're only interested in vary headers if they come from
            # a cache-able placeholder.
            vary_cache_on_set |= set(vary_cache_on)

    if EXPIRE_NOW not in placeholder_ttl_list:
        if placeholder_ttl_list:
            min_placeholder_ttl = min(x for x in placeholder_ttl_list)
        else:
            # Should only happen when there are no placeholders at all
            min_placeholder_ttl = MAX_EXPIRATION_TTL
        ttl = min(get_cms_setting("CACHE_DURATIONS")["content"], min_placeholder_ttl)

        if ttl > 0:
            # Adds expiration, etc. to headers
            patch_response_headers(response, cache_timeout=ttl)
            patch_vary_headers(response, sorted(vary_cache_on_set))

            version = _get_cache_version()
            # We also store the absolute expiration timestamp to avoid
            # recomputing it on cache-reads.
            expires_datetime = timestamp + timedelta(seconds=ttl)
            cache.set(
                _page_cache_key(request),
                (response.content, response._headers, expires_datetime,),
                ttl,
                version=version,
            )
            # See note in invalidate_cms_page_cache()
            _set_cache_version(version)
    return response
