#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'productaste',
        'USER': 'root',
        'PASSWORD': "199747",
        'HOST': '192.168.2.10',
        'port': 3306,
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}