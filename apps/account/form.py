#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()