# -*- coding: utf-8 -*-

import numpy as np
import wx
np.set_printoptions(suppress=True)

import matplotlib
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

from matplotlib.ticker import NullLocator
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import LogLocator
from matplotlib.ticker import LogFormatterMathtext

from matplotlib import style as mstyle 
import matplotlib.ticker as mticker
from matplotlib import rcParams

from . import UIManager
from . import UIControllerObject 
from . import UIViewObject 






# From: matplotlib\backends\backend_wxagg.py
"""
    The FigureCanvas contains the figure and does event handling.

    In the wxPython backend, it is derived from wxPanel, and (usually)
    lives inside a frame instantiated by a FigureManagerWx. The parent
    window probably implements a wxSizer to control the displayed
    control size - but we give a hint as to our preferred minimum
    size.
    """
"""
O CanvasBaseController eh a classe de base para todos objetos de Plotagem!!!
"""
 



class FigureCanvasController(UIControllerObject):
    tid = None

    _ATTRIBUTES = {

        
        
        
        
    }  

    
    def __init__(self, **state):
        super().__init__(**state)
          
        

    
class FigureCanvas(UIViewObject, FigureCanvas):  
    tid = None

    def __init__(self, controller_uid):
        UIViewObject.__init__(self, controller_uid)
        #
        self.figure = Figure()
        self.share_x = False
        #
        # Get wx parent from parent UIView object
        UIM = UIManager()
        parent_uid = UIM._getparentuid(self._controller_uid)
        parent_controller = UIM.get(parent_uid)        
        wx_parent = parent_controller._get_wx_parent(self.tid)
        #
        FigureCanvas.__init__(self, wx_parent, -1, self.figure)



    def PostInit(self):
        # Here, the model object was created and model.PostInit() was called.    
        UIM = UIManager()
        controller = UIM.get(self._controller_uid)
        #
        self._postpone_draw = False
        #
        self.base_axes = Axes(self.figure, controller.rect,
                                  facecolor=None,
                                  frameon=True,
                                  sharex=None,  # use Axes instance's xaxis info
                                  sharey=None,  # use Axes instance's yaxis info
                                  label='',
                                  xscale=controller.xscale,
                                  yscale=controller.yscale,
                                  xlim=controller.xlim,
                                  ylim=controller.ylim
        )
        self.figure.add_axes(self.base_axes)
        self.base_axes.set_zorder(0)        
        #
        if self.share_x:
            self.plot_axes = Axes(self.figure, 
                             rect=self.base_axes.get_position(True), 
                             sharey=self.base_axes, 
                             sharex=self.base_axes, 
                             frameon=False
            )
        else:    
            self.plot_axes = Axes(self.figure, 
                             rect=self.base_axes.get_position(True), 
                             sharey=self.base_axes, 
                             frameon=False
            )
            self.plot_axes.set_xlim(controller.xlim)

        
        
              
        #
        """
        _PLOT_XMIN = 0.0
        _PLOT_XMAX = 1.0            
      
        self.plot_axes = GripyMPLAxes(self.figure, 
                         rect=self.base_axes.get_position(True), 
                         sharey=self.base_axes, 
                         frameon=False
        )
        self.figure.add_axes(self.plot_axes)
        self.plot_axes.set_xlim(self._PLOT_XMIN, self._PLOT_XMAX)
        self.plot_axes.xaxis.set_visible(False)
        self.plot_axes.yaxis.set_visible(False)        
        self.plot_axes.set_zorder(1)            
        """    
        #
        self.figure.add_axes(self.plot_axes)
        #
        self.plot_axes.xaxis.set_visible(False)
        self.plot_axes.yaxis.set_visible(False)        
        self.plot_axes.set_zorder(1)        
        
        
        #
        self.set_axis_visibility('x', controller.xaxis_visibility)
        self.set_axis_visibility('y', controller.yaxis_visibility)


        #  
        self.figure.set_facecolor(controller.figure_facecolor)

        #
        
        self.set_axes_facecolor(controller.axes_facecolor)
        self.set_axes_edgecolor(controller.axes_edgecolor)
        self.set_axes_axisbelow(controller.axes_axisbelow)
        self.set_axes_linewidth(controller.axes_linewidth)
        
        #
        self._load_spines_properties()
        self._load_locator_properties()
        self._load_ticks_properties()
        self._load_grids_properties()
        self._load_labels_properties()
        #
        #self._postpone_draw = True
        

    def _load_spines_properties(self):
        UIM = UIManager()
        controller = UIM.get(self._controller_uid)        
        #
        self.set_spine_visibility('right', controller.axes_spines_right) 
        self.set_spine_visibility('left', controller.axes_spines_left) 
        self.set_spine_visibility('bottom', 
                                          controller.axes_spines_bottom) 
        self.set_spine_visibility('top', controller.axes_spines_top) 
        #        
        self.set_spine_position('right', 
                                controller.axes_spines_right_position)
        self.set_spine_position('left',
                                controller.axes_spines_left_position)
        self.set_spine_position('bottom',
                                controller.axes_spines_bottom_position)
        self.set_spine_position('top',
                                controller.axes_spines_top_position)
        #
        self.base_axes.spines['left'].set_zorder(10)
        self.base_axes.spines['right'].set_zorder(10)
        self.base_axes.spines['top'].set_zorder(10)
        self.base_axes.spines['bottom'].set_zorder(10)          
        #
        
        
    # TODO: Melhorar isso    
    def _load_locator_properties(self):
        UIM = UIManager()
        controller = UIM.get(self._controller_uid)
        
        if controller.xscale == 'log':
            return
            
        loc_type = 'multiple'
      
        self.set_locator(loc_type, 'x', 'major', 
                                     controller.xgrid_major_locator)
        self.set_locator(loc_type, 'x', 'minor', 
                                     controller.xgrid_minor_locator)
        self.set_locator(loc_type, 'y', 'major', 
                                     controller.ygrid_major_locator)
        self.set_locator(loc_type, 'y', 'minor', 
                                     controller.ygrid_minor_locator)        


    # TODO: colocar Tick label no centro matplotlib.axis.py (435)
    # TODO: zorder
    def _load_ticks_properties(self):
        UIM = UIManager()
        controller = UIM.get(self._controller_uid)
        # Major Ticks and its label visibility
        self.base_axes.tick_params(which='major',
            top=(controller.xtick_top and 
                 controller.xtick_major_top),
            bottom=(controller.xtick_bottom and 
                    controller.xtick_major_bottom),
            labeltop=(controller.xtick_labeltop and 
                      controller.xtick_major_top),
            labelbottom=(controller.xtick_labelbottom and 
                         controller.xtick_major_bottom),
            left=(controller.ytick_left and 
                  controller.ytick_major_left),
            right=(controller.ytick_right and 
                   controller.ytick_major_right),
            labelleft=(controller.ytick_labelleft and 
                       controller.ytick_major_left),
            labelright=(controller.ytick_labelright and 
                        controller.ytick_major_right)   
        )
        # Minor Ticks and its label visibility
        self.base_axes.tick_params(which='minor',
            top=(controller.xtick_top and 
                 controller.xtick_minor_top),
            bottom=(controller.xtick_bottom and 
                    controller.xtick_minor_bottom),
            labeltop=(controller.xtick_labeltop and 
                      controller.xtick_minor_top),
            labelbottom=(controller.xtick_labelbottom and 
                         controller.xtick_minor_bottom),
            left=(controller.ytick_left and 
                  controller.ytick_minor_left),
            right=(controller.ytick_right and 
                   controller.ytick_minor_right),
            labelleft=(controller.ytick_labelleft and 
                       controller.ytick_minor_left),
            labelright=(controller.ytick_labelright and 
                        controller.ytick_minor_right)
        )  
        # Ticks Properties
        self.base_axes.tick_params(axis='x', which='major', 
                           direction=controller.xtick_direction,
                           length=controller.xtick_major_size,
                           width=controller.xtick_major_width,
                           pad=controller.xtick_major_pad,
                           labelcolor=controller.xtick_labelcolor,
                           labelrotation=controller.xtick_labelrotation,
                           labelsize=controller.xtick_labelsize,
                           color=controller.xtick_color#,
                           #zorder=
        )
        self.base_axes.tick_params(axis='x', which='minor', 
                           direction=controller.xtick_direction,
                           length=controller.xtick_minor_size,
                           width=controller.xtick_minor_width,
                           pad=controller.xtick_minor_pad,
                           labelcolor=controller.xtick_labelcolor,
                           labelrotation=controller.xtick_labelrotation,
                           labelsize=controller.xtick_labelsize,
                           color=controller.xtick_color#,
                           #zorder=
        )
        self.base_axes.tick_params(axis='y', which='major', 
                           direction=controller.ytick_direction,
                           length=controller.ytick_major_size,
                           width=controller.ytick_major_width,
                           pad=controller.ytick_major_pad,
                           labelcolor=controller.ytick_labelcolor,
                           labelrotation=controller.ytick_labelrotation,
                           labelsize=controller.ytick_labelsize,
                           color=controller.ytick_color#,
                           #zorder=
        )
        self.base_axes.tick_params(axis='y', which='minor', 
                           direction=controller.ytick_direction,
                           length=controller.ytick_minor_size,
                           width=controller.ytick_minor_width,
                           pad=controller.ytick_minor_pad,
                           labelcolor=controller.ytick_labelcolor,
                           labelrotation=controller.ytick_labelrotation,
                           labelsize=controller.ytick_labelsize,
                           color=controller.ytick_color#,
                           #zorder=
        )




        
    def _load_grids_properties(self):
        UIM = UIManager()
        controller = UIM.get(self._controller_uid)
        self.set_grid_parameters(axis='x', which='major',                          
                         gridOn=controller.xgrid_major,
                         grid_color=controller.xgrid_major_color,
                         grid_alpha=controller.xgrid_major_alpha,
                         grid_linestyle=controller.xgrid_major_linestyle,
                         grid_linewidth=controller.xgrid_major_linewidth
        ) 
        self.set_grid_parameters(axis='x', which='minor',                          
                         gridOn=controller.xgrid_minor,
                         grid_color=controller.xgrid_minor_color,
                         grid_alpha=controller.xgrid_minor_alpha,
                         grid_linestyle=controller.xgrid_minor_linestyle,
                         grid_linewidth=controller.xgrid_minor_linewidth
        )
        self.set_grid_parameters(axis='y', which='major',                          
                         gridOn=controller.ygrid_major,
                         grid_color=controller.ygrid_major_color,
                         grid_alpha=controller.ygrid_major_alpha,
                         grid_linestyle=controller.ygrid_major_linestyle,
                         grid_linewidth=controller.ygrid_major_linewidth
        ) 
        self.set_grid_parameters(axis='y', which='minor',                          
                         gridOn=controller.ygrid_minor,
                         grid_color=controller.ygrid_minor_color,
                         grid_alpha=controller.ygrid_minor_alpha,
                         grid_linestyle=controller.ygrid_minor_linestyle,
                         grid_linewidth=controller.ygrid_minor_linewidth
        )




       # self.teste('red')


    def _load_labels_properties(self):
        UIM = UIManager()
        controller = UIM.get(self._controller_uid)        
        self.set_label_properties('figure', 
                        text=controller.figure_titletext, 
                        x=controller.figure_titlex, 
                        y=controller.figure_titley, 
                        ha=controller.figure_titleha, 
                        va=controller.figure_titleva,
                        size=controller.figure_titlesize, 
                        weight=controller.figure_titleweight
        )
        #
        self.set_label_properties('axes', 
                                  loc='left',
                                  text=controller.axes_titletextleft,
                                  color=controller.axes_titlecolor,
                                  pad=controller.axes_titlepad,
                                  size=controller.axes_titlesize,
                                  weight=controller.axes_titleweight
        ) 
        self.set_label_properties('axes', 
                                  loc='center',
                                  text=controller.axes_titletextcenter,
                                  color=controller.axes_titlecolor,
                                  pad=controller.axes_titlepad,
                                  size=controller.axes_titlesize,
                                  weight=controller.axes_titleweight
        ) 
        self.set_label_properties('axes', 
                                  loc='right',
                                  text=controller.axes_titletextright,
                                  color=controller.axes_titlecolor,
                                  pad=controller.axes_titlepad,
                                  size=controller.axes_titlesize,
                                  weight=controller.axes_titleweight
        )                               
        #
        self.set_label_properties('axis', axis='x', 
                                text=controller.xaxis_labeltext, 
                                color=controller.axes_labelcolor, 
                                pad=controller.axes_labelpad,
                                size=controller.axes_labelsize,
                                weight=controller.axes_labelweight
        )
        self.set_label_properties('axis', axis='y', 
                                text=controller.yaxis_labeltext,
                                color=controller.axes_labelcolor, 
                                pad=controller.axes_labelpad,
                                size=controller.axes_labelsize,
                                weight=controller.axes_labelweight
        )    



        
    def draw(self, drawDC=None):
        if not self._postpone_draw:
            super().draw(drawDC)



    # Only for base_axes
    def set_lim(self, axis, lim):
        if axis == 'x':
            return self.base_axes.set_xlim(lim)
        elif axis == 'y':
            return self.base_axes.set_ylim(lim)
        else:
            raise Exception('Invalid axis [{}].'.format(axis))        

    # Only for base_axes
    def set_scale(self, axis, scale):            
        if axis == 'x':
            return self.base_axes.set_xscale(scale)
        elif axis == 'y':
            return self.base_axes.set_yscale(scale)
        else:
            raise Exception('Invalid axis [{}].'.format(axis))   
  

    def set_figure_facecolor(self, color):
        try:
            self.figure.set_facecolor(color)
        except:
            raise
        
        
    def set_axis_visibility(self, axis, visibility):
        if axis == 'x':
            ax = self.base_axes.xaxis
        elif axis == 'y':
            ax = self.base_axes.yaxis
        else:
            raise Exception('Invalid axis [{}].'.format(axis))
        ax.set_visible(visibility)
         
        
    def set_spine_visibility(self, spine, visibility):
        try:
            self.base_axes.spines[spine].set_visible(visibility)
        except:
            raise


    def set_spine_position(self, spine, position):
        try:
            self.base_axes.spines[spine].set_position(position)
        except:
            raise

            
    def set_position(self, rect):
        try:
            self.base_axes.set_position(rect)
            self.plot_axes.set_position(rect)
        except:
            raise
                        
            
    def set_grid_parameters(self, axis, which, **kwargs):
