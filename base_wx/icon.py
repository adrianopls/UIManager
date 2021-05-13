# -*- coding: utf-8 -*-
"""
Created on Thu May 13 12:57:25 2021

@author: Adriano
"""

import wx

from pathlib import Path

class UIIcon(wx.Icon):
    
    def __init__(self, path_to_bitmap=None, type_=wx.BITMAP_TYPE_ANY):
        
        #print(PurePath(app.ICONS_PATH, path_to_bitmap), 'r')
        
        if path_to_bitmap is not None:
            if Path(path_to_bitmap).exists():
                pass
#            elif Path(app.ICONS_PATH, path_to_bitmap).exists():
#                path_to_bitmap = Path(app.ICONS_PATH, path_to_bitmap)
            else:
                raise Exception('ERROR: Wrong bitmap path.')
        super().__init__(path_to_bitmap, type_)    