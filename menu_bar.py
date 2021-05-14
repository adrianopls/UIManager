
import wx

from . import UIManager
from . import UIControllerObject 
from . import UIViewObject 



class MenuBarController(UIControllerObject):
    tid = 'menubar_controller'
    _singleton_per_parent = True
    
    def __init__(self, **state):
        super().__init__(**state)

   
class MenuBarView(UIViewObject, wx.MenuBar):
    tid = 'menubar_view'
 
    def __init__(self, controller_uid):
        UIViewObject.__init__(self, controller_uid)
        wx.MenuBar.__init__(self)
        #
        UIM = UIManager()
        parent_controller_uid = UIM._getparentuid(controller_uid)
        parent_controller = UIM.get(parent_controller_uid)
        wx_parent = parent_controller._get_wx_parent()
        wx_parent.SetMenuBar(self)
        
