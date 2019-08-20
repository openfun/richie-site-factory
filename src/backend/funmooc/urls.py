"""
FUN-MOOC urls
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve

from cms.sitemaps import CMSSitemap
from richie.apps.search.urls import urlpatterns as search_urlpatterns

# For now, we use URLPathVersioning to be consistent with fonzie. Fonzie uses it
# because DRF OpenAPI only supports URLPathVersioning for now. See fonzie
# API_PREFIX config for more information.
API_PREFIX = r"v(?P<version>[0-9]+\.[0-9]+)"

admin.autodiscover()

urlpatterns = [
    url(r"^sitemap\.xml$", sitemap, {"sitemaps": {"cmspages": CMSSitemap}}),
    url(r"^api/{}/".format(API_PREFIX), include(search_urlpatterns)),
    url(r"^", include("filer.server.urls")),
]

urlpatterns += i18n_patterns(
    url(r"^admin/", admin.site.urls),  # noqa
    url(r"^login/", auth_views.LoginView.as_view(), name="login"),
    url(r"^logout/", auth_views.LogoutView.as_view(), name="logout"),
    url(r"^oauth/", include("social_django.urls", namespace="social")),
    url(r"^", include("cms.urls")),  # noqa
)

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = (
        [
            url(
                r"^media/(?P<path>.*)$",
                serve,
                {"document_root": settings.MEDIA_ROOT, "show_indexes": True},
            )
        ]
        + staticfiles_urlpatterns()
        + urlpatterns
    )
