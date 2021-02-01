"""Test fun-mooc views."""
from django.test import TestCase

from richie.apps.core.factories import PageFactory, TitleFactory
from richie.apps.courses.factories import CourseFactory, OrganizationFactory


class CoursesEdxRedirectViewsTestCase(TestCase):
    """Test the "redirect_edx_courses" view."""

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

    def test_views_redirect_edx_courses_fallback_organization(self):
        """
        OpenEdX course urls are redirected to the organization page if the course page
        can not be found.
        """
        OrganizationFactory(code="sorbonne", page_title="Sorbonne", should_publish=True)

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
            reverse_id="search",
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
