"""Test fun-mooc views."""
from django.test import TestCase

from lxml import etree  # nosec
from richie.apps.core.factories import PageFactory, TitleFactory, UserFactory
from richie.apps.courses.factories import CourseFactory, OrganizationFactory


class ResourcesEdxRedirectViewsTestCase(TestCase):
    """Test the "redirect_edx_resources" view."""

    def test_views_redirect_edx_courses_success(self):
        """OpenEdX course urls are redirected to the corresponding page in richie."""
        course = CourseFactory(
            code="abc", page_title="Physique 101", should_publish=True
        )
        TitleFactory(page=course.extended_object, language="en", title="Physics 101")
        course.extended_object.publish("en")

        response = self.client.get("/courses/course-v1:sorbonne+abc+001/about/")

        self.assertRedirects(
            response,
            "/fr/physique-101/",
            status_code=301,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_views_redirect_edx_courses_success_with_old_course_uri(self):
        """Old OpenEdX course urls are redirected to the corresponding page in richie."""
        course = CourseFactory(
            code="abc", page_title="Physique 101", should_publish=True
        )
        TitleFactory(page=course.extended_object, language="en", title="Physics 101")
        course.extended_object.publish("en")

        response = self.client.get("/courses/sorbonne/abc/001/about/")

        self.assertRedirects(
            response,
            "/fr/physique-101/",
            status_code=301,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_views_redirect_edx_organization_success(self):
        """OpenEdX organization urls are redirected to the corresponding page in richie."""
        organization = OrganizationFactory(
            code="sorbonne",
            page_title="Sorbonne",
            should_publish=True,
        )
        TitleFactory(
            page=organization.extended_object,
            language="en",
            title="Sorbonne",
        )
        organization.extended_object.publish("en")

        response = self.client.get("/universities/sorbonne")

        self.assertRedirects(
            response,
            "/fr/sorbonne/",
            status_code=301,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_views_redirect_edx_courses_fallback_organization(self):
        """
        OpenEdX course urls are redirected to the organization page if the course page
        can not be found.
        """
        OrganizationFactory(page_title="Sorbonne", code="sorbonne", should_publish=True)

        response = self.client.get("/courses/course-v1:sorbonne+abc+001/about/")

        self.assertRedirects(
            response,
            "/fr/sorbonne/",
            status_code=301,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_views_redirect_edx_courses_fallback_search_page(self):
        """
        OpenEdX course urls are redirected to the search page if neither the course page
        nor the organization page can be found.
        """
        PageFactory(
            reverse_id="courses",
            template="search/search.html",
            title__title="Recherche",
            title__language="fr",
            should_publish=True,
        )

        response = self.client.get("/courses/course-v1:sorbonne+abc+001/about/")

        self.assertRedirects(
            response,
            "/fr/recherche/",
            status_code=301,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_views_redirect_edx_courses_no_fallback(self):
        """
        OpenEdX course urls are not redirected if the french version of the page is not
        published (english is not yet activated on the public site).
        """
        course = CourseFactory(code="abc", page_title="Mon titre", should_publish=True)
        TitleFactory(page=course.extended_object, language="en", title="My title")
        course.extended_object.publish("en")
        course.extended_object.unpublish("fr")

        response = self.client.get("/courses/course-v1:org+abc+001/about/")

        self.assertRedirects(
            response,
            "/fr/courses/course-v1:org+abc+001/about/",
            status_code=302,
            target_status_code=404,
            fetch_redirect_response=True,
        )


class DjangoCheckSeoTestCase(TestCase):
    def test_views_django_check_seo_is_accessible(self):
        """
        Check that Django Check SEO is accessible by an admin user
        """
        url = "/django-check-seo/?page=/"
        response = self.client.get(url)

        # - Anonymous user is redirected to the admin login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login", response.url)

        # - Otherwise the Django Check SEO report is displayed
        user = UserFactory(is_staff=True, is_superuser=True)
        self.client.login(username=user.username, password="password")  # nosec

        response = self.client.get(url)
        html = etree.fromstring(response.content)
        page_title = html.cssselect("title")[0].text

        self.assertEqual(response.status_code, 200)
        self.assertEqual(page_title, "Django check SEO")
