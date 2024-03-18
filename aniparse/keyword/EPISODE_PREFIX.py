from aniparse.token_tags import Descriptor
from aniparse.abstraction.KeywordBase import ElementEntry

episode_prefix = [
    ElementEntry('EP', {Descriptor.EPISODE}, regex_dict={r'EP\.?': {0: {Descriptor.EPISODE}}}),
    ElementEntry('EPS', {Descriptor.EPISODE},
                 regex_dict={r'EPS\.?': {0: {Descriptor.EPISODE}}}),
    ElementEntry('EPISODE', {Descriptor.EPISODE},
                 regex_dict={r'EPISODE\.?': {0: {Descriptor.EPISODE}}}),
    ElementEntry('EPISODES', {Descriptor.EPISODE},
                 regex_dict={r'EPISODES\.?': {0: {Descriptor.EPISODE}}}),
    ElementEntry('CAPITULO', {Descriptor.EPISODE}),
    ElementEntry('EPISODIO', {Descriptor.EPISODE}),
    ElementEntry('FOLGE', {Descriptor.EPISODE}),
    ElementEntry('E', {Descriptor.EPISODE}),
    ElementEntry('X', set(), regex_dict={r"(\d+)([\W_])?(X)([\W_])?(\d+)": {
        1: {Descriptor.SEQUENCE_NUMBER},
        2: {Descriptor.DELIMITER},
        3: {Descriptor.EPISODE},
        4: {Descriptor.DELIMITER},
        5: {Descriptor.SEQUENCE_NUMBER}
    }})
]
