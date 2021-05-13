# -*- coding: utf-8 -*-
"""
Created on Thu May 13 13:11:27 2021

@author: Adriano
"""

import wx

from collections import OrderedDict


# Have colormaps separated into categories:
# http://matplotlib.org/examples/color/colormaps_reference.html
"""
# MPL 1.4/1.5 COLORS

MPL_CATS_CMAPS = [('Perceptually Uniform Sequential', [
            'viridis', 'plasma', 'inferno', 'magma']),
         ('Sequential', [
            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']),
         ('Sequential (2)', [
            'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
            'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
            'hot', 'afmhot', 'gist_heat', 'copper']),
         ('Diverging', [
            'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
            'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']),
         ('Qualitative', [
            'Pastel1', 'Pastel2', 'Paired', 'Accent',
            'Dark2', 'Set1', 'Set2', 'Set3',
            'tab10', 'tab20', 'tab20b', 'tab20c']),
         ('Miscellaneous', [
            'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
            'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'hsv',
            'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar'])]
"""

# MPL 2.0 COLORS
MPL_CATS_CMAPS = [
            ('Perceptually Uniform Sequential', 
                 ['viridis', 'inferno', 'plasma', 'magma']
            ),
            ('Sequential', 
                 ['Blues', 'BuGn', 'BuPu', 'GnBu', 'Greens', 'Greys', 
                  'Oranges', 'OrRd', 'PuBu', 'PuBuGn', 'PuRd', 'Purples', 
                  'RdPu', 'Reds', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd'
                 ]
            ),
            ('Sequential (2)', 
                 ['afmhot', 'autumn', 'bone', 'cool', 'copper', 'gist_heat', 
                  'gray', 'hot', 'pink', 'spring', 'summer', 'winter'
                 ]
            ),
            ('Diverging', 
                 ['BrBG', 'bwr', 'coolwarm', 'PiYG', 'PRGn', 'PuOr',
                  'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral', 'seismic'
                 ]
            ),
            ('Qualitative', 
                 ['Accent', 'Dark2', 'Paired', 'Pastel1', 'Pastel2', 'Set1', 
                  'Set2', 'Set3', 'Vega10', 'Vega20', 'Vega20b', 'Vega20c'
                 ]
            ),
            ('Miscellaneous', 
                 ['gist_earth', 'terrain', 'ocean', 'gist_stern', 'brg', 
                  'CMRmap', 'cubehelix', 'gnuplot', 'gnuplot2', 'gist_ncar',
                  'nipy_spectral', 'jet', 'rainbow', 'gist_rainbow', 'hsv', 
                  'flag', 'prism'
                  ]
            )
]
    
    
    
#MPL_COLORMAPS = [value for (key, values) in MPL_CATS_CMAPS for value in values]


#MPL_COLORMAPS = sorted(cmap_d)

#"""
MPL_COLORMAPS = ['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 
                 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r',
                 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 
                 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r',
                 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r',
                 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBu_r',
                 'PuBuGn', 'PuBuGn_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r',
                 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 
                 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r',
                 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 
                 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Vega10', 'Vega10_r',
                 'Vega20', 'Vega20_r', 'Vega20b', 'Vega20b_r', 'Vega20c', 'Vega20c_r',
                 'Wistia', 'Wistia_r', 'YlGn', 'YlGn_r', 'YlGnBu', 'YlGnBu_r',
                  'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 
                  'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r',
                  'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 
                  'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r',
                  'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 
                  'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r',
                  'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r',
                  'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r',
                  'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r',
                  'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r',
                  'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 
                  'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 
                  'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 
                  'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 
                  'spectral', 'spectral_r', 'spring', 'spring_r', 
                  'summer', 'summer_r', 'terrain', 'terrain_r', 
                  'viridis', 'viridis_r', 'winter', 'winter_r']
  
#"""

###############################################################################
###############################################################################  

