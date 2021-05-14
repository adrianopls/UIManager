"""
GenericWxMeta Metaclasse
========================

GenericWxMeta is a convinience one for creating object inherits from 
GenericObject and wx.Object.

All UIBaseObject will have GenericWxMeta as metaclass.
"""

import wx

from .. import GenericMeta


class GenericWxMeta(GenericMeta, wx.siplib.wrappertype):
     pass