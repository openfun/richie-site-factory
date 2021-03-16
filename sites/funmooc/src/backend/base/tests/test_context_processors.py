"""Test funmooc context processors"""

import re

from django.test import TestCase
from django.test.utils import override_settings

from richie.apps.core.factories import PageFactory, UserFactory
from richie.apps.courses.factories import CourseFactory, OrganizationFactory


class ContextProcessorsTestCase(TestCase):
    """
    Test suite for the context processors
    """

    @override_settings(MARKETING_SITE_ID="123456")
    def test_context_processors_add_xiti_settings_if_exists(self):
        """
        Create a page and make sure it includes the marketing context as included
        in `base.html`.
        """
        page = PageFactory(
            should_publish=True,
            template="richie/single_column.html",
        )

        response = self.client.get(page.get_public_url(), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"xiti":')
        self.assertContains(response, f'"level2": "{page.node.get_root().pk}"')
        self.assertContains(response, '"site_id": "123456"')

    @override_settings(MARKETING_SITE_ID=None)
    def test_context_processors_do_not_add_xiti_settings_if_marketing_site_id_is_not_defined(
        self,
    ):
        """
        If MARKETING_SIDE_ID setting is not defined,
        frontend context should contains an empty xiti object
        """
        page = PageFactory(
            should_publish=True,
            template="richie/single_column.html",
        )

        response = self.client.get(page.get_public_url(), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"xiti": {}')

    @override_settings(MARKETING_SITE_ID="123456")
    def test_context_processors_do_not_add_xiti_settings_if_page_is_draft(
        self,
    ):
        """
        If the current page is a draft,
        frontend context should contains an empty xiti object
        """
        user = UserFactory(is_staff=True, is_superuser=True)
        self.client.login(username=user.username, password="password")  # nosec

        page = PageFactory(
            should_publish=False,
            template="richie/single_column.html",
        )

        response = self.client.get(page.get_absolute_url(), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"xiti": {}')

    @override_settings(MARKETING_SITE_ID="123456")
    def test_context_processors_get_organizations_code(self):
        """
        If an organization is linked to the page or there are organization plugins on the page,
        marketing context should contains the code of these organizations
        """
        organization = OrganizationFactory(should_publish=True)
        course = CourseFactory(should_publish=True, fill_organizations=[organization])

        response = self.client.get(course.extended_object.get_public_url(), follow=True)
        pattern = r'"organizations": \["{code:s}"\]'.format(code=organization.code)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(re.search(pattern, str(response.content)))

    def test_context_processors_retrieve_privacy_page_url_if_exists(self):
        """
        If a privacy policy page exists,
        tarteaucitron context should contains its url.
        """
        page = PageFactory(
            should_publish=True,
            template="richie/single_column.html",
            title__language="fr",
            languages="fr",
        )

        response = self.client.get(page.get_public_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"tarteaucitron":')
        self.assertContains(response, '"privacyUrl": null')

        privacy_page = PageFactory(
            title__title="Privacy policy",
            should_publish=True,
            reverse_id="annex__privacy",
            title__language="fr",
            languages="fr",
        )

        response = self.client.get(page.get_public_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, f'"privacyUrl": "{privacy_page.get_public_url()}"'
        )

    def test_context_processors_queries_are_cached(self):
        """
        Once the page is cached, no db queries should be made again
        """
        organizations = OrganizationFactory.create_batch(
            2, should_publish=True, page_languages=["fr"]
        )
        course = CourseFactory(
            should_publish=True, fill_organizations=organizations, page_languages=["fr"]
        )
        page = course.extended_object

        # Get the page a first time to cache it
        self.client.get(page.get_public_url())

        # Check that db queries are well cached
        # The one remaining is related to django-cms
        with self.assertNumQueries(1):
            self.client.get(page.get_public_url())