MPL_COLORS = OrderedDict()
MPL_COLORS['Black'] = None
MPL_COLORS['Maroon'] = None
MPL_COLORS['Green'] = wx.Colour(0, 100, 0) # Dark Green
MPL_COLORS['Olive'] = wx.Colour(128, 128, 0)
MPL_COLORS['Navy'] = None
MPL_COLORS['Purple'] = None
MPL_COLORS['Teal'] = wx.Colour(0, 128, 128)
MPL_COLORS['Gray'] = None
MPL_COLORS['Silver'] = wx.Colour(192, 192, 192)
MPL_COLORS['Red'] = None
MPL_COLORS['Lime'] = wx.Colour(0, 255, 0) # Green
MPL_COLORS['Yellow'] = None
MPL_COLORS['Blue'] = None
MPL_COLORS['Fuchsia'] = wx.Colour(255, 0, 255)
MPL_COLORS['Aqua'] = wx.Colour(0, 255, 255)
MPL_COLORS['White'] = None
MPL_COLORS['SkyBlue'] = wx.Colour(135, 206, 235)
MPL_COLORS['LightGray'] = wx.Colour(211, 211, 211)
MPL_COLORS['DarkGray'] = wx.Colour(169, 169, 169)
MPL_COLORS['SlateGray'] = wx.Colour(112, 128, 144)
MPL_COLORS['DimGray'] = wx.Colour(105, 105, 105)
MPL_COLORS['BlueViolet'] = wx.Colour(138, 43, 226)
MPL_COLORS['DarkViolet'] = wx.Colour(148, 0, 211)
MPL_COLORS['Magenta'] = None
MPL_COLORS['DeepPink'] = wx.Colour(148, 0, 211)
MPL_COLORS['Brown'] = None
MPL_COLORS['Crimson'] = wx.Colour(220, 20, 60)
MPL_COLORS['Firebrick'] = None
MPL_COLORS['DarkRed'] = wx.Colour(139, 0, 0)
MPL_COLORS['DarkSlateGray'] = wx.Colour(47, 79, 79)
MPL_COLORS['DarkSlateBlue'] = wx.Colour(72, 61, 139)
MPL_COLORS['Wheat'] = None
MPL_COLORS['BurlyWood'] = wx.Colour(222, 184, 135)
MPL_COLORS['Tan'] = None
MPL_COLORS['Gold'] = None
MPL_COLORS['Orange'] = None
MPL_COLORS['DarkOrange'] = wx.Colour(255, 140, 0)
MPL_COLORS['Coral'] = None
MPL_COLORS['DarkKhaki'] = wx.Colour(189, 183, 107)
MPL_COLORS['GoldenRod'] = None
MPL_COLORS['DarkGoldenrod'] = wx.Colour(184, 134, 11)
MPL_COLORS['Chocolate'] = wx.Colour(210, 105, 30)
MPL_COLORS['Sienna'] = None
MPL_COLORS['SaddleBrown'] = wx.Colour(139, 69, 19)
MPL_COLORS['GreenYellow'] = wx.Colour(173, 255, 47)
MPL_COLORS['Chartreuse'] = wx.Colour(127, 255, 0)
MPL_COLORS['SpringGreen'] = wx.Colour(0, 255, 127)
MPL_COLORS['MediumSpringGreen'] = wx.Colour(0, 250, 154)
MPL_COLORS['MediumAquamarine'] = wx.Colour(102, 205, 170)
MPL_COLORS['LimeGreen'] = wx.Colour(50, 205, 50)
MPL_COLORS['LightSeaGreen'] = wx.Colour(32, 178, 170)
MPL_COLORS['MediumSeaGreen'] = wx.Colour(60, 179, 113)
MPL_COLORS['DarkSeaGreen'] = wx.Colour(143, 188, 143)
MPL_COLORS['SeaGreen'] = wx.Colour(46, 139, 87)
MPL_COLORS['ForestGreen'] = wx.Colour(34, 139, 34)
MPL_COLORS['DarkOliveGreen'] = wx.Colour(85, 107, 47)
MPL_COLORS['DarkGreen'] = wx.Colour(1, 50, 32)
MPL_COLORS['LightCyan'] = wx.Colour(224, 255, 255)
MPL_COLORS['Thistle'] = None
MPL_COLORS['PowderBlue'] = wx.Colour(176, 224, 230)
MPL_COLORS['LightSteelBlue'] = wx.Colour(176, 196, 222)
MPL_COLORS['LightSkyBlue'] = wx.Colour(135, 206, 250)
MPL_COLORS['MediumTurquoise'] = wx.Colour(72, 209, 204)
MPL_COLORS['Turquoise'] = None
MPL_COLORS['DarkTurquoise'] = wx.Colour(0, 206, 209)
MPL_COLORS['DeepSkyBlue'] = wx.Colour(0, 191, 255)
MPL_COLORS['DodgerBlue'] = wx.Colour(30, 144, 255)
MPL_COLORS['CornflowerBlue'] = wx.Colour(100, 149, 237)
MPL_COLORS['CadetBlue'] = wx.Colour(95, 158, 160)
MPL_COLORS['DarkCyan'] = wx.Colour(0, 139, 139)
MPL_COLORS['SteelBlue'] = wx.Colour(70, 130, 180)
MPL_COLORS['RoyalBlue'] = wx.Colour(65, 105, 225)
MPL_COLORS['SlateBlue'] = wx.Colour(106, 90, 205)
MPL_COLORS['DarkBlue'] = wx.Colour(0, 0, 139)
MPL_COLORS['MediumBlue'] = wx.Colour(0, 0, 205)
MPL_COLORS['SandyBrown'] = wx.Colour(244, 164, 96)
MPL_COLORS['DarkSalmon'] = wx.Colour(233, 150, 122)
MPL_COLORS['Salmon'] = None
MPL_COLORS['Tomato'] = wx.Colour(255, 99, 71) 
MPL_COLORS['Violet'] = wx.Colour(238, 130, 238)
MPL_COLORS['HotPink'] = wx.Colour(255, 105, 180)
MPL_COLORS['RosyBrown'] = wx.Colour(188, 143, 143)
MPL_COLORS['MediumVioletRed'] = wx.Colour(199, 21, 133)
MPL_COLORS['DarkMagenta'] = wx.Colour(139, 0, 139)
MPL_COLORS['DarkOrchid'] = wx.Colour(153, 50, 204)
MPL_COLORS['Indigo'] = wx.Colour(75, 0, 130)
MPL_COLORS['MidnightBlue'] = wx.Colour(25, 25, 112)
MPL_COLORS['MediumSlateBlue'] = wx.Colour(123, 104, 238)
MPL_COLORS['MediumPurple'] = wx.Colour(147, 112, 219)
MPL_COLORS['MediumOrchid'] = wx.Colour(186, 85, 211) 

