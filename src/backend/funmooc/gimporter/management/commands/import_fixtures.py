"""Import fixtures management command."""
import json
import time

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from ...import_scripts.blogposts import import_blogposts
from ...import_scripts.categories import import_categories
from ...import_scripts.courses import import_courses
from ...import_scripts.organizations import import_organizations
from ...import_scripts.persons import import_persons

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://spreadsheets.google.com/feeds"]


class Command(BaseCommand):
    """Import pages from a Google Sheet."""

    help = __doc__

    def add_arguments(self, parser):

        parser.add_argument(
            "google_sheet_id",
            nargs="?",
            default=settings.GOOGLE_SHEET_ID,
            help="Google Sheet ID from which to import fixtures",
        )

    def import_pages(self, sheet, method, message):
        """
        Wrapper that adds displaying message and timing information when calling a given method.
        """
        self.stdout.write(message + " ", ending="")

        start = time.monotonic()
        for page in method(sheet):
            self.stdout.write(".", ending="")
        elapsed = time.monotonic() - start

        self.stdout.write(self.style.SUCCESS(" OK"), ending="")
        self.stdout.write(f" {elapsed:.3f}s")

    def handle(self, *args, **options):
        """Management command to import fixtures from a Google Sheet for each type of page."""
        if not settings.GOOGLE_SHEET_CREDENTIALS:
            raise CommandError(
                (
                    "You must provide credentials as a json string for a Google API Service "
                    'Account via the "DJANGO_GOOGLE_SHEET_CREDENTIALS" environment variable.'
                )
            )

        if not options["google_sheet_id"]:
            raise CommandError(
                (
                    "You must provide the ID of a Google sheet via the "
                    '"DJANGO_GOOGLE_SHEET_ID" environment variable or as a command argument.'
                )
            )

        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            json.loads(settings.GOOGLE_SHEET_CREDENTIALS), SCOPES
        )
        client = gspread.authorize(credentials)
        sheet = client.open_by_key(options["google_sheet_id"])

        self.import_pages(sheet, import_categories, "Importing categories")
        self.import_pages(sheet, import_organizations, "Importing organizations")
        self.import_pages(sheet, import_persons, "Importing persons")
        self.import_pages(sheet, import_courses, "Importing courses")
        self.import_pages(sheet, import_blogposts, "Importing blog posts")
