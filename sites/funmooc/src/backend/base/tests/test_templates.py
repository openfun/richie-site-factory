"""Test fun-mooc views."""
import random
from datetime import timedelta

from django.test import TestCase
from django.utils import formats, timezone, translation

import lxml.html  # nosec
from lxml import etree  # nosec
from richie.apps.courses.factories import CourseFactory, CourseRunFactory


class TemplatesTestCase(TestCase):
    """Test the funmooc template overrides."""

    def test_templates_course_detail_no_open_course_run(self):
        """For a course without course runs. It should be indicated in the side column."""
        course = CourseFactory(should_publish=True)
        page = course.extended_object

        url = page.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        html = lxml.html.fromstring(response.content)

        # Check syllabus intro
        header = str(etree.tostring(html.cssselect(".subheader__intro")[0]))
        self.assertNotIn("course-detail__run-descriptions", header)
        self.assertNotIn("session", header)

        # Check syllabus aside column
        aside = str(etree.tostring(html.cssselect(".course-detail__aside")[0]))
        self.assertNotIn("course-detail__run-descriptions", header)
        self.assertNotIn("S&#226;&#128;&#153;inscrire maintenant", aside)
        self.assertNotIn("Aucune autre session ouverte", aside)
        self.assertIn("Aucune session ouverte", aside)

    def test_templates_course_detail_one_open_course_run(self):
        """
        For a course with one open course run, the course run should be in the header
        and the side column should display an indication that there is no other course run.
        """
        course = CourseFactory()
        page = course.extended_object

        # Create an open course run
        now = timezone.now()
        CourseRunFactory(
            direct_course=course,
            start=now + timedelta(hours=1),
            enrollment_start=now - timedelta(hours=1),
            enrollment_end=now + timedelta(hours=1),
        )

        self.assertTrue(page.publish("fr"))

        url = page.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        html = lxml.html.fromstring(response.content)

        # Check syllabus intro
        header = str(etree.tostring(html.cssselect(".subheader__intro")[0]))
        self.assertEqual(header.count("course-detail__run-descriptions"), 1)
        self.assertIn("S&#226;&#128;&#153;inscrire maintenant", header)

        # Check syllabus aside column
        aside = str(etree.tostring(html.cssselect(".course-detail__aside")[0]))
        self.assertNotIn("course-detail__run-descriptions", aside)
        self.assertNotIn("S&#226;&#128;&#153;inscrire maintenant", aside)
        self.assertIn("Aucune autre session ouverte", aside)

    def test_templates_course_detail_two_open_course_runs(self):
        """
        For a course with two open course runs, the course run starting next should be in the
        header and the other course run should be in the side column.
        """
        course = CourseFactory()
        page = course.extended_object
        url = page.get_absolute_url()

        # Create 2 open course runs
        now = timezone.now()
        start1, start2 = random.sample(
            [now + timedelta(days=1), now + timedelta(days=2)], 2
        )
        CourseRunFactory(
            direct_course=course,
            start=start1,
            enrollment_start=now - timedelta(hours=1),
            enrollment_end=now + timedelta(hours=1),
        )
        CourseRunFactory(
            direct_course=course,
            start=start2,
            enrollment_start=now - timedelta(hours=1),
            enrollment_end=now + timedelta(hours=1),
        )

        self.assertTrue(page.publish("fr"))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        html = lxml.html.fromstring(response.content)

        # Check syllabus intro
        header = str(etree.tostring(html.cssselect(".subheader__intro")[0]))
        self.assertEqual(header.count("course-detail__runs--open"), 1)
        self.assertIn("S&#226;&#128;&#153;inscrire maintenant", header)
        date_string = formats.date_format(min(start1, start2))
        with translation.override("fr"):
            self.assertIn(f"Du {date_string}", header)

        # Check syllabus aside column
        aside = str(etree.tostring(html.cssselect(".course-detail__aside")[0]))
        self.assertEqual(header.count("course-detail__runs--open"), 1)
        self.assertIn("S&#226;&#128;&#153;inscrire maintenant", aside)
        date_string = formats.date_format(max(start1, start2))
        with translation.override("fr"):
            self.assertIn(f"Du {date_string}", aside)
