# -*- coding: utf-8 -*-
import os
import unittest
import datetime as dt

from treeage.core import path_depth, abbr_date


def test_path_depth():
    res = path_depth("/root", "/root/1/2")
    assert res == 2


def test_abbr_date():
    a_month_ago = dt.datetime.now() - dt.timedelta(days=31)
    assert abbr_date(a_month_ago) == "1 mon"
