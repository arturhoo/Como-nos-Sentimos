# -*- coding: utf-8 -*-
from unittest import TestCase, main as unittestMain
from sentiment_filter import identify_feelings


class TestSentimentFilter(TestCase):
    file_name = 'feelings.txt'

    def testCase(self):
        lower_case = identify_feelings(self.file_name, 'cansado')
        mixed_case = identify_feelings(self.file_name, 'cAnsADo')
        self.assertEqual(lower_case, mixed_case)

    def testUnicode(self):
        text = u'estou confortável'.encode('utf-8')
        result = identify_feelings(self.file_name, text)
        self.assertIn(u'confortável'.encode('utf-8'), result)

    def testFeelingBeginningOfString(self):
        text = u'cansado estou'
        result = identify_feelings(self.file_name, text)
        self.assertIn(u'cansado', result)

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
