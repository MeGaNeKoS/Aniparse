from aniparse.core.token_tags import Tag
from aniparse.abstraction.keyword_base import ElementEntry

episode_prefix = [
    ElementEntry(word='EP', categories={Tag.EPISODE}, regex_dict={
        r'EP\.?': {0: {Tag.EPISODE}}
    }),
    ElementEntry(word='EPS', categories={Tag.EPISODE}, regex_dict={
        r'EPS\.?': {0: {Tag.EPISODE}}
    }),
    ElementEntry(word='EPISODE', categories={Tag.EPISODE}, regex_dict={
        r'EPISODE\.?': {0: {Tag.EPISODE}}
    }),
    ElementEntry(word='EPISODES', categories={Tag.EPISODE}, regex_dict={
        r'EPISODES\.?': {0: {Tag.EPISODE}}
    }),
    ElementEntry(word='CAPITULO', categories={Tag.EPISODE}),
    ElementEntry(word='EPISODIO', categories={Tag.EPISODE}),
    ElementEntry(word='FOLGE', categories={Tag.EPISODE}),
    ElementEntry(word='E', categories={Tag.EPISODE}),
    ElementEntry(word='#', categories={Tag.EPISODE}),
    ElementEntry(word='X', categories=set(), regex_dict={
        r"(\d+)([\W_])?(X)([\W_])?(\d+)": {
            1: {Tag.SEQUENCE_NUMBER},
            2: {Tag.DELIMITER},
            3: {Tag.EPISODE},
            4: {Tag.DELIMITER},
            5: {Tag.SEQUENCE_NUMBER}
        }
    })
]
