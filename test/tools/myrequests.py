# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '.')
import urllib3
from tools.user_agent import UserAgent
import requests

import lxml.html


etree = lxml.html.etree

ua = UserAgent()
Headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'User-Agent': ua.random(),
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}
urllib3.disable_warnings()


class myrequests():

    def get(self, url, params=None, **kwargs):
        """Send a GET request

        :param url: URL for get
        :param params: (optional) Dictionary, list of tuples or bytes to send
        :param kwargs: Optional arguments tha ``requests`` takes
        :return: Response
        """

        kwargs.setdefault('timeout', 15)
        kwargs.setdefault('verify', False)
        kwargs.setdefault('headers', Headers)
        kwargs.setdefault('allow_redirects', True)

        with requests.Session() as session:
            response = session.get(url, params=params, **kwargs)
            response.xpath = etree.HTML(response.text).xpath

            return response


    def post(self, url, data=None, json=None, **kwargs):
        """Send a POST request

        :param url: URL for post
        :param data: (optional) Dictionary, list of tuples,
            bytes, or file-like to send
        :param json: (optional) json data to send
        :param kwargs: Optional arguments tha ``requests`` takes
        :return: Response
        """
        kwargs.setdefault('timeout', 15)
        kwargs.setdefault('verify', False)
        kwargs.setdefault('headers', Headers)
        kwargs.setdefault('allow_redirects', True)

        with requests.Session() as session:
            response = session.post(url, data=data, json=json, **kwargs)
            response.xpath = etree.HTML(response.text).xpath

            return response



_requests = myrequests()