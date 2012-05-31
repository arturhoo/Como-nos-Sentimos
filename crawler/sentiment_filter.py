# -*- coding: utf-8 -*-
import re


def load_feelings(file_name):
    feelings_dic = {}
    with open(file_name) as f:
        for line in f.readlines():
            line_list = line.split(';')
            item_dic = {'re': line_list[1],
                        'color': line_list[2]}
            feelings_dic[line_list[0]] = item_dic

    return feelings_dic


def identify_feeling(file_name, text):
    feelings = []
    feelings_dic = load_feelings(file_name)
    for (feeling, feeling_dic) in feelings_dic.items():
        regex = re.compile(r'.* ' + feeling_dic['re'] + r'.*', re.IGNORECASE)
        if regex.match(text):
            feelings.append(feeling)
    return feelings

if __name__ == '__main__':
    f = identify_feeling('feelings.txt', 'estou muito cansado')
    if f:
        print f
