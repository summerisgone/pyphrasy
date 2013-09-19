# coding=utf8
import unittest
import pymorphy2
from inflect import PhraseInflector


class InflectTestSuite(unittest.TestCase):

    def setUp(self):
        self.inflector = PhraseInflector(pymorphy2.MorphAnalyzer())

    def test_select_master_word(self):
        phrases = (
            (u'шар для боулинга', u'шар'),
            (u'красный шар для боулинга', u'шар'),
            (u'красный шар', u'шар'),
            (u'красная лента', u'лента'),
            (u'Кирпич керамический лицевой полнотелый одинарный велюровый 1НФ М150', u'кирпич'),
            (u'Труба стальная профильная электросварная', u'труба'),
            (u'плита для стальных перекрытий бетонная', u'плита'),
            (u'полные штаны', u'штаны'),
        )
        for phrase, master_word in phrases:
            parsed = self.inflector.select_master(phrase.split(' '))
            self.assertEqual(parsed.parsed.word, master_word, u'{0} instead {1}'.format(parsed.parsed.word, master_word))

    def test_inflection_with_master_genitive(self):
        phrases = (
            (u'шар для боулинга', u'шара для боулинга'),
            (u'красный шар для боулинга', u'красного шара для боулинга'),
            (u'красный шар', u'красного шара'),
            (u'красная лента', u'красной ленты'),
            (u'кирпич керамический лицевой полнотелый одинарный велюровый 1НФ М150',
                u'кирпича керамического лицевого полнотелого одинарного велюрового 1НФ М150'),
            (u'труба стальная профильная электросварная', u'трубы стальной профильной электросварной'),
            (u'плита для стальных перекрытий бетонная', u'плиты для стальных перекрытий бетонной'),
            (u'полные штаны', u'полных штанов'),
            (u'бедные люди', u'бедных людей'),
            (u'стальные плиты', u'стальных плит'),
        )
        for phrase, result in phrases:
            master = self.inflector.select_master(phrase.split(' '))
            genitive = self.inflector._inflect_with_master('gent', phrase, master.parsed)
            print genitive
            self.assertEqual(genitive, result)


    def test_inflection_with_master_accusative(self):
        phrases = (
            (u'шар для боулинга', u'шар для боулинга'),
            (u'красный шар для боулинга', u'красный шар для боулинга'),
            (u'красный шар', u'красный шар'),
            (u'красная лента', u'красную ленту'),
            (u'кирпич керамический лицевой полнотелый одинарный велюровый 1НФ М150',
                u'кирпич керамический лицевой полнотелый одинарный велюровый 1НФ М150'),
            (u'труба стальная профильная электросварная', u'трубу стальную профильную электросварную'),
            (u'плита для стальных перекрытий бетонная', u'плиту для стальных перекрытий бетонную'),
            (u'моя прекрасная няня', u'мою прекрасную няню'),
            (u'полные штаны', u'полные штаны'),
            (u'бедные люди', u'бедных людей'),
        )
        for phrase, result in phrases:
            master = self.inflector.select_master(phrase.split(' '))
            accusative = self.inflector._inflect_with_master('accs', phrase, master.parsed)
            print accusative
            self.assertEqual(accusative, result)

if __name__ == '__main__':
    unittest.main()
