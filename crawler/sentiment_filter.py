# -*- coding: utf-8 -*-
import re
from utils import load_query_terms, remove_accents


def load_feelings(file_name):
    feelings_dic = {}
    with open(file_name) as f:
        for line in f.readlines():
            line_list = line.split(';')
            item_dic = {'re': line_list[1],
                        'color': line_list[2]}
            feelings_dic[line_list[0]] = item_dic

    return feelings_dic


def identify_feelings(file_name, text):
    clean_text = remove_accents(text)
    feelings = []
    feelings_dic = load_feelings(file_name)
    query_list = load_query_terms('query_terms.txt')
    regex_query_string = '('
    for (idx, query) in enumerate(query_list):
        regex_query_string += query
        if idx + 1 != len(query_list):
            regex_query_string += '|'
    regex_query_string += ')'

    for (feeling, feeling_dic) in feelings_dic.items():
        regex = re.compile(r'(^|(?!RT).* )' + \
                           regex_query_string + \
                           r'.* ' + \
                           feeling_dic['re'] + \
                           r'.*', re.UNICODE | re.IGNORECASE)
        if regex.match(clean_text):
            feelings.append(feeling)
    return feelings

if __name__ == '__main__':
    f = identify_feelings('feelings.txt', u'eu tô muito cansado'.encode('utf-8'))
    if f:
        print f
