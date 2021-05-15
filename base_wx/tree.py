
import wx

from ..base.manager import UIManager
from ..base.objects import UIControllerObject 
from ..base.objects import UIViewObject 


class TreeController(UIControllerObject):
    tid = 'tree_controller'
    _DEFAULT_ROOT_NAME = "MyApp Project"
    
    def __init__(self): 
        super(TreeController, self).__init__()
        

class TreeView(UIViewObject, wx.TreeCtrl):
    tid = 'tree'
    
    def __init__(self, controller_uid):
        UIViewObject.__init__(self, controller_uid)
        UIM = UIManager()
        controller = UIM.get(self._controller_uid)
        parent_controller_uid = UIM._getparentuid(self._controller_uid)
        parent_controller =  UIM.get(parent_controller_uid)  
        #
        wx.TreeCtrl.__init__(self, parent_controller.view, -1, 
                             wx.Point(0, 0), wx.Size(200, 250),
                             wx.TR_DEFAULT_STYLE | wx.NO_BORDER
        )
        #
        self._rootid = self.AddRoot(controller._DEFAULT_ROOT_NAME)                  
    
        #self.SetItemData(self._rootid, (controller._PSEUDOROOTUID, None))
            
        '''
        imglist = wx.ImageList(16, 16, True, 2)
        imglist.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, wx.Size(16,16)))
        tree.AssignImageList(imglist)
        items.append(tree.AppendItem(root, "Item 1", 0))
        '''
        
        # parent_controller.view._mgr.AddPane(self, 
        #         wx.aui.AuiPaneInfo().Name("tree").
        #         Caption("").Left().Layer(1).Position(1).
        #         PinButton(True).MinimizeButton(True).
        #         CloseButton(False).MaximizeButton(True)
        # )        
        # parent_controller.view._mgr.Update()
        




