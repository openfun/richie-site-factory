from .docker_run_production import *


DEBUG = True
REQUIRE_DEBUG = True
PIPELINE_ENABLED = False

STATICFILES_STORAGE = "openedx.core.storage.DevelopmentStorage"
STATIC_ROOT = "/edx/app/edxapp/staticfiles"
STATIC_URL = "/static/"
MEDIA_ROOT = "/edx/app/edxapp/data/media"
WEBPACK_CONFIG_PATH = "webpack.dev.config.js"

SECRET_KEY = "foo"

ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = config(
    "EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)

# Disable CourseTalk service (student course reviewing)
COURSE_REVIEWS_TOOL_PROVIDER_FRAGMENT_NAME = None
COURSE_REVIEWS_TOOL_PROVIDER_PLATFORM_KEY = None
FEATURES["ENABLE_DISCUSSION_SERVICE"] = False

FEATURES["AUTOMATIC_AUTH_FOR_TESTING"] = True
FEATURES["RESTRICT_AUTOMATIC_AUTH"] = False

# SSO: oauth2 provider
FEATURES["ENABLE_OAUTH2_PROVIDER"] = True
OAUTH_OIDC_ISSUER = "https://lms:8073/oauth2"
