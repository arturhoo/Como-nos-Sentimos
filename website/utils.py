# -*- coding: utf-8 -*-
from htmlentitydefs import name2codepoint
from re import sub
from unicodedata import normalize, combining


def remove_accents(input_str):
    nkfd_form = normalize('NFKD', unicode(input_str))
    return u"".join([c for c in nkfd_form if not combining(c)])


def unescape(text):
    '''Removes HTML or XML character references and entities from a text string.
    @param text The HTML (or XML) source text.
    @return The plain text, as a Unicode string, if necessary.
    Author: Fredrik Lundh
    Source: http://effbot.org/zone/re-sub.htm#unescape-html
    '''
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # leave as is
    return sub("&#?\w+;", fixup, text)


def prepare_string_for_javascript(string):
    new_string = string.replace('\n', '')
    new_string = new_string.replace('\\', '\\\\')
    new_string = unescape(new_string)
    return new_string


def rgb_to_html_color(rgb_tuple):
    """convert an (R, G, B) tuple to #RRGGBB
    Source: http://code.activestate.com/recipes/266466/
    """
    hexcolor = '#%02x%02x%02x' % rgb_tuple
    # that's it! '%02x' means zero-padded, 2-digit hex values
    return hexcolor


def get_feeling_color(feeling, feelings_list):
    index = [x[0] for x in feelings_list].index(feeling)
    rgb_string = feelings_list[index][1]
    rgb_tuple = (int(rgb_string.split(',')[0]), \
                 int(rgb_string.split(',')[1]), \
                 int(rgb_string.split(',')[2]))
    return rgb_to_html_color(rgb_tuple)
