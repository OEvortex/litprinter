#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# LitPrinter - Never use print() to debug again
#
# License: MIT
#

from .core import LitPrintDebugger

# Create the global instance like icecream does, but with different prefix
litprint = LitPrintDebugger(prefix='litprint| ', includeContext=True)