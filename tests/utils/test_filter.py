import os
import unittest

from echis.utils.filter import is_bad_word


class TestFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.path = os.path.abspath("../../echis/csv/bad_words.csv")

    def test_is_bad_word_get_true(self):
        is_bad = is_bad_word("fuck", path=self.path)
        self.assertTrue(is_bad)

    def test_is_not_bad_word(self):
        is_bad = is_bad_word("random", path=self.path)
        self.assertFalse(is_bad)