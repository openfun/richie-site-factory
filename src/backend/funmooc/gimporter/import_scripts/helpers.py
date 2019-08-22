import io
import urllib

from django.conf import settings
from django.core.files import File

from cms.api import add_plugin, create_page
from cms.models import Page
from filer.models.imagemodels import Image
from richie.apps.courses.defaults import PAGES_INFO


def create_image(url):
    """
    Upload an image from a url and create it in Django Filer.
    We use the image sha1 hash to make sure we only create a given image once.
    """

    # Clean the url and make sure it is safe (bandit wants to make sure we don't access a file
    # from the filesystem with urls starting with ftp:// and file://
    url = url.strip()
    if not url.lower().startswith("http"):
        raise ValueError("Invalid image url: %s", url)

    try:
        in_memory_file = io.BytesIO(
            urllib.request.urlopen(url).read()  # nosec (above validated url is http)
        )
    except UnicodeEncodeError:
        # Encode the url's path to allow for special characters
        scheme, netloc, path, query, fragment = urllib.parse.urlsplit(url)
        path = urllib.parse.quote(path)
        url = urllib.parse.urlunsplit((scheme, netloc, path, query, fragment))
        in_memory_file = io.BytesIO(
            urllib.request.urlopen(url).read()  # nosec (above validated url is http)
        )

    filename = urllib.parse.urlparse(url).path.split("/")[-1]

    # Look for an existing image object for this file to avoid duplicates
    image = Image(file=File(in_memory_file, filename))
    image.generate_sha1()
    existing_image = Image.objects.filter(sha1=image.sha1).first()
    if existing_image:
        return existing_image

    # There is no existing image so we create a new one
    image.save()
    return image


def create_page_from_info(reverse_id):
    """Create a page for "known" pages in PAGES_INFO given its "reverse_id"."""
    try:
        return Page.objects.get(reverse_id=reverse_id, publisher_is_draft=True)
    except Page.DoesNotExist:
        return create_page(
            PAGES_INFO[reverse_id]["title"],
            PAGES_INFO[reverse_id]["template"],
            settings.LANGUAGE_CODE,
            reverse_id=reverse_id,
            published=True,
        )


def create_or_update_single_plugin(
    placeholder, plugin_type, filter_params=None, **kwargs
):
    """Create or update a single plugin linked to a given placeholder.

    Arguments:
    ----------
    placeholder (cms.models.Placeholder): the placeholder holding the targeted plugin,
    filter_params (dict): Django ORM filter parameters that uniquely target a plugin for the
        given placeholder
    kwargs (dict): values to update on the plugin model.

    """
    filter_params = filter_params or {}
    try:
        plugin = plugin_type.model.objects.get(placeholder=placeholder, **filter_params)
    except plugin_type.model.DoesNotExist:
        add_plugin(
            placeholder=placeholder, plugin_type=plugin_type, **kwargs, **filter_params
        )
    else:
        plugin_type.model.objects.filter(id=plugin.id).update(
            plugin_type=plugin_type.__name__, **kwargs
        )
