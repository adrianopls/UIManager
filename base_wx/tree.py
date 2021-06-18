
import logging

import wx
import numpy as np
from matplotlib.animation import FuncAnimation
 
import app
from ..base.manager import UIManager
from ..base.objects import UIControllerObject 
from ..base.objects import UIViewObject 
from classes.om import ObjectManager

from solver.animation import SGAnimation


ID_TYPE_OBJECT = 0
ID_TYPE_TID = 1
ID_TYPE_ATTRIBUTE = 2


class TreeController(UIControllerObject):
    tid = 'tree_controller'
    _DEFAULT_ROOT_NAME = "SonicSim Project"
    
    def __init__(self): 
        super(TreeController, self).__init__()
         
    def PostInit(self):
        OM = ObjectManager()
        OM.subscribe(self._on_OM_object_added, 'add')
        OM.subscribe(self._on_OM_object_removed, 'post_remove')

    def PreDelete(self): 
        OM = ObjectManager()
        OM.unsubscribe(self._on_OM_object_added, 'add')
        OM.unsubscribe(self._on_OM_object_removed, 'post_remove')


    def _on_OM_object_added(self, objuid):  
        self.reload_tree()

    def _on_OM_object_removed(self, objuid):  
        self.reload_tree()




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
                             wx.Point(0, 0), wx.Size(250, 300),
                             wx.TR_DEFAULT_STYLE | wx.NO_BORDER
        )
        #
        self._rootid = self.AddRoot(controller._DEFAULT_ROOT_NAME)                  
    
    
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self._on_activate)  
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self._on_rightclick)    
        

        parent_controller.view._mgr.AddPane(self, 
                wx.aui.AuiPaneInfo().Name("tree").
                Caption("").Left().Layer(1).Position(1).
                PinButton(True).MinimizeButton(True).
                CloseButton(False).MaximizeButton(True)
        )        
        parent_controller.view._mgr.Update()
        


    def _on_activate(self, event):
        tree_item = event.GetItem()
        if tree_item == self.GetRootItem():
            return
        item_data = self.GetItemData(tree_item)
        (node_type, node_main_info, node_extra_info) = item_data
        
        if node_type != ID_TYPE_OBJECT:    
            return
        
        if node_main_info[0] == "acoustic_2d_model":
            self._open_model(node_main_info)
        elif node_main_info[0] == "wavelet":
            self._open_wavelet(node_main_info)        
        elif node_main_info[0] == "simulation":
            self._open_simulation(node_main_info)               
        logging.debug("_on_activate: {} - {} - {}".format(node_type, node_main_info, node_extra_info))
        

        
 
    

    def _on_rightclick(self, event):
        tree_item = event.GetItem()
        if tree_item == self.GetRootItem():
            return
        item_data = self.GetItemData(tree_item)
        (node_type, node_main_info, node_extra_info) = item_data
        
        if node_type == ID_TYPE_ATTRIBUTE:    
            return

        logging.debug("_on_rightclick: {} - {} - {}".format(node_type, node_main_info, node_extra_info))
        
        self.popup_obj = (node_type, node_main_info, node_extra_info)
        self.popupmenu = wx.Menu()  
        item = self.popupmenu.Append(wx.NewId(), 'Properties')
        self.Bind(wx.EVT_MENU, self.on_object_properties, item)
        #
        pos = event.GetPoint()
        self.PopupMenu(self.popupmenu, pos)
        
        

    def reload_tree(self, *args):     
        
        print()
        
        logging.debug("reload_tree " + str(args))
        
        self.DeleteChildren(self._rootid)        
        OM = ObjectManager()
        
        lista = OM.list()
        print (lista)
        
        print()
        
        for obj in OM.list():            
            self._add_tree_node(obj.uid, OM._getparentuid(obj.uid))

            
            
    def _add_tree_node(self, objuid, parentuid=None):         
        
        logging.debug("_add_tree_node " + str(objuid) + " - " + str(parentuid))
        
        OM = ObjectManager()
        obj = OM.get(objuid)            


        node_props = obj._get_tree_object_node_properties()
        if node_props is None:
            return

             
        if obj._is_tree_tid_node_needed():
            
            obj_parent_node = self.get_object_tree_item(ID_TYPE_TID, 
                                                    objuid[0], parentuid
            )            
            if obj_parent_node is None:
                
                if parentuid is None:
                    # Create tid node as a root child
                    tid_parent_node = self.GetRootItem()
                else:
                    # Create tid node as another object child
                    tid_parent_node = self.get_object_tree_item(
                                            ID_TYPE_OBJECT, parentuid
                    ) 
                                      
                # Create tid node    
                class_ = OM._gettype(objuid[0])
                tid_label = class_._get_tid_friendly_name()
            

                obj_parent_node = self.AppendItem(tid_parent_node, 
                                                         tid_label)    
                self.SetItemData(obj_parent_node, 
                                      (ID_TYPE_TID, objuid[0], parentuid))        
                self.Expand(tid_parent_node)
        else:
            obj_parent_node = self.get_object_tree_item(ID_TYPE_OBJECT, parentuid) 
        
        
        obj_repr = node_props.pop('name')
        obj_node = self.AppendItem(obj_parent_node, obj_repr)
        self.SetItemData(obj_node, (ID_TYPE_OBJECT, objuid, 'name'))
       
        self.Expand(obj_parent_node) 
       
     
            
        for attr, attr_label in node_props.items():
            logging.debug('Creating attr_node: {} - {} - {}'.format(ID_TYPE_ATTRIBUTE, objuid, attr)) 
            attr_node = self.AppendItem(obj_node, attr_label)
            self.SetItemData(attr_node, (ID_TYPE_ATTRIBUTE, objuid, attr))      
            #print ('Creating attr_node:',  (ID_TYPE_ATTRIBUTE, objuid, attr))   
             
        self.Expand(obj_node)
        
     
        
     
        
    def get_object_tree_item(self, node_type, node_main_info, 
                                 node_extra_info=None, start_node_item=None):
        """Returns the wx.TreeItemId associated with Tree data given.
        """
