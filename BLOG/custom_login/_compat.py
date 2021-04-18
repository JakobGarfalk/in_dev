# -*- coding: utf-8 -*-
'''
    flask_login._compat
    -------------------
    A module providing tools for cross-version compatibility.
'''


import sys


#PY2 = sys.version_info[0] == 2


#if not PY2:  # pragma: no cover
unicode = str  # needed for pyflakes in py3


#if PY2:  # pragma: nocover

print ("You are shit out of luck friend, PY2 compability denied! \nUSE PY3")

#else:  # pragma: nocover

from urllib.parse import urlparse, urlunparse

def iteritems(d):
    return iter(d.items())

def itervalues(d):
    return iter(d.values())

text_type = str


__all__ = [
    'unicode',
    'urlparse',
    'urlunparse',
    'iteritems',
    'itervalues',
    'text_type',
]