#        print ('\nset_grid_params:', axis, which, kwargs)
        gridOn = kwargs.pop('gridOn', None)
        
        if gridOn is None:
            if axis == 'x' or axis == 'both':
                self.base_axes.xaxis.set_tick_params(**kwargs)
            if axis == 'y' or axis == 'both':
                self.base_axes.yaxis.set_tick_params(**kwargs)     
                          
        else:    
            if axis == 'x'or axis == 'both':            
                ax = self.base_axes.xaxis
                if which == 'major': 
                    ax._gridOnMajor = gridOn
                    ax.set_tick_params(which='major', 
                                           gridOn=ax._gridOnMajor, **kwargs)
                elif which == 'minor':     
                    ax._gridOnMinor = gridOn
                    ax.set_tick_params(which='minor', 
                                           gridOn=ax._gridOnMinor, **kwargs) 
            
            elif axis == 'y'or axis == 'both':
                ax = self.base_axes.yaxis
                if which == 'major': 
                    ax._gridOnMajor = gridOn
                    ax.set_tick_params(which='major', 
                                           gridOn=ax._gridOnMajor, **kwargs)
                elif which == 'minor':     
                    ax._gridOnMinor = gridOn
                    ax.set_tick_params(which='minor', 
                                           gridOn=ax._gridOnMinor, **kwargs) 
                    

    def set_locator(self, locator_type, axis, which, *args, **kwargs):
        try: 
            # TODO: Check Formatter (FmtType)
            FmtType = None
            if locator_type is None:
                LocType = NullLocator
            elif locator_type == 'multiple':
                LocType = MultipleLocator
            elif locator_type == 'log':
                LocType = LogLocator
                FmtType = LogFormatterMathtext
            else:
                raise Exception('Invalid locator_type.')
            #    
            if axis not in ['x', 'y']:
                raise Exception('Invalid axis.')
            if which not in ['minor', 'major']:
                raise Exception('Invalid which.')
            #            
            if axis == 'x':
                ax = self.base_axes.xaxis
            else:
                ax = self.base_axes.yaxis  
            #    
            if which == 'major':
                ax.set_major_locator(LocType(*args, **kwargs))
                if FmtType:
                    ax.set_major_formatter(FmtType())
            else:
                ax.set_minor_locator(LocType(*args, **kwargs))
                if FmtType:
                    ax.set_minor_formatter(FmtType())
        except:
            raise
        


        

    #TODO: tirar isso 
    #def teste(self, color):
    #    self.base_axes.patch.set_edgecolor(color)
        
        
    def set_axes_facecolor(self, color):
        self.base_axes.set_facecolor(color)
        
        
    def set_axes_edgecolor(self, color):
        self.base_axes.spines['left'].set_edgecolor(color)
        self.base_axes.spines['right'].set_edgecolor(color)
        self.base_axes.spines['bottom'].set_edgecolor(color)
        self.base_axes.spines['top'].set_edgecolor(color)
        
    def set_axes_axisbelow(self, b):
        """
        Set whether axis ticks and gridlines are above or below most artists.

        .. ACCEPTS: [ bool | 'line' ]

        Parameters
        ----------
        b : bool or 'line'
            
        *axisbelow*        [ bool | 'line' ] draw the grids
                             and ticks below or above most other artists,
                             or below lines but above patches
        """  
        
        try:
            b = bool(b)
        except Exception as e:
            print('ERRO:', e)         
        try:    
            self.base_axes.set_axisbelow(b)
        except:
            raise

    def set_axes_linewidth(self, value):
        self.base_axes.spines['left'].set_linewidth(value)
        self.base_axes.spines['right'].set_linewidth(value)
        self.base_axes.spines['bottom'].set_linewidth(value)
        self.base_axes.spines['top'].set_linewidth(value)     

    
    def set_label_properties(self, who, **kwargs):
        text = kwargs.pop('text', None)
        pad = kwargs.pop('pad', None)
        #
        axis = kwargs.pop('axis', None)
        loc = kwargs.pop('loc', 'all')
        #
        text_objs = []
          
        if who == 'axes':
            if loc == 'left' or loc == 'all':
                text_objs.append(self.base_axes._left_title)
            if loc == 'center' or loc == 'all':
                text_objs.append(self.base_axes.title)    
            if loc == 'right' or loc == 'all':
                text_objs.append(self.base_axes._right_title)       
  
        elif who == 'axis':
            if pad is not None:
                if axis == 'x' or axis == 'both':
                    self.base_axes.xaxis.labelpad = pad 
                    self.base_axes.xaxis.stale = True
                if axis == 'y' or axis == 'both':
                    self.base_axes.yaxis.labelpad = pad
                    self.base_axes.yaxis.stale = True 
            if axis == 'x' or axis == 'both':
                 text_objs.append(self.base_axes.xaxis.label)
            if axis == 'y' or axis == 'both':     
                 text_objs.append(self.base_axes.yaxis.label)
                 
        elif who == 'figure':  
            if self.figure._suptitle is None:
                x = kwargs.pop('x', 0.5)
                y = kwargs.pop('y', 0.98)
                if text is None:
                    text = ''
                self.figure._suptitle = self.figure.text(x, y, text) 
            text_objs.append(self.figure._suptitle)
            
            
        for text_obj in text_objs:
            if text is not None:
                text_obj.set_text(text)
            text_obj.update(kwargs) 
            
            
    
    def set_tick_params(self, axis, which, **kwargs):  
