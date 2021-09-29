"""
Template context_processors
"""
import json

from django.utils.translation import get_language_from_request

from cms.models import Page


def site_metas(request):
    """
    Context processor to add all information required by frontend scripts.
    """

    language = get_language_from_request(request, check_path=True)

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
    }

    return context
