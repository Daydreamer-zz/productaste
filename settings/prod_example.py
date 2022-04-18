#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'productaste',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4'
        }
    }
}