#        print ('\nset_tick_params:', axis, which, kwargs)
        if axis not in ['x', 'y', 'both']:
            raise Exception('Invalid axis.')
        #    
        if which not in ['minor', 'major', 'both']:
            raise Exception('Invalid which.') 
        #
        if axis in ['x', 'both']:
            axis_ = self.base_axes.xaxis
            try:
                axis_.set_tick_params(which=which, **kwargs)
            except:
                raise
            finally:
                axis_.stale = True 
                
        if axis in ['y', 'both']:
            axis_ = self.base_axes.yaxis
            try:
                axis_.set_tick_params(which=which, **kwargs)
            except:
                raise
            finally:
                axis_.stale = True      
    
    
    
    def set_minor_tick_visibility(self, axis, b):
        axis_list = []
        if axis == 'x' or axis == 'both':
            axis_list.append(self.base_axes.xaxis)
        if axis == 'y' or axis == 'both':
            axis_list.append(self.base_axes.yaxis)
        if b:
            for ax in axis_list:
                scale = ax.get_scale()    
                if scale == 'log':
                    s = ax._scale
                    ax.set_minor_locator(mticker.LogLocator(s.base, s.subs))
                elif scale == 'symlog':
                    s = ax._scale
                    ax.set_minor_locator(
                        mticker.SymmetricalLogLocator(s._transform, s.subs))
                else:
                    ax.set_minor_locator(mticker.AutoMinorLocator())
        else:
            for ax in axis_list:
                ax.set_minor_locator(mticker.NullLocator()) 



    def get_xlim(self, axes=None):
        if axes is None:
            return self.base_axes.get_xlim()
        elif axes == 'plot_axes':
            return self.plot_axes.get_xlim()
        else:
            raise Exception('Wrong axes informed.')
        
    
    def get_ylim(self):
        return self.base_axes.get_ylim()     
    
    def get_transdata(self):    
        return self.base_axes.transData   
    
    def get_transaxes(self):
        return self.base_axes.transAxes    