MPL_COLORS = OrderedDict(sorted(MPL_COLORS.items()))

###############################################################################
###############################################################################        

# Based on https://matplotlib.org/3.1.0/gallery/lines_bars_and_markers/linestyles.html
# 10/September/2019 - Adriano Santana

MPL_LINESTYLES = OrderedDict()
MPL_LINESTYLES['Solid'] = (0, ())
MPL_LINESTYLES['Dotted'] = (0, (1, 1))
MPL_LINESTYLES['Loosely dotted'] = (0, (1, 10))
MPL_LINESTYLES['Densely dotted'] = (0, (1, 1))
MPL_LINESTYLES['Dashed'] = (0, (5, 5))
MPL_LINESTYLES['Loosely dashed'] = (0, (5, 10))
MPL_LINESTYLES['Densely dashed'] = (0, (5, 1))
MPL_LINESTYLES['Dashdotted'] = (0, (3, 5, 1, 5))
MPL_LINESTYLES['Loosely dashdotted'] = (0, (3, 10, 1, 10))
MPL_LINESTYLES['Densely dashdotted'] = (0, (3, 1, 1, 1))
MPL_LINESTYLES['Dashdotdotted'] = (0, (3, 5, 1, 5, 1, 5))
MPL_LINESTYLES['Loosely dashdotdotted'] = (0, (3, 10, 1, 10, 1, 10))
MPL_LINESTYLES['Densely dashdotdotted'] = (0, (3, 1, 1, 1, 1, 1))
