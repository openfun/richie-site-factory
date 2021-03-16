"""
Template context_processors
"""
import json

from django.conf import settings
from django.db.models import Q
from django.utils.translation import get_language_from_request

from cms.models import Page
from richie.apps.courses.models import Organization


def site_metas(request):
    """
    Context processor to add all information required by frontend scripts.
    """

    page = request.current_page or None
    language = get_language_from_request(request, check_path=True)

    def get_organizations():
        """
        Return organization attached to the page and
        organizations linked to the current page via an organization plugin in any of the
        placeholders on the page
        """
        return list(
            Organization.objects.filter(
                Q(
                    extended_object__organization_plugins__cmsplugin_ptr__language=language,
                    extended_object__organization_plugins__cmsplugin_ptr__placeholder__page=page,
                )
                | Q(
                    extended_object__exact=page,
                ),
                extended_object__title_set__published=True,
            )
            .distinct()
            .values_list("code", flat=True)
        )

    def get_privacy_policy_uri():
        """
        Check if a privacy policy page is published in the request language
        then return its url.
        """
        try:
            page = Page.objects.get(
                publisher_is_draft=False,
                reverse_id="annex__privacy",
            )
            if page.is_published(language) is False:
                raise ValueError
        except (Page.DoesNotExist, ValueError):
            return None
        else:
            return page.get_public_url(language=language)

    context = {
        "PRIVACY_CONTEXT": json.dumps(
            {
                "tarteaucitron": {
                    "privacyUrl": get_privacy_policy_uri(),
                },
            }
        ),
        "MARKETING_CONTEXT": json.dumps(
            {
                "xiti": {
                    "level2": str(page.node.get_root().pk),
                    "organizations": get_organizations() if not page.is_home else [],
                    "site_id": settings.MARKETING_SITE_ID,
                }
                if getattr(settings, "MARKETING_SITE_ID", None)
                and page is not None
                and page.publisher_is_draft is False
                else {},
            }
        ),
    }

    return context
