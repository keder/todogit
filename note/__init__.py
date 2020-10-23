#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import date


class Note:
    """Note implementation."""

    def __init__(self, user_id, text):
        self.user_id = user_id
        self.text = text
        self.date = str(date.today())

    def __str__(self):
        return "{date}\n{text}".format(date=self.date, text=self.text)
