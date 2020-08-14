# -*- coding: utf-8 -*-

class NewPageElement(Exception):

    def __init__(self):
        super().__init__('new element error')

class MobilePage(Exception):

    def __init__(self):
        super().__init__('mobile page error')


class TooManyRequest(Exception):

    def __init__(self):
        super().__init__('too many request error')