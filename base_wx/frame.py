import wx

from ..base.manager import UIManager
from .toplevel import  TopLevelController, TopLevel



class FrameController(TopLevelController):
    tid = 'frame_controller'
         
    def __init__(self, **state):  
        super().__init__(**state)


class Frame(TopLevel, wx.Frame):
    tid = 'frame'

    def __init__(self, controller_uid):
        TopLevel.__init__(self, controller_uid)
        UIM = UIManager()
        controller = UIM.get(self._controller_uid)
        #
        parent_uid = UIM._getparentuid(self._controller_uid)
        parent_obj = UIM.get(parent_uid)
        if not parent_obj:
            wx_parent = None
        else:
            wx_parent = parent_obj.view
        #
        wx.Frame.__init__(self, wx_parent, wx.ID_ANY, controller.title,
            pos=controller.pos, size=controller.size, 
            style=controller.style              
        ) 
        if controller.icon:   
            self.icon = GenIcon(controller.icon, wx.BITMAP_TYPE_ICO)        
            self.SetIcon(self.icon)     
        if controller.maximized:
            self.Maximize()               
        # TODO: Bind para a super class???    
        self.Bind(wx.EVT_MAXIMIZE, self.on_maximize)       
        self.Bind(wx.EVT_SIZE, self.on_size)    
        self.Bind(wx.EVT_MOVE, self.on_move)    
        self.Bind(wx.EVT_CLOSE, self.on_close)  
        

    def on_close(self, event):
        print ('\n\nFrame on_close')
#        event.Skip()
#        self._call_self_remove()
        self._auto_removal()
        wx.CallAfter(self.Destroy)
        


class GenIcon(wx.Icon):
    
    def __init__(self, path_to_bitmap=None, type_=wx.BITMAP_TYPE_ANY):
        
        #print(PurePath(app.ICONS_PATH, path_to_bitmap), 'r')
        
        if path_to_bitmap is not None:
            if Path(path_to_bitmap).exists():
                pass
            elif Path(app.ICONS_PATH, path_to_bitmap).exists():
                path_to_bitmap = Path(app.ICONS_PATH, path_to_bitmap)
            else:
                raise Exception('ERROR: Wrong bitmap path.')
        super().__init__(path_to_bitmap, type_)    