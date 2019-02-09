# bencoding
# http://www.bittorrent.org/beps/bep_0003.html

"""
Strings are length-prefixed base ten followed by a colon and the string.
For example 4:spam corresponds to 'spam'.

>>> encode(b'spam')
b'4:spam'

Integers are represented by an 'i' followed by the number in base 10 followed by an 'e'.
For example i3e corresponds to 3 and i-3e corresponds to -3.
Integers have no size limitation. i-0e is invalid.
All encodings with a leading zero, such as i03e, are invalid,
other than i0e, which of course corresponds to 0.

    >>> decode(b'i3e')
    3
    >>> decode(b'i-3e')
    -3

    >>> decode(b'i0e')
    0
    >>> decode(b'i03e')
Traceback (most recent call last):
  ...
ValueError: invalid literal for int() with base 0: '03'


Lists are encoded as an 'l' followed by their elements (also bencoded) followed by an 'e'.
For example l4:spam4:eggse corresponds to ['spam', 'eggs'].

>>> decode(b'l4:spam4:eggse')
[b'spam', b'eggs']

Dictionaries are encoded as a 'd' followed by a list of alternating keys
and their corresponding values followed by an 'e'.
For example, d3:cow3:moo4:spam4:eggse corresponds to {'cow': 'moo', 'spam': 'eggs'}
Keys must be strings and appear in sorted order (sorted as raw strings, not alphanumerics).

>>> decode(b'd3:cow3:moo4:spam4:eggse')
OrderedDict([(b'cow', b'moo'), (b'spam', b'eggs')])

"""

import re, string


# coding_object_types = {
#     ':':encode.strings,
#     'i':encode.integers,
#     'l':encode.lists,
#     'd':encode.dicts
#                       }


def encode(data):
    # encoded = ""
    # def strings_encode(val):
    #     prefix = str(len(val))
    #     return encoded = encoded + prefix + ':' + str(val)
    # return strings_encode(val)
    if type(data) == int:
        return b'i' + str(data).encode() + b'e'
    elif type(data) == str:
        data = data.encode()
        return str(len(data)).encode() + b':' + data
    elif type(data) == list:
        return list_encode(data, b'l')
    elif type(data) == dict:
        return dict_encode(data)
    elif type(data) == bytes:
        return str(len(data)).encode() + b':' + data
    else:
        raise TypeError('Ошибка при обработке: тип данных не соответствует требованиям')


def list_encode(data, characters):
    result = characters
    for i in data:
        result += encode(i)
    return result + b'e'


def dict_encode(data):
    result = []
    for key, value in data.items():
        result.append(key)
        result.append(value)
    return list_encode(result, b'd')


def decode(data):
    # decoded  = ""
    # def strings_decode():
    #     for i in val:
    #         if val[i] == ':':
    #             pre_obj = i
    #             obj_lenght = val[i-1]
    #     for i in range(pre_obj + 1, pre_obj + 1 + obj_lenght):
    #         decoded = decoded + str(val[i])
    def decode_record(data):
        if data.startswith(b'i'):
            stash = re.match(b'i(-?\d+)e', data)
            return int(stash.group(1)), data[stash.span()[1]:]
        elif data.startswith(b'l') or data.startswith(b'd'):
            result = []
            data_rest = data[1:]
            while not data_rest.startswith(b'e'):
                element, data_rest = decode_record(data_rest)
                result.append(element)
            data_rest = data_rest[1:]
            if data.startswith(b'l'):
                return result, data_rest
            else:
                return {i: j for i, j in zip(result[::2], result[1::2])}, data_rest
        elif (data.startswith(i.encode()) for i in string.digits):
            m = re.match(b'(\d+):', data)
            lenght = int(m.group(1))
            i_rest = m.span()[1]
            starts_with = i_rest
            ends_with = i_rest + lenght
            return data[starts_with:ends_with], data[ends_with:]
        else:
            raise TypeError('Ошибка при обработке: тип данных не соответствует требованиям')

    if isinstance(data, str):
        data = data.encode()

    alpha_value, beta_value = decode_record(data)
    if beta_value:
        raise TypeError('Ошибка при обработке: тип данных не соответствует требованиям')
    return alpha_value
