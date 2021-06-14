
from . import UIManager
from . import UIControllerObject 
from . import UIViewObject 

from matplotlib.figure import Figure



class FigureController(UIControllerObject):
    tid = None

    _ATTRIBUTES = {
        # Figure properties
        'figure_facecolor': {
                'default_value': '#e8f3ff', #'LightSkyBlue', #'lightyellow',
                'type': str
        },

        'figure_titletext': {
                'default_value': '', #'Figure Title', #wx.EmptyString, 
                'type': str
        },
        'figure_titlex': {
                'default_value': 0.5, 
                'type': float
        },        
        'figure_titley': {
                'default_value': 0.95, 
                'type': float
        },
        'figure_titlesize': {
                'default_value': '15.0', 
                'type': str
        },
        'figure_titleweight': {
                'default_value': 'normal', 
                'type': str
        },                
        'figure_titleha': {
                'default_value': 'center', 
                'type': str
        },                  
        'figure_titleva': {
                'default_value': 'center', 
                'type': str
        },            
    }
    

class FigureView(UIViewObject, Figure):  
    tid = None

    def __init__(self, controller_uid):
        UIViewObject.__init__(self, controller_uid)
        Figure.__init__(
                 figsize=None,
                 dpi=None,
                 facecolor=None,
                 edgecolor=None,
                 linewidth=0.0,
                 frameon=None,
                 subplotpars=None,  # rc figure.subplot.*
                 tight_layout=None,  # rc figure.autolayout
                 constrained_layout=None,  # rc figure.constrained_layout.use
        )
        #
        # Get wx parent from parent UIView object
        # UIM = UIManager()
        # parent_uid = UIM._getparentuid(self._controller_uid)
        # parent_controller = UIM.get(parent_uid)        
        # wx_parent = parent_controller._get_wx_parent(self.tid)
        #
