
MAIN_ICON = "signal_32_32.bmp"

from ..gm.metaclasses import GenericMeta
from ..gm.generic_object import GenericObject
from ..gm.generic_manager import GenericManager
from ..gm import publisher

from .base.objects import UIBaseObject
from .base.objects import UIControllerObject
from .base.objects import UIViewObject
from .base.manager import UIManager
#from .base.data_mask import DataMaskController, DataMask

from .base_wx.frame import FrameController, Frame
from .base_wx.dialog import DialogController, Dialog
from .base_wx.tree import TreeController, TreeView

from .base_mpl import mpl_utils
 

#from .base.utils import TextChoiceRenderer
#                                                
from .pg.propgrid import PropertyGridController, PropertyGridView
#


from .trackssplitter import MultiSplitterWindow
from .wellplot_internal import WellPlotInternal
#from .dlg_las_header import LASHeaderController, LASHeader
#from .well_import import WellImportFrameController, WellImportFrame

#from .representation import RepresentationController, RepresentationView
#from .track_object import TrackObjectController



from .plotstatusbar import PlotStatusBar
from .main_window import MainWindowController, MainWindow
from .menu_bar import MenuBarController, MenuBarView
from .menu import MenuController, MenuView
from .menu_item import MenuItemController, MenuItemView
#from .tree import TreeController, TreeView
from .tool_bar import ToolBarController, ToolBar
from .tool_bar_tool import ToolBarToolController
from .status_bar import StatusBarController, StatusBar
from .workpage import WorkPageController, WorkPage
#from .well_plot import WellPlotController, WellPlot
#from .track import TrackController, TrackView
#
#from .frame_nav import NavigatorController, Navigator
from .cross_plotter import CrossPlotController, CrossPlot
#
from .plotter_image import ImagePlotController, ImagePlot
from .plotter_model import ModelPlotController, ModelPlot
from .plotter_wavelet import WaveletPlotController, WaveletPlot
from .plotter_simulation import SimulationPlotController, SimulationPlot
#
from .plotter_teste import TestePlotController, TestePlot
#
#from . import interface
#
#from . import ImportSelector
#from . import ExportSelector
#from . import ODTEditor
#from . import RockTableEditor
#

from .extras import SelectablePanelMixin
from .dialog_obj_props import ObjectPropertiesDialogController, \
                                                    ObjectPropertiesDialog
                                                    
from .coding_console import ConsoleController, Console
#
#from .repr_line import \
#    LineRepresentationController, LineRepresentationView
#from .repr_index import \
#    IndexRepresentationController, IndexRepresentationView
#from .repr_density import \
#    DensityRepresentationController, DensityRepresentationView
#    PatchesRepresentationController, PatchesRepresentationView, \
#    ContourfRepresentationController, ContourfRepresentationView        
                  
#from .well_plot_prop_editor import WellPlotEditorController, \
#                                                 WellPlotEditor  
                                               
#from .well_plot_prop_editor import LPEWellPlotPanelController, \
#                                                 LPEWellPlotPanel      
#from .well_plot_prop_editor import LPETrackPanelController, \
#                                                 LPETrackPanel
#from .well_plot_prop_editor import LPEObjectsPanelController, \
#                                                 LPEObjectsPanel
#

from .canvas_base import CanvasBaseController, CanvasBaseView                                         
from .canvas_plotter import CanvasPlotterController, CanvasPlotter                
from .canvas_track import TrackCanvasController, TrackCanvas   
from .track_label import TrackLabelController, TrackLabel

#### Modo teste
from .canvas_base_jun21 import CanvasBaseControllerJun21, CanvasBaseViewJun21                                         
from .canvas_plotter_jun21 import CanvasPlotterControllerJun21, CanvasPlotterJun21   
#### MOdo teste - fim
