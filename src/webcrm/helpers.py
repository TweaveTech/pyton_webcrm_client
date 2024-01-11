from collections import namedtuple
from copy import deepcopy
import re

snake_case_regex = re.compile(r'(?<!^)(?=[A-Z])')


def snake_case(s):
    return snake_case_regex.sub('_', s).lower()


def camelcase(s):
    s = s.replace('_', ' ')
    return ''.join(word.title() for word in s.split())


def convert_dict_to_namedtuple(base_name, d):
    snake_name_keys = [snake_case(k) for k in d.keys()]
    nt = namedtuple(camelcase(base_name), snake_name_keys)
    return_d = {}

    for k, v in deepcopy(d).items():
        if isinstance(v, dict):
            v = convert_dict_to_namedtuple(camelcase(k), v)
        elif isinstance(v, list | set | tuple):
            v = [convert_dict_to_namedtuple(camelcase(k),i) for i in v]
        
        return_d[snake_case(k)] = v

    return nt(**return_d)