"""Test base utils."""

from django.test import TestCase

from ..utils import merge_dict


class UtilsTestCase(TestCase):
    """Validate that utils in the base app work as expected."""

    def test_utils_merge_dict(self):
        """Update a deep nested dictionary with another deep nested dictionary."""
        d1 = {"k1": {"k11": {"a": 0, "b": 1}}}
        d2 = {"k1": {"k11": {"b": 10}, "k12": {"a": 3}}}
        self.assertEqual(
            merge_dict(d1, d2), {"k1": {"k11": {"a": 0, "b": 10}, "k12": {"a": 3}}}
        )
