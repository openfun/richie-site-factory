# Import persons from a Google Sheet
from django.conf import settings
from django.utils.text import slugify

from cms.api import create_page
from cms.models import Page
from richie.apps.courses.defaults import PERSONS_PAGE
from richie.apps.courses.models import Person
from richie.plugins.plain_text.cms_plugins import PlainTextPlugin
from richie.plugins.simple_picture.cms_plugins import SimplePicturePlugin
from richie.plugins.simple_text_ckeditor.cms_plugins import CKEditorPlugin

from .helpers import create_or_update_single_plugin, create_page_from_info, import_file


def import_persons(sheet):
    """Import persons from a Google Sheet's "persons" tab."""

    language = settings.LANGUAGE_CODE
    root_reverse_id = PERSONS_PAGE["reverse_id"]
    root_page = create_page_from_info(root_reverse_id)

    for record in sheet.worksheet(root_reverse_id).get_all_records():
        title = record["title"].strip()

        if not title:
            continue

        reverse_id = record["reverse_id"].strip()
        slug = slugify(title)
        try:
            person_page = Page.objects.get(
                reverse_id=reverse_id,
                node__parent__cms_pages=root_page,
                publisher_is_draft=True,
            )
        except Page.DoesNotExist:
            person_page = create_page(
                title,
                PERSONS_PAGE["template"],
                language,
                parent=root_page,
                reverse_id=reverse_id,
                slug=slug,
            )
        else:
            # Update slug and title that may have changed
            title_obj = person_page.title_set.get(language=language)
            title_obj.slug = slug
            title_obj.title = title
            title_obj.save()

        Person.objects.update_or_create(
            extended_object__reverse_id=reverse_id,
            extended_object__publisher_is_draft=True,
            defaults={"extended_object": person_page},
        )

        bio = None
        maincontent = None

        if record["bio"]:
            bio = record["bio"]
            maincontent = record["maincontent"]
        elif record["maincontent"]:
            if "." in record["maincontent"]:
                bio, maincontent = record["maincontent"].split(".", 1)
                bio += "."
            else:
                bio = record["maincontent"]

        if bio:
            # Add a plugin for the bio
            placeholder_bio = person_page.placeholders.get(slot="bio")
            create_or_update_single_plugin(
                placeholder_bio, PlainTextPlugin, language=language, body=bio
            )

        if maincontent:
            # Add a plugin for the main content
            placeholder_maincontent = person_page.placeholders.get(slot="maincontent")
            create_or_update_single_plugin(
                placeholder_maincontent,
                CKEditorPlugin,
                language=language,
                body=maincontent,
            )

        # Add a plugin for the portrait
        placeholder_portrait = person_page.placeholders.get(slot="portrait")
        if record["portrait"]:
            create_or_update_single_plugin(
                placeholder_portrait,
                SimplePicturePlugin,
                language=language,
                picture=import_file(record["portrait"]),
                attributes={"alt": ""},
            )

        person_page.publish(language)

        yield person_page
