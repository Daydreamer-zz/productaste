#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from datetime import datetime
from datetime import timedelta


def form_date(delta):
    return datetime.today() - timedelta(delta)


def str2date(date, format="%Y-%m-%d"):
    return datetime.strptime(date, format).date()