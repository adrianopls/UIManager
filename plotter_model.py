
import logging

import wx
from matplotlib import style as mstyle 

from . import WorkPageController
from . import WorkPage
from . import PlotStatusBar
from . import UIManager
from .base_wx.bitmap import UIBitmap



CP_NORMAL_TOOL = wx.NewId()        
CP_SELECTION_TOOL = wx.NewId()   
CP_FLOAT_PANEL = wx.NewId()  



class ModelPlotController(WorkPageController):
    tid = 'modelplot_controller'
    
    def __init__(self, **state):
        super().__init__(**state)


    
class ModelPlot(WorkPage):
    tid = 'modelplot'
    _TID_FRIENDLY_NAME = '2D Model'

    def __init__(self, controller_uid):   
        super().__init__(controller_uid) 
 
    def PostInit(self):
        logging.debug("ModelPlot.PostInit")
        try:
            self.sizer = wx.BoxSizer(wx.VERTICAL)
            self._tool_bar =  wx.aui.AuiToolBar(self)
            self.sizer.Add(self._tool_bar, 0, flag=wx.TOP|wx.EXPAND)
            #     
            UIM = UIManager()   
            canvas_controller = UIM.create('canvas_plotter_controller',
                                            self._controller_uid,
                                            figure_facecolor = "#FFFFFF",
                                            figure_titlesize = 10,
                                            xtick_labelbottom = True,
                                            ytick_labelleft = True,
                                            xgrid_major_locator = 50.0,
                                            ygrid_major_locator = 50.0,
                                            xtick_bottom = True,
                                            xtick_minor_visible = False,
                                            ytick_left = True,
                                            ytick_minor_left = False, 
                                            xtick_minor_bottom = False,
                                            xaxis_labeltext = "Grid points in X axis",
                                            yaxis_labeltext = "Grid points in Y axis"
            )
            #
                     
            self._main_panel = canvas_controller.view
            # TODO: Keep this conection? (must be disconected at PreDelete??)
