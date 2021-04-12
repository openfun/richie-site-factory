"""Views for the fun-mooc site."""
from django.db.models import Q
from django.http import HttpResponsePermanentRedirect

from cms.api import Page
from cms.constants import PUBLISHER_STATE_PENDING
from richie.apps.core.views.error import error_view_handler


def redirect_edx_resources(request, organization, course=None, session=None):
    """
    The richie site is hosted on the same domain as OpenEdX before.
    Redirect OpenEdX course/organization urls
    to the corresponding Richie course/organization urls.
    """

    def get_redirect_url(**kwargs):
        """Look for a published page matching the kwargs query filters."""
        try:
            page = Page.objects.get(
                ~Q(title_set__publisher_state=PUBLISHER_STATE_PENDING),
                publisher_is_draft=False,
                title_set__language=request.LANGUAGE_CODE,
                title_set__published=True,
                **kwargs
            )
        except Page.DoesNotExist:
            return

        return page.get_absolute_url(request.LANGUAGE_CODE)

    url = (
        course is not None
        and get_redirect_url(course__code__iexact=course)
        or get_redirect_url(organization__code__iexact=organization)
        or get_redirect_url(reverse_id="courses")
    )

    if url is None:
        return error_view_handler(request, "Page not found", 404)

    return HttpResponsePermanentRedirect(url)
