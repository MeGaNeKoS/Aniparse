from aniparse.element import DescriptorType
from aniparse.abstraction.KeywordBase import ElementEntry

episode_prefix = [
    ElementEntry('EP', {DescriptorType.EPISODE_PREFIX}, regex_dict={r'EP\.?': {0: {DescriptorType.EPISODE_PREFIX}}}),
    ElementEntry('EPS', {DescriptorType.EPISODE_PREFIX},
                 regex_dict={r'EPS\.?': {0: {DescriptorType.EPISODE_PREFIX}}}),
    ElementEntry('EPISODE', {DescriptorType.EPISODE_PREFIX},
                 regex_dict={r'EPISODE\.?': {0: {DescriptorType.EPISODE_PREFIX}}}),
    ElementEntry('EPISODES', {DescriptorType.EPISODE_PREFIX},
                 regex_dict={r'EPISODES\.?': {0: {DescriptorType.EPISODE_PREFIX}}}),
    ElementEntry('CAPITULO', {DescriptorType.EPISODE_PREFIX}),
    ElementEntry('EPISODIO', {DescriptorType.EPISODE_PREFIX}),
    ElementEntry('FOLGE', {DescriptorType.EPISODE_PREFIX}),
    ElementEntry('E', {DescriptorType.EPISODE_PREFIX}),
    ElementEntry('X', set(), regex_dict={r"(\d+)([\W_])?(X)([\W_])?(\d+)": {
        1: {DescriptorType.SEASON_NUMBER},
        2: {DescriptorType.DELIMITER},
        3: {DescriptorType.EPISODE_PREFIX},
        4: {DescriptorType.DELIMITER},
        5: {DescriptorType.EPISODE_NUMBER}
    }})
]
