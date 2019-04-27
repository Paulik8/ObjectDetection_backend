import base64
from tornado import gen


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
