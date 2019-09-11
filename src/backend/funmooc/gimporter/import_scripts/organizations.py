# Import organizations from a Google Sheet
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from cms.api import create_page
from cms.models import Page
from richie.apps.courses.defaults import ORGANIZATIONS_PAGE
from richie.apps.courses.models import Organization
from richie.plugins.simple_picture.cms_plugins import SimplePicturePlugin
from richie.plugins.simple_text_ckeditor.cms_plugins import CKEditorPlugin

from .helpers import create_or_update_single_plugin, create_page_from_info, import_file


def import_organizations(sheet):
    """Import organizations from a Google Sheet's "organizations" tab."""

    language = settings.LANGUAGE_CODE
    root_reverse_id = ORGANIZATIONS_PAGE["reverse_id"]
    root_page = create_page_from_info(root_reverse_id)

    records = sheet.worksheet(root_reverse_id).get_all_records()

    for record in sorted(records, key=lambda r: -int(r["score"])):
        if int(record["is_obsolete"]):
            continue

        title = record["title"]
        reverse_id = record["reverse_id"].strip()
        slug = slugify(title)

        try:
            organization_page = Page.objects.get(
                reverse_id=reverse_id,
                node__parent__cms_pages=root_page,
                publisher_is_draft=True,
            )
        except Page.DoesNotExist:
            organization_page = create_page(
                title,
                ORGANIZATIONS_PAGE["template"],
                language,
                parent=root_page,
                reverse_id=reverse_id,
                slug=slug,
            )
        else:
            # Update slug and title that may have changed
            title_obj = organization_page.title_set.get(language=language)
            title_obj.slug = slug
            title_obj.title = title
            title_obj.save()

        organization, _created = Organization.objects.update_or_create(
            extended_object__reverse_id=reverse_id,
            extended_object__publisher_is_draft=True,
            defaults={"extended_object": organization_page},
        )
        organization.create_page_role()

        # Add a plugin for the description
        placeholder_description = organization_page.placeholders.get(slot="description")
        if record["description"]:
            create_or_update_single_plugin(
                placeholder_description,
                CKEditorPlugin,
                language=language,
                body=record["description"],
            )

        # Add a plugin for the logo
        placeholder_logo = organization_page.placeholders.get(slot="logo")
        if record["logo"]:
            create_or_update_single_plugin(
                placeholder_logo,
                SimplePicturePlugin,
                language=language,
                picture=import_file(record["logo"]),
            )

        # Add a plugin for the banner
        placeholder_banner = organization_page.placeholders.get(slot="banner")
        if record["banner"]:
            create_or_update_single_plugin(
                placeholder_banner,
                SimplePicturePlugin,
                language=language,
                picture=import_file(record["banner"]),
                attributes={"alt": str(_("organization banner"))},
            )

        if record["detail_page_enabled"]:
            organization_page.publish(language)

        yield organization_page
