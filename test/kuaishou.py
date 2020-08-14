from tools.myrequests import _requests as request
from tools.myrequests import Headers as headers
import json
from pyquery import PyQuery
import time
import queue
import threading
import logging
from lxml import html
import re


url = 'https://v.kuaishou.com/8ZIJa7'
response = request.get(url, headers=headers)
like = html.etree.HTML(response.text).xpath('//div[@class="profile-user-count-info"]//span[@class="like-count"]//text()')
comment = html.etree.HTML(response.text).xpath('//div[@class="profile-user-count-info"]//span[@class="comment-count"]//text()')
co = html.etree.HTML(response.text).xpath('//div[@class="comment-header"]//text()')
print(like)
print(comment)
print(co)
# print(response.text)

pattern = re.compile(r'"displayView":(.*?),')
view = pattern.findall(response.text)
pattern = re.compile(r'"displayLike":(.*?),')
like = pattern.findall(response.text)
pattern = re.compile(r'"displayComment":(.*?),')
comment = pattern.findall(response.text)
print(view)
print(like)
print(comment)

# headers = {
#     'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Mobile Safari/537.36',
# }
# url = 'https://v.kuaishou.com/7Ml6h0'
# response = request.get(url, headers=headers)
# fans = html.etree.HTML(response.text).xpath('//div[@class="ribbon"]//text()')
# print(fans)

