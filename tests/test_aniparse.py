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

    def test_season_part_as_unique(self):
        titles = {
            'Attack On Titan Season 3 Part 2.mkv': {
                True: {'file_name': 'Attack On Titan Season 3 Part 2.mkv',
                       'file_extension': 'mkv',
                       'anime_title': 'Attack On Titan Season 3 Part 2'},
                False: {'file_name': 'Attack On Titan Season 3 Part 2.mkv',
                        'file_extension': 'mkv',
                        'anime_title': 'Attack On Titan',
                        'anime_season_prefix': 'Season',
                        'anime_season': 3},
            },
            'Attack On Titan Season 3 Part 2 - 1.mkv': {
                True: {'file_name': 'Attack On Titan Season 3 Part 2 - 1.mkv',
                       'file_extension': 'mkv',
                       'anime_title': 'Attack On Titan Season 3 Part 2',
                       'episode_number': 1},
                False: {'file_name': 'Attack On Titan Season 3 Part 2 - 1.mkv',
                        'file_extension': 'mkv',
                        'anime_title': 'Attack On Titan',
                        'anime_season_prefix': 'Season',
                        'anime_season': 3,
                        'episode_number': 1},
            }
        }

        for title, options in titles.items():
            for condition, expected in options.items():
                anime = aniparse.parse(title, options={'season_part_as_unique': condition})
                self.assertEqual(expected, anime)
