#-*- coding: utf-8 -*-
from __future__ import absolute_import

try:
    from .local import *
except ImportError:
    raise RuntimeError("local settings file not found")
