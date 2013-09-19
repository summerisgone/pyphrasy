# coding: utf8
from operator import attrgetter
import argparse
import logging

import pymorphy2
CASE_CHOICES = ('nomn', 'gent', 'datv', 'accs', 'ablt', 'loct', 'voct', 'gen2', 'acc2', 'loc2')

LOGGING_LEVELS = {
    0: logging.ERROR,
    1: logging.INFO,
    2: logging.DEBUG
}
logger = logging.getLogger()
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO


class InflectionError(Exception):
    pass


class PhraseInflector(object):

    class ScoreHelper(object):
        score = 0

        def __init__(self, parsed):
            self.parsed = parsed

    def __init__(self, morph):
        self.morph = morph

    def parse_first(self, word):
        parse = self.morph.parse(word)
        if len(parse) > 0:
            return parse[0]
        else:
            return None

    def select_master(self, phrase):
        versions = []
        for i, word in enumerate(phrase):
            for j, parsed in enumerate(self.morph.parse(word)):
                if {'NOUN', 'nomn'} in parsed.tag:
                    version = self.ScoreHelper(parsed)
                    version.score = 100 / (2.0 * j + 1) + 100 / (1.0 * i + 1)
                    versions.append(version)
        if versions:
            return sorted(versions, key=attrgetter('score'), reverse=True)[0]
        else:
            return None

    def inflect(self, phrase, case):
        # phrase = phrase.lower()
        master_word = self.select_master(phrase.lower().split(' '))
        if master_word:
            return self._inflect_with_master(case, phrase, master_word.parsed)
        else:
            logger.error(u'Can not find master word in: {0}'.format(phrase))
            return self._inflect_without_master(case, phrase)

    def _inflect_with_master(self, case, phrase, master_word):
        result = []
        for chunk in phrase.split(' '):
            parsed_chunk = self.morph.parse(chunk)
            if chunk.lower() == master_word.word.lower():
                infl = {case}
                inflected = master_word.inflect(infl)
                if inflected:
                    result.append(inflected.word)
                else:
                    logger.error(u'Can not inflect word {1}: {0}'.format(phrase, chunk))
                    result.append(chunk)
                continue

            dependent = None
            for version in parsed_chunk:
                if version.tag.POS in (u'ADJF', u'PRTF') and version.tag.case == master_word.tag.case:
                    infl = {case, master_word.tag.number}
                    if master_word.tag.number == 'sing':
                        infl.add(master_word.tag.gender)
                    else:
                        infl.add(master_word.tag.number)

                    if case == u'accs' and (master_word.tag.gender == u'masc' or master_word.tag.number == u'plur'):
                        infl.add(master_word.tag.animacy)

                    try:
                        inflected = version.inflect(infl)
                    except ValueError,e:
                        logger.error(u'{0} at {1}'.format(e, version.word))
                        dependent = version
                    else:
                        if inflected:
                            dependent = inflected
                        else:
                            logger.error(u'Can not inflect word {1}: {0}'.format(phrase, version.word))
                            dependent = version
                    break

            if dependent:
                result.append(dependent.word)
            else:
                result.append(chunk)

        return u' '.join(result)

    def _inflect_without_master(self, case, phrase):
        result = []
        for chunk in phrase.split(' '):
            parsed = self.parse_first(chunk)
            if parsed:
                if any(map(lambda x: x in parsed.tag, ({'NOUN', 'nomn'}, {'ADJF', 'nomn'}))):
                    infl = {case}
                    if case == u'accs':
                        infl.add('inan')
                    try:
                        inflected = parsed.inflect(infl)
                        if inflected:
                            result.append(inflected.word)
                        else:
                            logger.error(u'Can not inflect word {1}: {0}'.format(phrase, chunk))
                            result.append(chunk)
                    except ValueError:
                        result.append(chunk)
                else:
                    result.append(chunk)
            else:
                result.append(chunk)

        return u' '.join(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Inflect input phrase')
    parser.add_argument('word', help='Phrase to inflect')
    parser.add_argument('case', help='case from https://pymorphy2.readthedocs.org/en/latest/user/grammemes.html',
                        choices=CASE_CHOICES)
    parser.add_argument('-v', '--verbose', type=int, required=False, default=0, choices=LOGGING_LEVELS)
    args = parser.parse_args()
    logging.basicConfig(format='%(levelname)s: %(message)s', level=LOGGING_LEVELS[args.verbose])

    morph = pymorphy2.MorphAnalyzer()
    inflector = PhraseInflector(morph)
    print inflector.inflect(args.word.decode('utf8'), args.case)