#            self._main_panel.mpl_connect('motion_notify_event', 
#                                                     self.on_canvas_mouse_move)
            self.sizer.Add(self._main_panel, 1, flag=wx.EXPAND)
            #
            self._status_bar =  PlotStatusBar(self)
            self.sizer.Add(self._status_bar, 0, flag=wx.BOTTOM|wx.EXPAND)
            self.SetSizer(self.sizer)   
            #
            self._build_tool_bar()
            self.Layout()            
        except Exception as e:
            print ('ERROR IN CrossPlot.PostInit:', e)
            raise

    def PreDelete(self):
        try:
            self.sizer.Remove(0)
            del self._tool_bar
        except Exception as e:
            msg = 'PreDelete ' + self.__class__.__name__ + \
                                            ' ended with error: ' + str(e)
            print (msg)                                
            pass       

    def get_friendly_name(self):   
        return self._get_tid_friendly_name()

    def _set_own_name(self):
        """
        """  
        UIM = UIManager()   
        controller = UIM.get(self._controller_uid)   
        controller.title = self.get_friendly_name()

    def _get_wx_parent(self, *args):
        flag = args[0]
        return self
    
    def on_canvas_mouse_move(self, event):
        axes = event.inaxes
        if axes is None:
            return
        x_axis_label = 'X'
        y_axis_label = 'Y'
        msg = '{}: {:0.2f}, {}: {:0.2f}'.format(x_axis_label, event.xdata, 
                                                   y_axis_label, event.ydata
        )
        self._status_bar.SetStatusText(msg)
        
    def get_canvas_plotter_controller(self):
        UIM = UIManager()
        return UIM.list('canvas_plotter_controller',  self._controller_uid)[0]

    def _on_change_float_panel(self, event):
        # TODO: Integrar binds de toggle buttons...
        if event.GetId() == CP_FLOAT_PANEL:
            UIM = UIManager()   
            controller = UIM.get(self._controller_uid)
            controller.float_mode = event.IsChecked()            

    def _OnEditFormat(self, event): 
        cpc = self.get_canvas_plotter_controller()
        create_properties_dialog(cpc.uid, size=(600, 600))

    def _on_change_tool(self, event): 
        if event.GetId() == CP_NORMAL_TOOL:
            print ('\nCP_NORMAL_TOOL')
        elif event.GetId() == CP_SELECTION_TOOL:  
            print ('\nCP_SELECTION_TOOL')

    def _build_tool_bar(self):
        self.fp_item = self._tool_bar.AddTool(CP_FLOAT_PANEL, 
                      wx.EmptyString,
                      UIBitmap('restore_window-25.png'), 
                      wx.NullBitmap,
                      wx.ITEM_CHECK,
                      'Float Panel', 
                      'Float Panel',
                      None
        )
        self._tool_bar.ToggleTool(CP_FLOAT_PANEL, False)
        self._tool_bar.Bind(wx.EVT_TOOL, self._on_change_float_panel, None,
                  CP_FLOAT_PANEL
        )        
        self._tool_bar.AddSeparator()
        #
        self._tool_bar.AddTool(CP_NORMAL_TOOL, 
                      wx.EmptyString,
                      UIBitmap('cursor_24.png'), 
                      wx.NullBitmap,
                      wx.ITEM_RADIO,
                      'Normal Tool', 
                      'Normal Tool',
                      None
        )
        self._tool_bar.ToggleTool(CP_NORMAL_TOOL, True) 
        #
        self._tool_bar.AddTool(CP_SELECTION_TOOL, 
                      wx.EmptyString,
                      UIBitmap('cursor_filled_24.png'), 
                      wx.NullBitmap,
                      wx.ITEM_RADIO,
                      'Selection Tool', 
                      'Selection Tool',
                      None
        )  
        self._tool_bar.Bind(wx.EVT_TOOL, self._on_change_tool, None,
                  CP_NORMAL_TOOL, CP_SELECTION_TOOL
        )
        #
        self._tool_bar.AddSeparator()
        
        self._tool_bar.label_MC = wx.StaticText(self._tool_bar, 
                                                label='MPL Theme:  '
        )
        self._tool_bar.AddControl(self._tool_bar.label_MC, '')

        styles = ['default'] + mstyle.available[:]
        self._tool_bar.choice_Style = wx.Choice(self._tool_bar, choices=styles)
        self._tool_bar.choice_Style.SetSelection(0)
        #
        self._tool_bar.choice_Style.Bind(wx.EVT_CHOICE , self._on_choice_style) 
        self._tool_bar.AddControl(self._tool_bar.choice_Style, '')

        self._tool_bar.AddSeparator()

        button_edit_format = wx.Button(self._tool_bar, label='Edit Figure')
        button_edit_format.Bind(wx.EVT_BUTTON , self._OnEditFormat)
        self._tool_bar.AddControl(button_edit_format, '')
        self._tool_bar.AddSeparator()    
        #   
        self._tool_bar.Realize()  

    
    def set_own_name(self):
        UIM = UIManager()   
        controller = UIM.get(self._controller_uid)
        idx = 0
        lpcs = UIM.list('crossplot_controller')
        for lpc in lpcs:
            idx += 1
        controller.title = self._get_tid_friendly_name() + ' [' + str(idx) + ']'    
        
    def _on_choice_style(self, event):
        lib_name = event.GetString()
        UIM = UIManager()  
        cc = UIM.list('canvas_plotter_controller', self._controller_uid)[0]
        cc.load_style(lib_name)



def create_properties_dialog(obj_uid, size=None):
    if not size:
        size = (300, 330)
    UIM = UIManager()
    try:      
        dlg = UIM.create('object_properties_dialog_controller')
        #print(dlg)
        dlg.obj_uid = obj_uid
        dlg.view.SetSize(size)
        dlg.view.ShowModal()            
    except Exception as e:
        print ('\nERROR create_properties_dialog:', e)
        raise
    finally:
        UIM.remove(dlg.uid)    