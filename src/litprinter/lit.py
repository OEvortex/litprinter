#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# LitPrinter - Never use print() to debug again
#
# License: MIT
#

from .core import LitPrintDebugger

# Create the global instance like icecream does
lit = LitPrintDebugger(includeContext=True)