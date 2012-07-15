# -*- coding: utf-8 -*-


def feelings_filter(args, feelings):
    feelings_query_list = []
    for feeling in args.getlist('feeling'):
        feelings_query_list.append(feeling)
    return feelings_query_list


def states_filter(args, states):
    states_query_list = []
    for state in args.getlist('state'):
        indexes_full_names = [i for i, v in enumerate(states) if v[0] == state]
        for index in indexes_full_names:
            state_full_name = states[index][1]
            states_query_list.append(state_full_name)
    return states_query_list


def request_args_filter(request_args, feelings, states):
    query_dict = {}
    if 'feeling' in request_args:
        query_dict['feelings'] = {
            '$in': feelings_filter(request_args, feelings)
        }
        query_dict['feelings_size'] = 1
    if 'state' in request_args:
        query_dict['location.state'] = {
            '$in': states_filter(request_args, states)
        }
    if 'location-only' in request_args:
        if request_args['location-only'].lower() == 'yes':
            query_dict['location'] = {'$exists': True}
    if 'weather-only' in request_args:
        if request_args['weather-only'].lower() == 'yes':
            query_dict['location.weather'] = {'$exists': True}
    return query_dict
