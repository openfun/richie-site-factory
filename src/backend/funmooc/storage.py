"""Customizing Django storage backends to enable blue/green deployments."""
from django.conf import settings
from django.contrib.staticfiles.storage import ManifestFilesMixin, StaticFilesStorage

from storages.backends.s3boto3 import S3Boto3Storage


class ConfigurableManifestFilesMixin(ManifestFilesMixin):
    """Allow configuring the name of the manifest file via Django settings."""

    manifest_name = settings.STATICFILES_MANIFEST_NAME


class ConfigurableManifestStaticFilesStorage(
    ConfigurableManifestFilesMixin, StaticFilesStorage
):
    """A ManifestStaticFilesStorage backend with configurable manifest file name.
    A static file system storage backend which saves files on the filesystem with unique names
    derived from their content. The name of the manifest file is configurable.
    """

    pass


class ConfigurableManifestS3Boto3Storage(
    ConfigurableManifestFilesMixin, S3Boto3Storage
):
    """A S3Boto3Storage backend to serve static files via CloudFront with blue/green deployments.

    A static file system storage backend which saves files on AWS S3 with unique names
    derived from their content. The name of the manifest file is configurable to allow blue/green
    deployments.
    """

    bucket_name = settings.AWS_STATIC_BUCKET_NAME
    custom_domain = settings.AWS_CLOUDFRONT_DOMAIN
    location = settings.STATIC_URL


class MediaStorage(S3Boto3Storage):
    """A S3Boto3Storage backend to serve media files via CloudFront."""
    bucket_name = settings.AWS_MEDIA_BUCKET_NAME
    custom_domain = settings.AWS_CLOUDFRONT_DOMAIN
    file_overwrite = False
    location = settings.MEDIA_URL
