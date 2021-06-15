
from matplotlib.figure import Figure

from . import UIManager
from . import UIControllerObject 
from . import UIViewObject 


class FigureController(UIControllerObject):
    tid = "figure_controller"

    _ATTRIBUTES = {
        # Figure properties
        'facecolor': {
                'default_value': '#e8f3ff', #'LightSkyBlue', #'lightyellow',
                'type': str
        },
        'edgecolor': {
                'default_value': 'LightSkyBlue', #'lightyellow',
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
    

class Figure(UIViewObject, Figure):  
    tid = "figure"

    def __init__(self, controller_uid):
        UIViewObject.__init__(self, controller_uid)
        UIM = UIManager()
        controller = UIM.get(self._controller_uid)
        
        Figure.__init__(
                 figsize=None,
                 dpi=None,
                 facecolor=controller.facecolor,
                 edgecolor=controller.edgecolor,
                 linewidth=0.0,
                 frameon=None,
                 subplotpars=None,  # rc figure.subplot.*
                 tight_layout=None,  # rc figure.autolayout
                 constrained_layout=None,  # rc figure.constrained_layout.use
        )

