# -*- coding: utf-8 -*-


def load_query_terms(file_name):
    query_list = []
    with open(file_name) as f:
        for line in f.readlines():
            query_list.append(line.rstrip())

    return query_list
