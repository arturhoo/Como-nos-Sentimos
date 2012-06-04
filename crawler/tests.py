# -*- coding: utf-8 -*-
from unittest import TestCase, main as unittestMain
from sentiment_filter import identify_feelings


class TestSentimentFilter(TestCase):
    file_name = 'feelings.txt'

    def testFeelingCase(self):
        lower_case = identify_feelings(self.file_name, 'estou cansado')
        mixed_case = identify_feelings(self.file_name, 'estou cAnsADo')
        self.assertEqual(lower_case, mixed_case)

    def testQueryCase(self):
        lower_case = identify_feelings(self.file_name, 'estou cansado')
        mixed_case = identify_feelings(self.file_name, 'eSToU cansado')
        self.assertEqual(lower_case, mixed_case)

    def testNoQuery(self):
        text = u'cansado'
        result = identify_feelings(self.file_name, text)
        self.assertNotIn(u'cansado', result)

    def testFeelingUnicode(self):
        text = u'estou confortável'.encode('utf-8')
        result = identify_feelings(self.file_name, text)
        self.assertIn(u'confortável'.encode('utf-8'), result)

    def testQueryUnicode(self):
        text = u'eu tô cansado'.encode('utf-8')
        result = identify_feelings(self.file_name, text)
        self.assertIn(u'cansado'.encode('utf-8'), result)

    def testQueryOrder(self):
        text = u'cansado estou'
        result = identify_feelings(self.file_name, text)
        self.assertNotIn(u'cansado', result)

    def testFeelingAsSubstring(self):
        text = u'estou esfomeado demais'
        result = identify_feelings(self.file_name, text)
        self.assertNotIn(u'fome', result)

    def testMultipleFeelings(self):
        text = 'estou muito cansada e feliz'
        result = identify_feelings(self.file_name, text)
        self.assertIn(u'feliz', result)
        self.assertIn(u'cansado', result)


if __name__ == '__main__':
    unittestMain()
