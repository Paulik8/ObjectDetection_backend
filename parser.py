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
    # size = len(find(str(data), '=').result())
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
    # size = len(find(str(data), '=').result())
    data_str = str(data)[2:-1].split(':')
    nickname = data_str[0]
    password = data_str[1]
    list = [nickname, password]
    return list


@gen.coroutine
def find(str, ch):
    app = []
    for i, ltr in enumerate(str):
        if ltr == ch:
            app.append(i)
    return app


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
    if len(arr) > 0:
        for el_dict in arr:
            el = el_dict['id']
            if valid_arr[el - 1] == 0:
                valid_arr[el - 1] = 1

        for index, res_el in enumerate(valid_arr):
            if index == 0 and res_el == 1:
                res_arr.append(1)
            if index == 1 and res_el == 1:
                res_arr.append(2)
    return res_arr


@gen.coroutine
def tag_to_id_parse(arr):

    valid_arr = [0, 0]
    res_arr = []

    if '_' in arr:
        ready_arr = arr.split('_')
    else:
        ready_arr = arr

    for i in ready_arr:
        if 'cat' == i or 'cats' == i:
            valid_arr[0] = 1
        if 'dog' == i or 'dogs' == i:
            valid_arr[1] = 1

    for index, res_el in enumerate(valid_arr):
        if index == 0 and res_el == 1:
            res_arr.append(1)
        if index == 1 and res_el == 1:
            res_arr.append(2)
    return res_arr



# @gen.coroutine
# def request_tags_parse(str):
#     arr = str.split('_')



# res = get_tag2('17.jpg')
# print (res)
# data = base64.b64decode('dXM6dXM=')
# size = len(find('dXM6dXM=', '=').result())
# data_str = str(data)[size:-1].split(':')
# print(data_str)