#        print ('\nget_object_tree_item:', node_type, node_main_info, 
#                                           node_extra_info, start_node_item)
        
        try:
            if start_node_item is None:
                start_node_item = self.GetRootItem()
                
            start_node_data = self.GetItemData(start_node_item)
            
#            print ('111', start_node_item, start_node_data)

                
            if start_node_data is not None:
                    
                if node_type == ID_TYPE_OBJECT:
                    _, obj_uid, _ = start_node_data
                    if obj_uid == node_main_info:
                        # We found the TreeItem (Object)
                        return start_node_item
                    
                elif start_node_data == (node_type, node_main_info, node_extra_info):
                    # We found the TreeItem (Tid or Object attribute)
                    return start_node_item      
                
            # Let's search in children
            (child_item, cookie) = self.GetFirstChild(start_node_item)
            
            while child_item.IsOk():
                ret_child_val = self.get_object_tree_item(node_type, 
                                node_main_info, node_extra_info, child_item)
                if ret_child_val is not None:
                    return ret_child_val         
                (child_item, cookie) = self.GetNextChild(start_node_item,
                                                                        cookie)
            
#            print('RETORNOU NONE!!!!')
            
            return None       
        
        except Exception as e:
            print('\nERROR: get_object_tree_item:', e)
        #except:
            raise        



    def on_object_properties(self, event):
        print ('on_object_properties', self.popup_obj)
        
        return
        
        # node_main_info is the obj_uid
        _, obj_uid, _ = self.popup_obj
        app.menu_functions.create_properties_dialog(obj_uid)



    def _open_model(self, model_uid):
        OM = ObjectManager()
        model = OM.get(model_uid)    
        
        UIM = UIManager()      
        mwc = wx.GetApp().get_main_window_controller()
        cc = UIM.create('modelplot_controller', mwc.uid)        
        
        
        
        #xlim_max, ylim_max = model.data.shape
        # (left, right, bottom, top)
        extent = (0, model.nx, model.ny, 0)
        
        print("\n\n")
        print(extent)
        print("\n\n")
        
        
        image = cc._main_panel.append_artist("AxesImage", 
                                              cmap="binary",
                                              extent=extent)

        image.set_data(model.data)
      
        
        cpc = UIM.list('canvas_plotter_controller', cc.uid)[0]
        cpc.figure_titletext = model.name 
        
        xlim = (0, model.nx)
        cpc.xlim = xlim
        cpc.set_plot_lim("x", xlim)
        ylim = (model.ny, 0)
        cpc.ylim = ylim
        cpc.set_plot_lim("y", ylim)
        
        print(model.nx, model.ny)

        #image.set_label('crossplot_controller')            


    def _open_wavelet(self, wavelet_uid):
        OM = ObjectManager()
        wavelet = OM.get(wavelet_uid)    
        
        UIM = UIManager()      
        # mwc = wx.GetApp().get_main_window_controller()
        # cc = UIM.create('crossplot_controller', mwc.uid)        

        dlg = UIM.create('dialog_controller', title='Plot Wavelet')
        #
        ctn_dt = dlg.view.AddCreateContainer('StaticBox', 
                                        label='Wavelet Time Step (dt)', 
                                        orient=wx.VERTICAL, 
                                        proportion=0, 
                                        flag=wx.EXPAND|wx.TOP, border=5)
        dlg.view.AddTextCtrl(ctn_dt, proportion=0, flag=wx.EXPAND|wx.TOP, 
                             border=5, widget_name='dt', initial='0.01') 
        #

        ctn_time_stop = dlg.view.AddCreateContainer('StaticBox', 
                                        label='Wavelet Time Stop', 
                                        orient=wx.VERTICAL, 
                                        proportion=0, 
                                        flag=wx.EXPAND|wx.TOP, border=5)
        dlg.view.AddTextCtrl(ctn_time_stop, proportion=0, flag=wx.EXPAND|wx.TOP, 
                             border=5, widget_name='time_stop', initial='1.0') 
        #
        

    
    
        dlg.view.SetSize((300, 400))
        result = dlg.view.ShowModal()
        #
        try:
            disableAll = wx.WindowDisabler()
            wait = wx.BusyInfo("Ploting wavelet. Wait...")
            if result == wx.ID_OK:
                results = dlg.get_results()          
                print (results)
                
                mwc = wx.GetApp().get_main_window_controller()
                cc = UIM.create('waveletplot_controller', mwc.uid)      
        
                time = np.arange(0, float(results.get("time_stop")),
                                                     float(results.get("dt")))
        
                data = wavelet.get_amplitude_data(time)
        
                line = cc._main_panel.append_artist("Line2D",
                                                    time,
                                                    data,                         
                                                    linewidth=1,
                                                    color="blue")

                
                cpc = UIM.list('canvas_plotter_controller', cc.uid)[0]
                cpc.figure_titletext = wavelet.name 
                
                xlim = (0, float(results.get("time_stop")))
                cpc.xlim = xlim
                cpc.set_plot_lim("x", xlim)
                
                ylim = (np.min(data), np.max(data))
                cpc.ylim = ylim
                cpc.set_plot_lim("y", ylim)
                
                #
                #
                
                idx = len(data)-1
                segue = True
                for i in range(len(data)-1, -1, -1):
                    print(str(i) + " - " + str(data[i])) 
                    if np.absolute(data[i]) > 0.0000001 and segue:
                        idx = i
                        segue = False

                print("\n\n")
                print("last idx: " + str(len(data)-1))
                print("idx: ", idx)
                print("time: ", time[idx])
                print("\n\n")
                

                
        except Exception as e:
            print ('ERROR [on_create_model]:', str(e))
            raise
            
        finally:
            del wait
            del disableAll
            UIM.remove(dlg.uid)   



    def _open_simulation(self, simulation_uid):
        OM = ObjectManager()
        simulation = OM.get(simulation_uid)    
        model = OM.get(simulation.model_uid)    
        
        UIM = UIManager()      
        
        
        dlg = UIM.create('dialog_controller', title='Plot Simulation')
        #
        ctn_dt = dlg.view.AddCreateContainer('StaticBox', 
                                        label='Max Amplitude', 
                                        orient=wx.VERTICAL, 
                                        proportion=0, 
                                        flag=wx.EXPAND|wx.TOP, border=5)
        dlg.view.AddTextCtrl(ctn_dt, proportion=0, flag=wx.EXPAND|wx.TOP, 
                             border=5, widget_name='vmax', initial=str(simulation.max)) 
        #

        ctn_time_stop = dlg.view.AddCreateContainer('StaticBox', 
                                        label='Min Amplitude', 
                                        orient=wx.VERTICAL, 
                                        proportion=0, 
                                        flag=wx.EXPAND|wx.TOP, border=5)
        dlg.view.AddTextCtrl(ctn_time_stop, proportion=0, flag=wx.EXPAND|wx.TOP, 
                             border=5, widget_name='vmin', initial=str(simulation.min)) 
        #
        
        ctn_interval = dlg.view.AddCreateContainer('StaticBox', 
                                        label='Interval (ms)', 
                                        orient=wx.VERTICAL, 
                                        proportion=0, 
                                        flag=wx.EXPAND|wx.TOP, border=5)
        dlg.view.AddTextCtrl(ctn_interval, proportion=0, flag=wx.EXPAND|wx.TOP, 
                             border=5, widget_name='interval', initial=str(40)) 
        #
    
        ##
        ctn_receiver_1x = dlg.view.AddCreateContainer('StaticBox', 
                                        label='Receiver 1 X', 
                                        orient=wx.VERTICAL, 
                                        proportion=0, 
                                        flag=wx.EXPAND|wx.TOP, border=5)
        dlg.view.AddTextCtrl(ctn_receiver_1x, proportion=0, flag=wx.EXPAND|wx.TOP, 
                             border=5, widget_name='x_rec1') 
        #    
        ctn_receiver_1y = dlg.view.AddCreateContainer('StaticBox', 
                                        label='Receiver 1 Y', 
                                        orient=wx.VERTICAL, 
                                        proportion=0, 
                                        flag=wx.EXPAND|wx.TOP, border=5)
        dlg.view.AddTextCtrl(ctn_receiver_1y, proportion=0, flag=wx.EXPAND|wx.TOP, 
                             border=5, widget_name='y_rec1') 
        #     
        ##
        ctn_receiver_2x = dlg.view.AddCreateContainer('StaticBox', 
                                        label='Receiver 2 X', 
                                        orient=wx.VERTICAL, 
                                        proportion=0, 
                                        flag=wx.EXPAND|wx.TOP, border=5)
        dlg.view.AddTextCtrl(ctn_receiver_2x, proportion=0, flag=wx.EXPAND|wx.TOP, 
                             border=5, widget_name='x_rec2') 
        #    
        ctn_receiver_2y = dlg.view.AddCreateContainer('StaticBox', 
                                        label='Receiver 2 Y', 
                                        orient=wx.VERTICAL, 
                                        proportion=0, 
                                        flag=wx.EXPAND|wx.TOP, border=5)
        dlg.view.AddTextCtrl(ctn_receiver_2y, proportion=0, flag=wx.EXPAND|wx.TOP, 
                             border=5, widget_name='y_rec2') 
        #         

        ##
        ctn_receiver_3x = dlg.view.AddCreateContainer('StaticBox', 
                                        label='Receiver 3 X', 
                                        orient=wx.VERTICAL, 
                                        proportion=0, 
                                        flag=wx.EXPAND|wx.TOP, border=5)
        dlg.view.AddTextCtrl(ctn_receiver_3x, proportion=0, flag=wx.EXPAND|wx.TOP, 
                             border=5, widget_name='x_rec3') 
        #    
        ctn_receiver_3y = dlg.view.AddCreateContainer('StaticBox', 
                                        label='Receiver 3 Y', 
                                        orient=wx.VERTICAL, 
                                        proportion=0, 
                                        flag=wx.EXPAND|wx.TOP, border=5)
        dlg.view.AddTextCtrl(ctn_receiver_3y, proportion=0, flag=wx.EXPAND|wx.TOP, 
                             border=5, widget_name='y_rec3') 
        #     

    
    
    
        dlg.view.SetSize((300, 600))
        result = dlg.view.ShowModal()
        #
        try:
            disableAll = wx.WindowDisabler()
            wait = wx.BusyInfo("Ploting simulation. Wait...")
            if result == wx.ID_OK:
                results = dlg.get_results()          
                print (results)
                
                
                
                
                mwc = wx.GetApp().get_main_window_controller()
                
                
                #sim_plotter = UIM.create('simulationplot_controller', mwc.uid)        
                sim_plotter = UIM.create('testeplot_controller', mwc.uid)   
        
                
        
               #xlim_max, ylim_max = simulation.nx
                # (left, right, bottom, top)
                extent = (0, simulation.nx, simulation.ny, 0)
                
                print("\n\n")
                print(extent)
                print("\n\n")
                
                
                img_base = sim_plotter._main_panel.append_artist("AxesImage", 
                                                      cmap="binary",
                                                      extent=extent)
                
                img_base.set_data(model.data)
                img_base.set_alpha(0.9)
                #self.img_base = main_ax.imshow(vec)
                img_base.set_cmap("Greys")
        
        
        
                sga = SGAnimation(simulation.uid, sim_plotter.uid, 
                                  vmin=float(results.get("vmin")),
                                  vmax=float(results.get("vmax")),
                                  x_rec1=int(results.get("x_rec1")), y_rec1=int(results.get("y_rec1")),
                                  x_rec2=int(results.get("x_rec2")), y_rec2=int(results.get("y_rec2")),
                                  x_rec3=int(results.get("x_rec3")), y_rec3=int(results.get("y_rec3"))
                )
                
                fig = sim_plotter._main_panel.plot_axes.get_figure()
                
                #sec_axes = sim_plotter._main_panel.get_secondary_axes()
                
                
                animation = FuncAnimation(fig, sga, frames=simulation.nt, 
                                          init_func=sga.init_func, 
                                          interval=int(results.get("interval")), 
                                          repeat=True, blit=False
                )
        
        
        
                #cpc = UIM.list('canvas_plotter_controller', sim_plotter.uid)[0]
                
                try:
                    cpc = UIM.list('canvas_plotter_controller', sim_plotter.uid)[0]
                except:
                    cpc = UIM.list('canvas_plotter_controller_jun21', sim_plotter.uid)[0]
                
                
                #cpc.figure_titletext = model.name 
                
                xlim = (0, simulation.nx)
                cpc.xlim = xlim
                cpc.set_plot_lim("x", xlim)
                ylim = (simulation.ny, 0)
                cpc.ylim = ylim
                cpc.set_plot_lim("y", ylim)
                
                print(simulation.nx, simulation.ny)


        except Exception as e:
            print ('ERROR [_open_simulation]:', str(e))
            raise
            
        finally:
            del wait
            del disableAll
            UIM.remove(dlg.uid)   



        # sga = SGAnimation(simulation.uid, cc.uid)
        
        # fig = cc._main_panel.plot_axes.get_figure()
        
        # animation = FuncAnimation(fig, sga, frames=simulation.nt, 
        #                           init_func=sga.init_func, 
        #                           interval=100, 
        #                           repeat=True, blit=False
        # )
        
        
        #cc._main_panel.plot_axes
        
        
        # xlim_max, ylim_max = model.simulation.shape
        # # (left, right, bottom, top)
        # extent = (0, xlim_max, ylim_max, 0)
        
        # print("\n\n")
        # print(extent)
        # print("\n\n")
        
        
        # image = cc._main_panel.append_artist("AxesImage", 
        #                                       cmap="Greys",
        #                                       extent=extent)

        # image.set_data(model.data)
      
        
        # cpc = UIM.list('canvas_plotter_controller', cc.uid)[0]
        # cpc.figure_titletext = model.name 
        
        # xlim = (0, xlim_max)
        # cpc.xlim = xlim
        # cpc.set_plot_lim("x", xlim)
        # ylim = (ylim_max, 0)
        # cpc.ylim = ylim
        # cpc.set_plot_lim("y", ylim)
        
        # print(xlim_max, ylim_max)

        #image.set_label('crossplot_controller')            
        