##############################################################################
##############################################################################
##############################################################################
        
    
    # Only for plot_axes
    def set_plot_lim(self, axis, lim):
        print('\nset_plot_lim:', axis, lim)
        if axis == 'x':
            return self.plot_axes.set_xlim(lim)
        elif axis == 'y':
            return self.plot_axes.set_ylim(lim)
        else:
            raise Exception('Invalid axis [{}].'.format(axis))        


    # Only for plot_axes
    def set_plot_scale(self, axis, scale):            
        if axis == 'x':
            return self.plot_axes.set_xscale(scale)
        elif axis == 'y':
            return self.plot_axes.set_yscale(scale)
        else:
            raise Exception('Invalid axis [{}].'.format(axis))  
    
    
    # TODO: separar create e add
    def append_artist(self, artist_type, *args, **kwargs):
        if artist_type == 'Line2D':
            line = matplotlib.lines.Line2D(*args, **kwargs)
            return self.plot_axes.add_line(line)
        
        elif artist_type == 'Text':
            return self.plot_axes.text(*args, **kwargs)
        
        elif artist_type == 'AxesImage':
            image = matplotlib.image.AxesImage(self.plot_axes, *args, **kwargs)
            self.plot_axes.add_image(image)
            return image
        
        elif artist_type == 'Rectangle':
            rect = matplotlib.patches.Rectangle(*args, **kwargs)
            return rect
        
        elif artist_type == 'PatchCollection':
            collection = matplotlib.collections.PatchCollection(*args, **kwargs)
            return self.plot_axes.add_collection(collection)
        
        elif artist_type == 'contourf':
            #contours = mcontour.QuadContourSet(self.plot_axes, *args, **kwargs)
            #self.plot_axes.autoscale_view()
            image = self.plot_axes.contourf(*args, **kwargs)
            #self.plot_axes.add_image(image)
            return image
        
        elif artist_type == 'scatter':
            # TODO: rever linha abaixo, colocando de forma similar as de cima
            return self.plot_axes.scatter(*args, **kwargs)
            #def scatter(self, x, y, s=None, c=None, marker=None, cmap=None, norm=None,
            #    vmin=None, vmax=None, alpha=None, linewidths=None,
            #    verts=None, edgecolors=None,
            #    **kwargs):
        
        else:
            raise Exception('artist_type not known.')  
    
    
    def transform(self, value, left_scale, right_scale, scale=0):
        """
        Transform data to a virtual X axis and scale.
                
        Usado em um cenario onde plot_axes recebe multiplos artists de forma 
        virtual. 
        Nesta ideia, plot_axes eh sempre linear.
        left_scale e right_scale sao os limites do eixo virtual.
        scale eh a escala virtual (0=linear, 1=log)
        """
        if left_scale is None or right_scale is None:
            raise Exception('Left or Right scales cannot be None.')
        if scale not in [0, 1]:
            raise Exception('Scale must be 0 or 1.')
        invalid_err = np.geterr().get('invalid')
        invalid_err = np.geterr().get('invalid')
        np.seterr(invalid='ignore')
        #
        plot_axis_left_xlim, plot_axis_right_xlim = self.plot_axes.get_xlim()
        # Linear scale
        if scale == 0:
            range_ = np.absolute(right_scale - left_scale)
            translated_value = np.abs(value - left_scale)    
            ret_val =  (translated_value / range_)
        # Log scale    
        else:
            if left_scale <= 0.0:
                raise Exception('left_scale <= 0.0')
            ls = np.log10(left_scale)    
            rs = np.log10(right_scale)
            range_ = rs - ls
            data = np.copy(value)
            data[data == 0] = left_scale
            translated_value = np.log10(data) - ls   
            ret_val =  (translated_value / range_)     
        real_range_ = np.absolute(plot_axis_right_xlim - plot_axis_left_xlim)
        ret_val = ret_val * real_range_
        ret_val = ret_val + plot_axis_left_xlim 
        np.seterr(invalid=invalid_err)
        return ret_val   
     
    
    def inverse_transform(self, value, left_scale, right_scale, scale=0):
        """
        Inverse transform data to a virtual X axis and scale.
        
        Usado em um cenario onde plot_axes recebe multiplos artists de forma 
        virtual. 
        Nesta ideia, plot_axes eh sempre linear.
        left_scale e right_scale sao os limites do eixo virtual.
        scale eh a escala virtual (0=linear, 1=log)
        """    
        if left_scale is None or right_scale is None:
            raise Exception('Left or Right scales cannot be None.')
        if scale not in [0, 1]:
            raise Exception('Scale must be 0 or 1.')
        invalid_err = np.geterr().get('invalid')
        np.seterr(invalid='ignore')
        #
        plot_axis_left_xlim, plot_axis_right_xlim = self.plot_axes.get_xlim()
        #
        ret_val = value - plot_axis_left_xlim
        real_range_ = np.absolute(plot_axis_right_xlim - plot_axis_left_xlim) 
        ret_val = ret_val / real_range_
        if scale == 0:
            range_ = np.absolute(right_scale - left_scale)
            ret_val = ret_val * range_
            ret_val = ret_val + left_scale
        else:
            ls = np.log10(left_scale)    
            rs = np.log10(right_scale)
            range_ = rs - ls
            translated_value = ret_val * range_
            ret_val = np.power(10.0, translated_value)
        np.seterr(invalid=invalid_err)
        return ret_val     
    