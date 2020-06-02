# Import categories from a Google Sheet
from django.conf import settings
from django.utils.text import slugify

from cms.api import create_page
from cms.models import Page
from richie.apps.courses.defaults import CATEGORIES_PAGE
from richie.apps.courses.models import Category

from .helpers import create_page_from_info


def import_categories(sheet):
    """Import categories from a Google Sheet's "categories" tab."""

    language = settings.LANGUAGE_CODE
    root_reverse_id = CATEGORIES_PAGE["reverse_id"]
    category_root_page = create_page_from_info(root_reverse_id)

    for record in sheet.worksheet(root_reverse_id).get_all_records():
        title = record["title"]
        reverse_id = record["reverse_id"]
        slug = slugify(title)

        if record["parent"]:
            parent_page = Page.objects.get(
                reverse_id=record["parent"], publisher_is_draft=True
            )
        else:
            parent_page = category_root_page

        try:
            category_page = Page.objects.get(
                reverse_id=reverse_id,
                node__parent__cms_pages=parent_page,
                publisher_is_draft=True,
            )
        except Page.DoesNotExist:
            category_page = create_page(
                title,
                CATEGORIES_PAGE["template"],
                language,
                parent=parent_page,
                reverse_id=reverse_id,
                slug=slug,
            )
        else:
            # Update slug and title that may have changed
            title_obj = category_page.title_set.get(language=language)
            title_obj.slug = slug
            title_obj.title = title
            title_obj.save()

        Category.objects.update_or_create(
            extended_object__reverse_id=reverse_id,
            extended_object__publisher_is_draft=True,
            defaults={"extended_object": category_page},
        )

        category_page.publish(language)

        yield category_page
