"""
API routes exposed by our base app.
"""
from django.urls import re_path

from .views import redirect_edx_courses

COURSE_KEY_PATTERN = r"course-v1:(?P<organization>.+)\+(?P<course>.+)\+(?P<session>.+)"

urlpatterns = [
    re_path(
        r"courses/{}/about/?$".format(COURSE_KEY_PATTERN),
        redirect_edx_courses,
        name="redirect_edx_courses",
    )
]
