import logging

from aniparse.element import ElementCategory
from aniparse.keyword import KeywordManager
from aniparse.aniparse import Aniparse
from aniparse.parser_option import Options

logger = logging.getLogger(__name__)

__all__ = ['parse']


def parse(filename, options: Options = None, ignore_errors=True, keyword_manager: KeywordManager = None, as_dict=False):
    options = options or Options(default=True)
    keyword_manager = keyword_manager or KeywordManager(options, cache=True)

    try:
        parser = Aniparse(filename, options, keyword_manager)

    except Exception as e:
        logger.error('Error parsing {}: {}'.format(filename, e))
        if ignore_errors:
            if as_dict:
                return {
                    ElementCategory.FILE_NAME.value: filename
                }
            else:
                return {
                    ElementCategory.FILE_NAME: filename
                }
        raise
