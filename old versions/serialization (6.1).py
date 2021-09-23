# {str: int / str}
# {"12345": 26}
# {"12345": "main state}

# def dump | load

# 12335: str:26
# 12335: int:26
# 12335: str:main_state
import json


def dumps(d):
    result = ''
    for key, value in d.items():
        type_ = type(value).__name__
        result += '{key}:{type_}:{value}\n'.format(key=key, type_=type_, value=value)
    return result


# print(type("26"))  # <class 'str'>
# print(type("26").__name__)  # str !!!

dumped = dumps({'a': 24, 'c': '25', 'b': 'aaabc'})
# print(dumped)

TYPES = {
    'str': str,
    'int': int,
}


def loads(s):
    result = {}
    s = s.strip()
    for line in s.split('\n'):
        key, raw_type, raw_value = line.split(':')
        type_class = TYPES[raw_type]
        value = type_class(raw_value)
        result[key] = value
    return result


# print(loads(dumped))

# import json

# print('json')
dumped_json = json.dumps({
    'a': 'a',
    1: 2,
    'b': True,
    'c': False,
    'd': None,
    'e': 5.6,
    'f': [{}]
}, indent=4)
print(dumped_json)
json.loads(dumped_json)
# print(json.dumps({'a': 24, 'c': '25', 'b': 'aaabc'}))

import pickle

dumped_ = pickle.dumps({
    'a': 'a',
    1: 2,
    'b': True,
    'c': False,
    'd': None,
    'e': 5.6,
    'f': [{}]
})

# print(pickle.loads(dumped_))

print(pickle.dumps(loads))

dumped_a = pickle.dumps('a')

loaded_a = pickle.loads(dumped_a)


