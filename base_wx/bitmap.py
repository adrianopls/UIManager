# -*- coding: utf-8 -*-
"""
Created on Thu May 13 13:28:11 2021

@author: Adriano
"""

import wx

class UIBitmap(wx.Bitmap):
    
    def __init__(self, path_to_bitmap=None):
        if path_to_bitmap is None:
            super().__init__()
            return
        if os.path.exists(path_to_bitmap):
            full_file_name = path_to_bitmap
        elif os.path.exists(os.path.join(app.ICONS_PATH, \
                                                 path_to_bitmap)):
            full_file_name = os.path.join(app.ICONS_PATH, path_to_bitmap)
        else:
            raise Exception('ERROR: Wrong bitmap path [{}, {}].'.format(\
                            app.ICONS_PATH, path_to_bitmap)
            )
        super().__init__(full_file_name)    
