# Import blogposts from a Google Sheet
from django.conf import settings
from django.utils.text import slugify

from cms.api import create_page
from cms.models import Page
from filer.models import Folder
from richie.apps.courses.cms_plugins import CategoryPlugin
from richie.apps.courses.defaults import BLOGPOSTS_PAGE
from richie.apps.courses.models import BlogPost
from richie.plugins.plain_text.cms_plugins import PlainTextPlugin
from richie.plugins.simple_picture.cms_plugins import SimplePicturePlugin
from richie.plugins.simple_text_ckeditor.cms_plugins import CKEditorPlugin

from .helpers import (
    create_or_update_single_plugin,
    create_page_from_info,
    extract_and_replace_media,
    import_file,
    parse_datetime,
)


def import_blogposts(sheet):
    """Import blogposts from a Google Sheet's "blogposts" tab."""

    language = settings.LANGUAGE_CODE
    root_reverse_id = BLOGPOSTS_PAGE["reverse_id"]
    root_page = create_page_from_info(root_reverse_id)

    # Make sure a folder exists to store blog posts related media
    blogposts_folder, _created = Folder.objects.get_or_create(name=root_reverse_id)

    for record in sheet.worksheet(root_reverse_id).get_all_records():
        if not int(record["is_published"]) == 1:
            continue

        title = record["title"]
        reverse_id = "blogpost_{:d}".format(record["id"])
        slug = slugify(title)

        try:
            blogpost_page = Page.objects.get(
                reverse_id=reverse_id,
                node__parent__cms_pages=root_page,
                publisher_is_draft=True,
            )
        except Page.DoesNotExist:
            blogpost_page = create_page(
                title,
                BLOGPOSTS_PAGE["template"],
                language,
                parent=root_page,
                reverse_id=reverse_id,
                slug=slug,
            )
        else:
            # Update slug and title that may have changed
            title_obj = blogpost_page.title_set.get(language=language)
            title_obj.slug = slug
            title_obj.title = title
            title_obj.save()

        # Force creation date
        Page.objects.filter(id=blogpost_page.id).update(
            creation_date=parse_datetime(record["created_at"])
        )
        blogpost_page.refresh_from_db()

        BlogPost.objects.update_or_create(
            extended_object__reverse_id=reverse_id,
            extended_object__publisher_is_draft=True,
            defaults={"extended_object": blogpost_page},
        )

        # Add plugins for categories
        categories = record["categories"].strip()
        if categories:
            placeholder_categories = blogpost_page.placeholders.get(slot="categories")
            page_ids = Page.objects.filter(
                publisher_is_draft=True,
                reverse_id__in=[c for c in categories.split(",") if c],
            ).values_list("id", flat=True)

            for page_id in page_ids:
                create_or_update_single_plugin(
                    placeholder_categories,
                    CategoryPlugin,
                    language=language,
                    filter_params={"page_id": page_id},
                )
            # Delete any plugin on this placeholder that does not match our filter params anymore
            CategoryPlugin.model.objects.filter(
                placeholder=placeholder_categories
            ).exclude(page__in=page_ids).delete()

        # Add a plugin for the cover image
        if record["cover"]:
            placeholder_cover = blogpost_page.placeholders.get(slot="cover")
            create_or_update_single_plugin(
                placeholder_cover,
                SimplePicturePlugin,
                language=language,
                picture=import_file(record["cover"], folder=blogposts_folder),
            )

        # Add a plugin for the excerpt
        placeholder_excerpt = blogpost_page.placeholders.get(slot="excerpt")
        if record["excerpt"]:
            create_or_update_single_plugin(
                placeholder_excerpt,
                PlainTextPlugin,
                language=language,
                body=record["excerpt"],
            )

        # Add a plugin for the body
        placeholder_body = blogpost_page.placeholders.get(slot="body")
        if record["body"]:
            body = extract_and_replace_media(record["body"])

            create_or_update_single_plugin(
                placeholder_body, CKEditorPlugin, language=language, body=body
            )

        blogpost_page.publish(language)

        yield blogpost_page
