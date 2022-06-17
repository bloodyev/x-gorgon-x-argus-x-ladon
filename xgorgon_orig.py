from hashlib import md5
from time import time


def hex_string(num):
    tmp_string = hex(num)[2:]
    if len(tmp_string) < 2:
        tmp_string = '0' + tmp_string
    return tmp_string


def reverse(num):
    tmp_string = hex_string(num)
    return int(tmp_string[1:] + tmp_string[:1], 16)


def RBIT(num):
    result = ''
    tmp_string = bin(num)[2:]
    while len(tmp_string) < 8:
        tmp_string = '0' + tmp_string
    for i in range(0, 8):
        result = result + tmp_string[7 - i]
    return int(result, 2)


def X_Gorgon(url, data, cookie):
    gorgon = ''
    url_md5 = md5(bytearray(url, 'utf-8')).hexdigest()
    gorgon += url_md5
    if data:
        data_md5 = md5(bytearray(data, 'utf-8')).hexdigest()
        gorgon += data_md5
    else:
        gorgon += '00000000000000000000000000000000'
    if cookie:
        cookie_md5 = md5(bytearray(cookie, 'utf-8')).hexdigest()
        gorgon += cookie_md5
    else:
        gorgon += '00000000000000000000000000000000'
    gorgon += '00000000000000000000000000000000'
    return calc_xg(gorgon)


def calc_xg(data):
    ts = int(time())
    len = 0x14
    key = [0xDF, 0x77, 0xB9, 0x40, 0xb9, 0x9b, 0x84, 0x83, 0xd1, 0xb9, 0xcb, 0xd1, 0xf7, 0xc2, 0xb9, 0x85, 0xc3, 0xd0,
           0xfb, 0xc3]
    param_list = []
    for i in range(0, 12, 4):
        temp = data[8 * i: 8 * (i + 1)]
        for j in range(4):
            H = int(temp[j * 2:(j + 1) * 2], 16)
            param_list.append(H)
    param_list.extend([0x0, 0x6, 0xB, 0x1C])
    H = int(hex(ts), 16)
    param_list.append((H & 0xFF000000) >> 24)
    param_list.append((H & 0x00FF0000) >> 16)
    param_list.append((H & 0x0000FF00) >> 8)
    param_list.append((H & 0x000000FF) >> 0)
    eor_result_list = []
    for A, B in zip(param_list, key):
        eor_result_list.append(A ^ B)
    for i in range(len):
        C = reverse(eor_result_list[i])
        D = eor_result_list[(i + 1) % len]
        E = C ^ D
        F = RBIT(E)
        H = ((F ^ 0xFFFFFFFF) ^ len) & 0xFF
        eor_result_list[i] = H
    result = ''
    for param in eor_result_list:
        result += hex_string(param)
    xgorgon = '0408b0d30000' + result
    return {'X-Gorgon': xgorgon, 'X-Khronos': str(ts)}
