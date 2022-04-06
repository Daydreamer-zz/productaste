#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from datetime import datetime
from datetime import timedelta
from django.utils import dateparse


def form_date(delta):
    return datetime.today() - timedelta(delta)


def str2date(date, format="%Y-%m-%d"):
    return datetime.strptime(date, format).date()


def iso8601_to_datetime(iso8601_utc):
    date_utc = dateparse.parse_datetime(iso8601_utc)
    timestamp_utc = date_utc.timestamp()
    date_now = datetime.fromtimestamp(timestamp_utc)
    return date_now
