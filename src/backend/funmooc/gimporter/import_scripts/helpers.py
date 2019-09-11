# Helpers used by import scripts to import fixtures from Google sheet.
import io
import re
import urllib
from datetime import datetime

from django.conf import settings
from django.core.files import File

from cms.api import add_plugin, create_page
from cms.models import Page
from filer.models.filemodels import File as FilerFile
from filer.models.imagemodels import Image as FilerImage
from PIL import Image
from pytz import timezone
from richie.apps.courses.defaults import PAGES_INFO


def extract_and_replace_media(content, folder=None):
    """
    Find relative paths targetting media files in the content, import the corresponding files
    and replace the old paths by the new ones in the content.
    """
    # Find media files in the content
    media_paths = re.findall(r'"(/media[^> ]*)"', content)

    for path in media_paths:
        try:
            file_object = import_file(settings.GIMPORTER_BASE_URL + path, folder=folder)
        except urllib.error.HTTPError:
            # Media files that can't be found on the old fun-mooc.fr site are ignored
            continue

        # Replace the url by the url of the new file in Django filer
        content = content.replace(path, file_object.url)

    return content


def import_file(url, folder=None):
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

    # Determine whether the downloaded file is an image or not
    try:
        Image.open(in_memory_file)
    except IOError:
        model_class = FilerFile
    else:
        model_class = FilerImage

    # Look for an existing image object for this file to avoid duplicates
    file_object = model_class(file=File(in_memory_file, filename), folder=folder)
    file_object.generate_sha1()

    existing_file_object = model_class.objects.filter(sha1=file_object.sha1).first()
    if existing_file_object:
        # update its location as it may have changed
        existing_file_object.folder = folder
        existing_file_object.save()
        return existing_file_object

    # Actually create a new file object
    file_object.save()
    return file_object


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


def parse_date(date_string):
    """
    Parse a date string of the form "dd.mm.yy" to a timezone aware datetime assuming it is
    Paris time
    """
    return (
        timezone("Europe/Paris").localize(datetime.strptime(date_string, "%d.%m.%y"))
        if date_string
        else None
    )


def parse_datetime(datetime_string):
    """
    Parse a datetime string of the form "yyyy-mm-dd HH:MM:SS" and make it timezone aware
    assuming it is Paris time.
    """
    return (
        timezone("Europe/Paris").localize(
            datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
        )
        if datetime_string
        else None
    )
