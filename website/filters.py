# -*- coding: utf-8 -*-


def feelings_filter(args, feelings):
    feelings_query_list = []
    for feeling in args.getlist('feeling'):
        feelings_query_list.append(feeling)
    return feelings_query_list


def states_filter(args, states_unique):
    states_query_list = []
    for state in args.getlist('state'):
        state_full_name = states_unique[[x[0] for x in states_unique].index(state)][1]
        states_query_list.append(state_full_name)
    return states_query_list


def request_args_filter(request_args, feelings, states_unique):
    query_dict = {}
    if 'feeling' in request_args:
        query_dict['feelings'] = {
            '$in': feelings_filter(request_args, feelings)
        }
        query_dict['feelings_size'] = 1
    if 'state' in request_args:
        query_dict['location.state'] = {'$in': states_filter(request_args, states_unique)}
    return query_dict