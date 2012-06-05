# -*- coding: utf-8 -*-
import unicodedata


def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])


def load_query_terms(file_name):
    query_list = []
    with open(file_name) as f:
        for line in f.readlines():
            query_list.append(line.rstrip())

    return query_list
