# -*- coding: utf-8 -*-
import re
from utils import load_terms, remove_accents


def load_feelings(file_name):
    feelings_dic = {}
    with open(file_name) as f:
        for line in f.readlines():
            line_list = line.split(';')
            item_dic = {'re': line_list[1],
                        'color': line_list[2]}
            feelings_dic[line_list[0]] = item_dic

    return feelings_dic


def make_regex_groups(query_list):
    regex_group = '('
    for (idx, query) in enumerate(query_list):
        regex_group += query
        if idx + 1 != len(query_list):
            regex_group += '|'
    regex_group += ')'
    return regex_group


def make_negative_regex_groups(query_list):
    negative_regex_group = '('
    for (idx, query) in enumerate(query_list):
        negative_regex_group += '(?<!' + query + ' )'
    negative_regex_group += ')'
    return negative_regex_group


def identify_feelings(file_name, text):
    clean_text = remove_accents(text)
    feelings = []
    feelings_dic = load_feelings(file_name)
    query_list = load_terms('query_terms.txt')
    pre_negation_terms = load_terms('pre_negation_terms.txt')
    post_negation_terms = load_terms('post_negation_terms.txt')
    regex_query_group = make_regex_groups(query_list)
    regex_pre_negation = make_negative_regex_groups(pre_negation_terms)
    regex_post_negation = make_negative_regex_groups(post_negation_terms)

    for (feeling, feeling_dic) in feelings_dic.items():
        regex_string = r'(^|(?!RT).* )' + \
                       regex_pre_negation + \
                       regex_query_group + \
                       r'.* ' + \
                       regex_post_negation + \
                       feeling_dic['re'] + \
                       r'.*'
        regex = re.compile(regex_string, re.UNICODE | re.IGNORECASE)
        if regex.match(clean_text):
            feelings.append(feeling)
    return feelings

if __name__ == '__main__':
    f = identify_feelings('feelings.txt', u'eu tô muito cansado')
    if f:
        print f
