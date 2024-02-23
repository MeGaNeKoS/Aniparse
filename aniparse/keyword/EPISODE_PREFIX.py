from aniparse.element import Metadata
from aniparse.abstraction.KeywordBase import ElementEntry

episode_prefix = [
    ElementEntry('EP', {Metadata.EPISODE_PREFIX}, regex_dict={r'EP\.?': {0: {Metadata.EPISODE_PREFIX}}}),
    ElementEntry('EPS', {Metadata.EPISODE_PREFIX},
                 regex_dict={r'EPS\.?': {0: {Metadata.EPISODE_PREFIX}}}),
    ElementEntry('EPISODE', {Metadata.EPISODE_PREFIX},
                 regex_dict={r'EPISODE\.?': {0: {Metadata.EPISODE_PREFIX}}}),
    ElementEntry('EPISODES', {Metadata.EPISODE_PREFIX},
                 regex_dict={r'EPISODES\.?': {0: {Metadata.EPISODE_PREFIX}}}),
    ElementEntry('CAPITULO', {Metadata.EPISODE_PREFIX}),
    ElementEntry('EPISODIO', {Metadata.EPISODE_PREFIX}),
    ElementEntry('FOLGE', {Metadata.EPISODE_PREFIX}),
    ElementEntry('E', {Metadata.EPISODE_PREFIX}),
    ElementEntry('X', set(), regex_dict={r"(\d+)([\W_])?(X)([\W_])?(\d+)": {
        1: {Metadata.SEQUENCE_NUMBER},
        2: {Metadata.DELIMITER},
        3: {Metadata.EPISODE_PREFIX},
        4: {Metadata.DELIMITER},
        5: {Metadata.SEQUENCE_NUMBER}
    }})
]
