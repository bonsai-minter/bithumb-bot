#!/usr/bin/env python3.6
import sys
from functools import partial
from time import gmtime, strftime
"""
Pretty Output
Aareon Sullivan - 2017
"""

color = {'red': '\033[31m',
         'yellow': '\033[33m',
         'green': '\033[32m',
         'cyan': '\033[36m',
         'magenta': '\033[35m',
         'black': '\033[30m',
         'reset': '\033[37m'}

reset = color.get('reset')

def _status(string, color_code, stat_msg, prn_out, time, space):
    message = _format(color_code, stat_msg, string, space)
    if time:
        stat_msg += '[' + strftime("%Y-%m-%d/%H:%M:%S", gmtime()) + ']'
        message = _format(color_code, stat_msg, string, space)
    if prn_out:
        print(message)
    return message

def _format(color_code, stat_msg, string, space):
    color_code = color.get(color_code)
    i = 30
    if not color_code:
        color_code = color.get('yellow')
        error_msg = ('Incorrect color option! A list of options are as follows: '
          + ', '.join(value + key + reset for key, value in color.items()))
        print(color_code + '[PRTTYERR]'.ljust(i) + '| ' + reset + error_msg)
    if not space:
        i = 10
    return color_code + stat_msg.ljust(i) + '| ' + reset + string

error = partial(_status, string='An error has ocurred!', color_code='red', stat_msg='[ERROR]', prn_out=True, time=False, space=False)
warning = partial(_status, string='Something is not right', color_code='yellow', stat_msg='[WARNING]', prn_out=True, time=False, space=False)
success = partial(_status, string='Great success!', color_code='green', stat_msg='[SUCCESS]', prn_out=True, time=False, space=False)
info = partial(_status, string='Information:', color_code='cyan', stat_msg='[INFO]', prn_out=True, time=False, space=False)
custom = partial(_status, string='Custom text', color_code='magenta', stat_msg='[CUSTOM]', prn_out=True, time=False, space=False)

def color_this(string, color_code):
    return color.get(color_code)+string+reset

def extend(tup, color_code='yellow', extens='>>>', prn_out=True):
    """Takes a tuple, returns a sub-message"""
    string = ''
    for item in tup:
        string += ' '+color_this(extens.ljust(14), color_code)+item+'\n'
    string = string[:-1]
    if prn_out:
        print(string)

def version(color_code='magenta', stat_msg='[PRTTYOUT]', string='Pretty Output version info:', prn_out: bool=True):
    version = {'python': str(sys.version_info[0]) + '.' + str(sys.version_info[1]),
               'output': '2.8.4'}

    pyver = color_this(version.get('python'), 'magenta')
    outver = color_this(version.get('output'), 'magenta')

    _status(string, color_code, stat_msg, prn_out)
    extend(('Python Version - ' + pyver, 'PreOut Version - ' + outver))

