import unittest
import re
from idea.parser_number import multi_season_episode_pattern


class TestMultiSeasonEpisodePattern(unittest.TestCase):
    def setUp(self) -> None:
        self.multi_season_episode_test_cases = [
            ('2x01', [
                (None, '2', None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                 None, 'x', None, None, '01', None, None, None, None, None, None)
            ]),
            ('2x01v2', [
                (None, '2', None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                 None, 'x', None, None, '01', 'v', '2', None, None, None, None)
            ]),
            ('s01e03', [
                ('s', '01', None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                 None, None, None, 'e', '03', None, None, None, None, None, None)
            ]),
            ('s01e03v2', [
                (
                    's', '01', None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                    None, None, None, 'e', '03', 'v', '2', None, None, None, None)
            ]),
            ('s01-02xe001-150', [
                (
                    's', '01', None, None, None, None, None, None, '-', None, '02', None, None, None, None,
                    None, None, None, 'x', 'e', '001', None, None, '-', '150', None, None)
            ]),
            ('s01-02xe001-150v2', [
                ('s', '01', None, None, None, None, None, None, '-', None, '02', None, None, None,
                 None, None, None, None, 'x', 'e', '001', None, None, '-', '150', 'v', '2')
            ]),
            ('s01-02xe001v3-150v2', [
                ('s', '01', None, None, None, None, None, None, '-', None, '02', None, None, None,
                 None, None, None, None, 'x', 'e', '001', 'v', '3', '-', '150', 'v', '2')
            ]),
            ('s01-s02xe001-150', [
                ('s', '01', None, None, None, None, None, None, '-', 's', '02', None, None, None, None,
                 None, None, None, 'x', 'e', '001', None, None, '-', '150', None, None)
            ]),
            ('s01-s02xe001-150v2', [
                ('s', '01', None, None, None, None, None, None, '-', 's', '02', None, None, None,
                 None, None, None, None, 'x', 'e', '001', None, None, '-', '150', 'v', '2')
            ]),
            ('s01-s02xe001v3-150v2', [
                ('s', '01', None, None, None, None, None, None, '-', 's', '02', None, None, None,
                 None, None, None, None, 'x', 'e', '001', 'v', '3', '-', '150', 'v', '2')
            ]),
            ('s01e03-s02e04', [
                ('s', '01', None, None, 'e', '03', None, None, '-', 's', '02', None, None, None, None,
                 None, None, None, None, 'e', '04', None, None, None, None, None, None)
            ]),
            ('s01e03-s02e04v2', [
                ('s', '01', None, None, 'e', '03', None, None, '-', 's', '02', None, None, None, None,
                 None, None, None, None, 'e', '04', 'v', '2', None, None, None, None)
            ]),
            ('s01e03v4-s02e04v2-s03e05v3', [
                ('s', '01', None, None, 'e', '03', 'v', '4', '-', 's', '02', None, None, None, None, None, None, None,
                 None, 'e', '04', 'v', '2', None, None, None, None),
                ('s', '03', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                 None, None, 'e', '05', 'v', '3', None, None, None, None)
            ]),
            ('s01e03-04', [
                ('s', '01', None, None, None, None, None, None, None, None, None, None, None, None, None,
                 None, None, None, None, 'e', '03', None, None, '-', '04', None, None)
            ]),
            ('s01e03-04v2', [
                ('s', '01', None, None, None, None, None, None, None, None, None, None, None, None, None,
                 None, None, None, None, 'e', '03', None, None, '-', '04', 'v', '2')
            ]),
            ('s01e03v4-04v2', [
                ('s', '01', None, None, None, None, None, None, None, None, None, None, None, None, None,
                 None, None, None, None, 'e', '03', 'v', '4', '-', '04', 'v', '2')
            ]),
            ('e01', [
                (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                 None, None, None, None, '01', None, None, None, None, None, None)
            ]),
            ('e01v2', [
                (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                 None, None, None, None, '01', 'v', '2', None, None, None, None)
            ]),
            ('01', [
                (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                 None, None, None, None, '01', None, None, None, None, None, None)
            ]),
            ('01v2', [
                (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                 None, None, None, None, '01', 'v', '2', None, None, None, None)
            ]),
            ('01-02', [
                (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                 None, None, None, None, '01', None, None, '-', '02', None, None)
            ]),
            ('01-02v2', [
                (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                 None, None, None, None, '01', None, None, '-', '02', 'v', '2')
            ]),
            ('01v2-02', [
                (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                 None, None, None, None, '01', 'v', '2', '-', '02', None, None)
            ]),
            ('01v2-02v3', [
                (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                 None, None, None, None, None, '01', 'v', '2', '-', '02', 'v', '3')
            ])

        ]

    def test_multi_season_episode_pattern(self):
        for test_input, expected_output in self.multi_season_episode_test_cases:
            matches = list(re.finditer(multi_season_episode_pattern, test_input))
            self.assertEqual(len(matches), len(expected_output))
            for match, expected_groups in zip(matches, expected_output):
                self.assertEqual(match.groups(), expected_groups)


if __name__ == "__main__":
    unittest.main()
