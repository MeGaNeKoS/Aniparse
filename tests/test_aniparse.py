from unittest import TestCase

import aniparse
from aniparse.element import ElementCategory
from aniparse.keyword import KeywordManager, option
from tests.fixtures.table import table


class TestAniparse(TestCase):

    def test_table(self):
        keyword = KeywordManager()
        keyword.add(ElementCategory.RELEASE_GROUP, option["default"], [
            'THORA'
        ])
        for index, expected in enumerate(table):
            filename = expected["file_name"]
            anime = aniparse.parse(filename, keyword_manager=keyword)
            self.assertEqual(expected, anime, 'on entry number %d' % index)
