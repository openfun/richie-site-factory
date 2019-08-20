"""Django authentication backends.

For more information visit
https://docs.djangoproject.com/en/dev/topics/auth/customizing/.

This authentication backend is inspired from the official edx's auth-backends
project:
https://github.com/edx/auth-backends/blob/master/auth_backends/backends.py
"""

from django.core.cache import cache

import jwt
from social_core.backends.oauth import BaseOAuth2

EDX_USER_PROFILE_TO_DJANGO = {
    "preferred_username": "username",
    "email": "email",
    "name": "full_name",
    "given_name": "first_name",
    "family_name": "last_name",
    "locale": "language",
    "user_id": "user_id",
    "administrator": "is_staff",
    "superuser": "is_superuser",
}


class EdXOAuth2(BaseOAuth2):
    """
    OAuth2-based backend to authenticate with OpenEdx's LMS OAuth2 provider
    (hawthorn release).
    """

    name = "edx-oauth2"

    ACCESS_TOKEN_METHOD = "POST"  # nosec
    DEFAULT_SCOPE = ["profile", "email"]
    ID_KEY = "preferred_username"

    # EXTRA_DATA is used to store important data in the
    # UserSocialAuth.extra_data field. See:
    # https://python-social-auth.readthedocs.io/en/latest/backends/oauth.html?highlight=extra_data
    EXTRA_DATA = [
        # Update the stored user_id, if it's present in the response
        ("user_id", "user_id", True),
        # Update the stored refresh_token, if it's present in the response
        ("refresh_token", "refresh_token", True),
    ]

    def endpoint(self):
        """Get OAuth2 provider endpoint."""
        return self.setting("ENDPOINT").strip("/")

    @property
    def provider_configuration(self):
        """Get OAuth2 provider configuration and cache its configuration for a week."""

        cache_key = "edx_oauth2_provider_configuration"
        config = cache.get(cache_key)

        if not config:
            config = self.get_json(
                self.endpoint() + "/.well-known/openid-configuration"
            )

            # Cache for one week since the configuration rarely changes
            cache.set(
                cache_key,
                config,
                self.setting("PROVIDER_CONFIGURATION_CACHE_TTL", 604800),
            )

        return config

    def authorization_url(self):
        """Get OAuth2 provider authorization URL."""
        return self.provider_configuration.get("authorization_endpoint")

    def access_token_url(self):
        """Get OAuth2 provider access token URL."""
        return self.provider_configuration.get("token_endpoint")

    def end_session_url(self):
        """Get OAuth2 provider end session URL."""
        return self.provider_configuration.get("end_session_endpoint")

    def auth_complete_params(self, state=None):
        """Force the access token type to be JWT."""
        params = super().auth_complete_params(state)
        params.update({"token_type": "jwt"})
        return params

    def user_data(self, access_token, *args, **kwargs):
        """Get claimed user data from the JWT formatted access token."""
        decoded_access_token = jwt.decode(access_token, verify=False)
        return {
            key: decoded_access_token[key]
            for key in EDX_USER_PROFILE_TO_DJANGO
            if key in decoded_access_token
        }

    def get_user_details(self, response):
        """Convert claim user details from the response."""
        return {
            d: response[s]
            for s, d in EDX_USER_PROFILE_TO_DJANGO.items()
            if s in response
        }
