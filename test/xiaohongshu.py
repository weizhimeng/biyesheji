# from tools.myrequests import _requests as request
# from tools.myrequests import Headers as headers
# import json
# from pyquery import PyQuery
# import time
# import queue
# import threading
# import logging
# from lxml import html
# import re
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# import time

# ticks = time.time()
# new_ticks = str(ticks).replace('.', '')[:-4]
#
#
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# user_ag = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Mobile Safari/537.36'
# chrome_options.add_argument('user-agent=%s'%user_ag)
#
# driver = webdriver.Chrome(executable_path='./chromedriver')
#
# driver.get('https://www.xiaohongshu.com/user/profile/5b40260e11be107fe355ff63?')
# cookie=driver.get_cookies()
# print(cookie)
# # cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
# xhsTrackerId = cookie[-1]['value']
#
# driver.close()
# exit()
# cookie = 'xhsTrackerId={};timestamp2={}e576c1de432564b7'.format(xhsTrackerId,new_ticks)
# print(cookie)
import requests
xhsTrackerId = '2c119bde-c49b-4da6-cd32-305109bb006d'
new_ticks = '1597047090670'
headers = {
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Mobile Safari/537.36',
    'cookie': 'xhsTrackerId={};timestamp2={}e576c1de432564b7'.format(xhsTrackerId,new_ticks)
    # 'cookie':';'.join(cookie)
}
url = 'https://www.xiaohongshu.com/user/profile/5b40260e11be107fe355ff63?'
response = requests.get(url, headers=headers)
# print(response.cookies)
print(response.text)

# import requests
# url = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=6854031033118002445&dytk='
# response = requests.get(url, headers=headers)
# print(response.text)