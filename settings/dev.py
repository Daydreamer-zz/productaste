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
        'HOST': '172.31.85.114',
        'port': 3306,
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}