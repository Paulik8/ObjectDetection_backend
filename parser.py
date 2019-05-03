import base64
from tornado import gen
from get_tag2 import get_tag2


@gen.coroutine
def auth_parse(req):
    header = yield header_parse(req.request.headers.get('Authorization'))
    if header is None:
        return
    age = req.get_argument('age')
    data = base64.b64decode(header)
    data_str = str(data)[2:-1].split(':')
    nickname = data_str[0]
    password = data_str[1]
    list = [nickname, password, age]
    return list

@gen.coroutine
def common_parse(req):
    header = yield header_parse(req.request.headers.get('Authorization'))
    if header is None:
        return
    data = base64.b64decode(header)
    data_str = str(data)[2:-1].split(':')
    nickname = data_str[0]
    password = data_str[1]
    list = [nickname, password]
    return list


@gen.coroutine
def header_parse(str):
    if str is None:
        return
    code = str.split(' ')[1]
    return code

@gen.coroutine
def tags_parse(arr):
    valid_arr = [0, 0]
    res_arr = []
    if arr.len() > 0:
        for el_dict in arr:
            el = el_dict['id']
            if valid_arr[el - 1] == 0:
                valid_arr[el - 1] = 1

        for index, res_el in enumerate(valid_arr):
            if index == 0 and res_el == 1:
                res_arr.extend(['cat', 'cats'])
            if index == 1 and res_el == 1:
                res_arr.extend(['dog', 'dogs'])
    return res_arr

# res = get_tag2('dog.jpg')
# print (res)