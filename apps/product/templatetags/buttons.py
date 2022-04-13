#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from django import template
from apps.product.models import ProductVoteUser

register = template.Library()


@register.inclusion_tag("tags/vote_button.html", takes_context=True)
def vote_button(context, product):
    user = context['user']
    is_voted = False
    if user.is_authenticated:
        is_voted = ProductVoteUser.voted(user, product)
    res = {
        "voted": is_voted,
        "pid": product.pid,
        "vote_count": product.vote_count
    }
    return res
