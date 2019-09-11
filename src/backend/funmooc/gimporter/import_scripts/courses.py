# Import courses from a Google Sheet
from django.conf import settings
from django.utils.text import slugify

import markdown
from cms.api import create_page
from cms.models import Page
from djangocms_video.cms_plugins import VideoPlayerPlugin
from filer.models import Folder
from richie.apps.courses.cms_plugins import (
    CategoryPlugin,
    LicencePlugin,
    OrganizationPlugin,
    PersonPlugin,
)
from richie.apps.courses.defaults import COURSERUNS_PAGE, COURSES_PAGE
from richie.apps.courses.models import Course, CourseRun, Licence
from richie.plugins.plain_text.cms_plugins import PlainTextPlugin
from richie.plugins.simple_picture.cms_plugins import SimplePicturePlugin
from richie.plugins.simple_text_ckeditor.cms_plugins import CKEditorPlugin

from .helpers import (
    create_or_update_single_plugin,
    create_page_from_info,
    import_file,
    parse_date,
)


def import_courses(sheet):
    """Import courses from a Google Sheet's "courses" tab."""

    language = settings.LANGUAGE_CODE
    root_reverse_id = COURSES_PAGE["reverse_id"]
    root_page = create_page_from_info(root_reverse_id)

    # Start by importing licences

    # Make sure a folder exists to store licence related media
    licences_folder, _created = Folder.objects.get_or_create(name="Licences")

    licences = {}
    for licence_record in sheet.worksheet("licences").get_all_records():
        licences[
            licence_record["reverse_id"]
        ], _created = Licence.objects.update_or_create(
            url=licence_record["url"],
            defaults={
                "name": licence_record["name"],
                "logo": import_file(licence_record["logo"], folder=licences_folder),
                "content": licence_record["content"],
            },
        )

    for record in sheet.worksheet(root_reverse_id).get_all_records():
        title = record["title"].strip()

        if not title:
            continue

        reverse_id = str(record["reverse_id"])
        slug = slugify(title)

        try:
            course_page = Page.objects.get(
                reverse_id=reverse_id,
                node__parent__cms_pages=root_page,
                publisher_is_draft=True,
            )
        except Page.DoesNotExist:
            course_page = create_page(
                title,
                COURSES_PAGE["template"],
                language,
                parent=root_page,
                reverse_id=reverse_id,
                slug=slug,
            )
        else:
            # Update slug and title that may have changed
            if title:
                title_obj = course_page.title_set.get(language=language)
                title_obj.slug = slug
                title_obj.title = title
                title_obj.save()

        course, _created = Course.objects.update_or_create(
            extended_object__reverse_id=reverse_id,
            extended_object__publisher_is_draft=True,
            defaults={"extended_object": course_page},
        )
        role = course.create_page_role()

        # field the effort field
        effort = record["effort"].strip()
        if effort:
            duration, unit = effort.split(" ")
            effort, reference = unit.split("/")
            course.effort = int(duration), effort, reference

        # Add a plugin for the description
        if record["description"]:
            placeholder_description = course_page.placeholders.get(
                slot="course_description"
            )
            create_or_update_single_plugin(
                placeholder_description,
                PlainTextPlugin,
                language=language,
                body=record["description"],
            )

        # Add a plugin for the format
        if record["format"]:
            placeholder_format = course_page.placeholders.get(slot="course_format")
            create_or_update_single_plugin(
                placeholder_format,
                PlainTextPlugin,
                language=language,
                body=record["format"],
            )

        # Add a plugin for the prerequisites
        if record["prerequisites"]:
            placeholder_prerequisites = course_page.placeholders.get(
                slot="course_prerequisites"
            )
            create_or_update_single_plugin(
                placeholder_prerequisites,
                PlainTextPlugin,
                language=language,
                body=record["prerequisites"],
            )

        # Add a plugin for the plan
        if record["plan"]:
            placeholder_plan = course_page.placeholders.get(slot="course_plan")
            create_or_update_single_plugin(
                placeholder_plan,
                CKEditorPlugin,
                language=language,
                body=markdown.markdown(record["plan"]),
            )

        # Add a plugin for the assessment
        if record["assessment"]:
            placeholder_assessment = course_page.placeholders.get(
                slot="course_assessment"
            )
            create_or_update_single_plugin(
                placeholder_assessment,
                PlainTextPlugin,
                language=language,
                body=record["assessment"],
            )

        # Add a plugin for the cover image
        if record["cover"]:
            placeholder_cover = course_page.placeholders.get(slot="course_cover")
            create_or_update_single_plugin(
                placeholder_cover,
                SimplePicturePlugin,
                language=language,
                picture=import_file(record["cover"], folder=role.folder),
            )

        # Add plugins for categories
        categories = record["categories"].strip()
        if categories:
            placeholder_categories = course_page.placeholders.get(
                slot="course_categories"
            )
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

        # Add plugins for organizations
        organizations = record["organizations"].strip()
        if organizations:
            placeholder_organizations = course_page.placeholders.get(
                slot="course_organizations"
            )
            organization_reverse_ids = [o for o in organizations.split(",") if o]
            organization_pages = Page.objects.filter(
                publisher_is_draft=True, reverse_id__in=organization_reverse_ids
            )

            if len(organization_pages) != len(organization_reverse_ids):
                raise ValueError(
                    f"Some organizations for course {reverse_id:s} could not be found."
                )

            for organization_page in organization_pages:
                create_or_update_single_plugin(
                    placeholder_organizations,
                    OrganizationPlugin,
                    language=language,
                    filter_params={"page_id": organization_page.id},
                )

                # Give permissions to this course
                course.create_permissions_for_organization(
                    organization_page.organization
                )

            # Delete any plugin on this placeholder that does not match our filter params anymore
            OrganizationPlugin.model.objects.filter(
                placeholder=placeholder_organizations
            ).exclude(page__in=organization_pages).delete()

        # Add a plugin for the teaser
        if record["teaser"]:
            placeholder_teaser = course_page.placeholders.get(slot="course_teaser")
            create_or_update_single_plugin(
                placeholder_teaser,
                VideoPlayerPlugin,
                language=language,
                embed_link=record["teaser"],
            )

        # Add the course team
        team = record["team"].strip()
        if team:
            placeholder_team = course_page.placeholders.get(slot="course_team")
            team_reverse_ids = [p.strip() for p in team.split(",") if p]
            page_ids = Page.objects.filter(
                publisher_is_draft=True, reverse_id__in=team_reverse_ids
            ).values_list("id", flat=True)

            if len(page_ids) != len(team_reverse_ids):
                raise ValueError(
                    "Some persons in the team for course {reverse_id:s} could not be found."
                )

            for page_id in page_ids:
                create_or_update_single_plugin(
                    placeholder_team,
                    PersonPlugin,
                    language=language,
                    filter_params={"page_id": page_id},
                )
            # Delete any plugin on this placeholder that does not match our filter params anymore
            PersonPlugin.model.objects.filter(placeholder=placeholder_team).exclude(
                page__in=page_ids
            ).delete()

        # Add a plugin for the course content license
        if record["licence_content"]:
            placeholder_licence_content = course_page.placeholders.get(
                slot="course_license_content"
            )
            create_or_update_single_plugin(
                placeholder_licence_content,
                LicencePlugin,
                language=language,
                filter_params={"licence_id": licences[record["licence_content"]].id},
            )

        # Add a plugin for the course participation license
        if record["licence_participation"]:
            placeholder_licence_participation = course_page.placeholders.get(
                slot="course_license_participation"
            )
            create_or_update_single_plugin(
                placeholder_licence_participation,
                LicencePlugin,
                language=language,
                filter_params={
                    "licence_id": licences[record["licence_participation"]].id
                },
            )

        # Add the course run
        run_slug = slugify(record["session"])
        run_reverse_id = f"{reverse_id:s}_{run_slug:s}"
        try:
            run_page = Page.objects.get(
                reverse_id=run_reverse_id,
                node__parent__cms_pages=course_page,
                publisher_is_draft=True,
            )
        except Page.DoesNotExist:
            run_page = create_page(
                record["session"],
                COURSERUNS_PAGE["template"],
                language,
                parent=course_page,
                reverse_id=run_reverse_id,
                slug=run_slug,
            )
        else:
            # Update slug and title that may have changed
            run_title = run_page.title_set.get(language=language)
            run_title.slug = run_slug
            run_title.title = record["session"]
            run_title.save()

        run, _created = CourseRun.objects.update_or_create(
            extended_object__reverse_id=run_reverse_id,
            extended_object__publisher_is_draft=True,
            defaults={
                "extended_object": run_page,
                "start": parse_date(record["start"]),
                "end": parse_date(record["end"]),
                "enrollment_start": parse_date(record["enrollment_start"]),
                "enrollment_end": parse_date(record["enrollment_end"]),
                "languages": record["languages"].split(","),
            },
        )

        run.save()
        course_page.publish(language)

        # We can publish the run now that the course is published
        run_page.publish(settings.LANGUAGE_CODE)

        yield course_page
