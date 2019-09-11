# Import blogposts from a Google Sheet
import re
from functools import reduce

from django.conf import settings
from django.utils.text import slugify

from cms.api import create_page
from cms.models import Page
from filer.models import Folder
from richie.apps.courses.cms_plugins import CategoryPlugin
from richie.apps.courses.defaults import (
    BLOGPOSTS_PAGE,
    COURSES_PAGE,
    ORGANIZATIONS_PAGE,
)
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

    course_page_path = Page.objects.get(
        reverse_id=COURSES_PAGE["reverse_id"], publisher_is_draft=True
    ).get_path()

    # We need to replace old urls by new ones in the blog posts content:
    # - Get a mapping from organizations old slugs to new paths
    organizations_mapping = {}
    for record in sheet.worksheet(ORGANIZATIONS_PAGE["reverse_id"]).get_all_records():
        try:
            organizations_mapping[record["slug"].lower()] = Page.objects.get(
                reverse_id=record["reverse_id"], publisher_is_draft=True
            ).get_path()
        except Page.DoesNotExist:
            pass

    # - Get a mapping from courses old slugs to new paths
    courses_mapping = reduce(
        lambda acc, record: {
            **acc,
            str(record["reverse_id"]): Page.objects.get(
                reverse_id=record["reverse_id"], publisher_is_draft=True
            ).get_path(),
        },
        sheet.worksheet(COURSES_PAGE["reverse_id"]).get_all_records(),
        {},
    )

    # Get or create the root page for blogposts
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
            body = extract_and_replace_media(record["body"], folder=blogposts_folder)

            # All urls pointing to this site should be relative
            # In the content we found a lot of broken urls pointing to:
            # - fun-mooc.fr
            # - france-universite-numerique-mooc.fr (already broken on the old site)
            #
            # Many derived urls will be found e.g:
            # - https://fun-mooc.fr            to be replaced by "/"
            # - http://www.fun-mooc.fr/courses to be replaced by "/courses"
            # - fun-mooc.fr/courses/my-course  to be replaced by "/courses/my-course"
            def domain_sub(match):
                """Return the matched path between quotes if any, or "/" otherwise."""
                return '"{:s}"'.format(match.group(1)) if match.group(1) else '"/"'

            body = re.sub(
                (
                    r"""["|'] ?(?:http)?s?(?:\://)?(?:www\.|studio\.)?"""
                    r"""(?:france-universite-numerique-mooc|fun-mooc)\.fr([^"']*)["|']"""
                ),
                domain_sub,
                body,
            )

            # Search and replace universities urls
            pattern = r'/universities/{:s}/?"'
            organizations_urls = re.findall(pattern.format(r'([^> "/]*)'), body)
            for organization_url in organizations_urls:
                body = re.sub(
                    pattern.format(organization_url),
                    f'/{organizations_mapping[organization_url.lower()]:s}/"',
                    body,
                )

            # Search and replace courses urls
            for pattern, group, separator in (
                (r"/courses/course-v1:{:s}/about", '([^> "/]*)', "+"),
                (r"/courses/{:s}/about", '([^> "+]*)', "/"),
            ):
                courses_urls = re.findall(pattern.format(group), body)
                for course_url in courses_urls:
                    course_number = course_url.split(separator)[1].lower()
                    if course_number in courses_mapping:
                        replacement = f"/{courses_mapping[course_number]:s}/"
                    else:
                        replacement = f"/{course_page_path:s}/"
                    body = body.replace(pattern.format(course_url), replacement)

            create_or_update_single_plugin(
                placeholder_body, CKEditorPlugin, language=language, body=body
            )

        blogpost_page.publish(language)

        yield blogpost_page
