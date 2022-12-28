# Change the init comit to: Initial commit for project rewrite to improve performance and simplify class hierarchy

from aniparse.element import ElementCategory
from aniparse.keyword import Keyword
from aniparse.keyword_manager import KeywordManager


# import logging
#
# from aniparse.aniparse import Aniparse
# from aniparse.element import ElementCategory
# from aniparse.keyword import KeywordManager
#
# logger = logging.getLogger(__name__)
#
# __all__ = ['parse']
#
# default_options = {
#     'allowed_delimiters': ' _.&+,|',
#     'check_title_enclosed': True,
#     'eps_lower_than_alt': True,
#     'ignored_dash': True,
#     'ignored_strings': [],
#     'keep_delimiters': False,
#     'max_extension_length': 4,
#     'title_before_episode': True,
#     'valid_video_formats': ['3GP', 'AVI', 'DIVX', 'FLV', 'M2TS', 'MKV', 'MOV',
#                             'MP4', 'MPG', 'OGM', 'RM', 'RMVB', 'TS', 'WEBM',
#                             'WMV']
#
# }
#
#
# def parse(filename, options=None, ignore_errors=True, keyword_manager: KeywordManager = KeywordManager()):
#     if options is None:
#         options = {}
#
#     # Add missing options
#     for key, value in default_options.items():
#         options.setdefault(key, value)
#     try:
#         parser = Aniparse(filename, options, keyword_manager)
#         parser.parse()
#         return parser.populate()
#     except Exception as e:
#         logger.error('Error parsing {}: {}'.format(filename, e))
#         if ignore_errors:
#             return {
#                 ElementCategory.FILE_NAME.value: filename
#             }
#         raise
