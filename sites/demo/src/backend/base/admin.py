"""Admin overrides for the demo site."""

import cms.cache.page

from .cache import set_page_cache

# Django CMS disables page cache for authenticated users
# (See https://github.com/divio/django-cms/blob/3.7.4/cms/cache/page.py#L38)
#
# In our case, since most of our users will be authenticated and be served the
# same content, this is a problem. That's why we are monkey patching the
# function `cms.cache.page.set_page_cache`.
# All non-staff users will benefit from page cache.

cms.cache.page.set_page_cache = set_page_cache
