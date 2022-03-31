#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import hashids


def make_hashid(id, length=6):
    KEY = "this is a key"
    hasher = hashids.Hashids(salt=KEY, min_length=length)
    return hasher.encode(id)
