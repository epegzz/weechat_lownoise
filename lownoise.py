# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 by epegzz <epegzz@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import re
import weechat
w = weechat

SCRIPT_NAME    = "lownoise"
SCRIPT_AUTHOR  = "epegzz <epegzz@gmail.com>"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "GPL"
SCRIPT_DESC    = "Less noise through join/leave messages."

print_debug = False

short = re.compile(r'%s[0-9]{2}' % '\x19' )
medium = re.compile(r'%sF[0-9]{2}' % '\x19' )
long = re.compile(r'%sF@[0-9]{5}' % '\x19' )
reset = re.compile(r'%s' % '\x1c' )

def strip_colors(input):
    input = short.sub('', input)
    input = medium.sub('', input)
    input = long.sub('', input)
    input = reset.sub('', input)
    return input


def debug(line):
    if print_debug:
        print line


def colorize_cb(data, modifier, modifier_data, line):

    action_info = (modifier_data.split(';')[2]).split(',')
    action = action_info[0]

    debug("===================")
    debug(modifier_data)

    if len(action_info) > 1 and action_info[1] == 'irc_numeric':
        if action == 'irc_332':
            action = 'irc_topic'
        else:
            action = 'irc_other'

    debug(action)

    colors = dict\
        ( irc_topic   = w.color('250')
        , irc_notice  = w.color('255')
        , irc_join    = w.color('238')
        , irc_part    = w.color('238')
        , irc_quit    = w.color('238')
        , irc_nick    = w.color('238')
        , irc_other   = w.color('238')
        , irc_mode    = w.color('238')
        , irc_kick    = w.color('250')
        )

    if action in colors:
        color = colors[action]
        xline = strip_colors(line)
        parts = xline.split('\t')
        xline = "%(c)s%(p0)s%(c)s\t%(c)s%(p1)s%(c)s" % dict\
            ( c = color
            , p0 = parts[0]
            , p1 = parts[1]
            )
        #debug(xline)
        return xline

    #debug(line)
    return line


if __name__ == "__main__":
    if w.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE,
                        SCRIPT_DESC, "", ""):
        w.hook_modifier('50|weechat_print', 'colorize_cb', '')


