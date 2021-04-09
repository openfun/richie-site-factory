"""
API routes exposed by our base app.
"""
from django.urls import re_path

from .views import redirect_edx_courses

# Support both course OpenEdX routes
#  http://open-fun.fr/courses/course-v1:acme+00001+session01/about
#  http://open-fun.fr/courses/acme/00001/session01/about
COURSE_KEY_PATTERN = (
    r"(course-v1:)?(?P<organization>.+)(\/|\+)(?P<course>.+)(\/|\+)(?P<session>.+)"
)

urlpatterns = [
    re_path(
        r"courses/{}/about/?$".format(COURSE_KEY_PATTERN),
        redirect_edx_courses,
        name="redirect_edx_courses",
    ),
]
