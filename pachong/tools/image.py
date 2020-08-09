# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '.')
import os
import requests
import time
from PIL import Image
from tools.myrequests import _requests as requests


def get_img_size(img_url, type='kuaibao'):
    """Get a image width and height

    :return: a tuple of width, height
    """
    time.sleep(1)
    resp = requests.get(img_url)
    if type == 'kuaibao':
        # filename = 'qqkuaibao/imgTemp/' + img_url.split('/')[-2]
        filename = './imgTemp/' + img_url.split('/')[-2]
    elif type == 'toutiao':
        filename = 'todayHeadline/imgTemp/' + img_url.split('/')[-1]
        # filename = './imgTemp/' + img_url.split('/')[-1]
    elif type == 'qutoutiao':
        filename = 'todayHeadline/imgTemp/' + img_url.split('/')[-1]
        # filename = './imgTemp/' + img_url.split('/')[-1]

    with open(filename, 'wb') as f:
        f.write(resp.content)

    im = Image.open(filename)
    width, height = im.size

    # os.remove(filename)

    return width, height