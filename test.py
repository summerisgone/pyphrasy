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
            self.assertEqual(parsed.parsed.word, master_word,
                             u'{0} instead {1}'.format(parsed.parsed.word, master_word))

    def test_inflection_with_master_genitive(self):
        phrases = (
            (u'взбитые сливки', u'взбитых сливок'),
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
            self.assertEqual(genitive, result)


    def test_inflection_with_master_accusative(self):
        phrases = (
            (u'взбитые сливки', u'взбитые сливки'),
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
            self.assertEqual(accusative, result)

    def test_inflection_with_master_singular(self):
        phrases = (
            (u'взбитые сливки', u'взбитые сливки'),
            (u'шары для боулинга', u'шар для боулинга'),
            (u'красные шары для боулинга', u'красный шар для боулинга'),
            (u'красные шары', u'красный шар'),
            (u'красные ленты', u'красная лента'),
            (u'кирпичи керамические лицевые полнотелые одинарные велюровые 1НФ М150',
             u'кирпич керамический лицевой полнотелый одинарный велюровый 1НФ М150'),
            (u'трубы стальные профильные электросварные', u'труба стальная профильная электросварная'),
            (u'плиты для стальных перекрытий бетонные', u'плита для стальных перекрытий бетонная'),
            (u'мои прекрасные няни', u'моя прекрасная няня'),
            (u'полные штаны', u'полные штаны'),
            (u'бедные люди', u'бедный человек'),
        )
        for phrase, result in phrases:
            master = self.inflector.select_master(phrase.split(' '))
            sing = self.inflector._inflect_with_master('sing', phrase, master.parsed)
            self.assertEqual(sing, result)

    def test_inflection_with_master_plural(self):
        phrases = (
            (u'взбитые сливки', u'взбитые сливки'),
            (u'шар для боулинга', u'шары для боулинга'),
            (u'красный шар для боулинга', u'красные шары для боулинга'),
            (u'красный шар', u'красные шары'),
            (u'красная лента', u'красные ленты'),
            (u'кирпич керамический лицевой полнотелый одинарный велюровый 1НФ М150',
             u'кирпичи керамические лицевые полнотелые одинарные велюровые 1НФ М150'),
            (u'труба стальная профильная электросварная', u'трубы стальные профильные электросварные'),
            (u'плита для стальных перекрытий бетонная', u'плиты для стальных перекрытий бетонные'),
            (u'моя прекрасная няня', u'мои прекрасные няни'),
            (u'полные штаны', u'полные штаны'),
            (u'бедные люди', u'бедные люди'),
        )
        for phrase, result in phrases:
            master = self.inflector.select_master(phrase.split(' '))
            plur = self.inflector._inflect_with_master('plur', phrase, master.parsed)
            self.assertEqual(plur, result)


if __name__ == '__main__':
    unittest.main()
