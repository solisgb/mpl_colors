# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 11:03:50 2023

@author: solis
"""
import matplotlib.colors as mcolors
from matplotlib.colors import ListedColormap
from matplotlib import colorbar
import matplotlib.pyplot as plt
from math import fmod
import numpy as np
from typing import Union, List

import littleLogging as logging

class MplColors():

    __COLOR_TABLE_NAMES = \
        {'base': mcolors.BASE_COLORS,
         'css4': mcolors.CSS4_COLORS, 
         'tableau': mcolors.TABLEAU_COLORS,
         'xkcd': mcolors.XKCD_COLORS}
    __COLOR_BAR = {'height': 0.5, 'length': 9}
    __RGB_COLORS = ['red', 'green', 'blue']
    
    def __init__(self):
        pass
    
    
    @staticmethod
    def display_all_named_colors(sorted_by_name:bool=True) -> None:
        named_colors = mcolors.cnames
        # Order tht dictionay by code color
        if not sorted_by_name:
            sorted_by = 'hex RGB color code'
            sorted_items = sorted(named_colors.items(), key=lambda x: x[1])
            # Create a new dictionary from the sorted list
            sorted_dict = dict(sorted_items)
            # Convert the color names into valid color specifications
            color_list = list(sorted_dict.values())
        else:
            sorted_by = 'color name'
            color_list = list(named_colors.values())
        
        # Create a ListedColormap using the color list
        cmap1 = ListedColormap(color_list)
        
        fig, ax = plt.subplots(figsize=(MplColors.__COLOR_BAR['length'],
                                        MplColors.__COLOR_BAR['height']))
        colorbar.ColorbarBase(ax, cmap=cmap1, orientation = 'horizontal')
        plt.title(f" Named colors: {cmap1.N} colors. Order: {sorted_by}")
        plt.show()

    
    @staticmethod
    def display_some_named_colors(color_names:[str]=__RGB_COLORS) -> None:
        named_colors = mcolors.cnames
        valid_colors_names = [cn1 for cn1 in color_names if cn1 in named_colors.keys()]
        if not valid_colors_names:
            logging.append('Not valid colors names')
            return
        else:
            if len(valid_colors_names) != len(color_names):
                logging.append('Some colors in colors_names are not valid')

        colors_dict = {key: named_colors[key] for key in valid_colors_names}
        print('Selected colors')
        for k, v in colors_dict.items():
            print(f'{k}, {v}')
        
        color_list = list(colors_dict.values())
        cmap1 = ListedColormap(color_list)
        title = f"Selected named colors: {cmap1.N} colors"
        MplColors.fig_colorbar_cmap(cmap1, title)


    @staticmethod
    def get_colormaps_names(ordered:bool=True) -> None:
        cmaps_names = [cmn1 for cmn1 in plt.colormaps()]
        if ordered:
            cmaps_names.sort()
        return cmaps_names
    
    
    @staticmethod
    def print_colormaps_names(cmap_line:int=5) -> None:
        cmaps_names = [f'{cmn1}: {plt.get_cmap(cmn1).N} colors' \
                       for cmn1 in plt.colormaps()]
        cmaps_names.sort()
        n = len(cmaps_names)
        for i in range(0, n, cmap_line):
            print(", ".join(cmaps_names[i:i+cmap_line]))

    
    @staticmethod
    def fig_colorbar_cmap(col_map:mcolors.LinearSegmentedColormap,
                      title:str) -> None:
        fig, ax = plt.subplots(figsize=(MplColors.__COLOR_BAR['length'],
                                        MplColors.__COLOR_BAR['height']))
        colorbar.ColorbarBase(ax, cmap=col_map, orientation = 'horizontal')
        plt.title(title)
        plt.show()

    
    @staticmethod
    def display_colormaps(cmap_names: Union[str, List[str]]=[], 
                          ndisplays:int=5) -> None:
    
        if cmap_names:
            if isinstance(cmap_names, str):
                cmap_names = [cmap_names]
    
        cmaps_names_set = [cmn1 for cmn1 in plt.colormaps()]
        cmaps_names_set.sort()
        ncmaps = len(cmaps_names_set)
    
        if cmap_names:
            valid_cmap_names = [cmn1 for cmn1 in cmap_names \
                                if cmn1 in cmaps_names_set]
            for cmn1 in valid_cmap_names:
                col_map = plt.get_cmap(cmn1)
                title = f"Colormap {cmn1}: {col_map.N} colors"
                MplColors.fig_colorbar_cmap(col_map, title)                
        else:
            for i, cmn1 in enumerate(cmaps_names_set):
                if i > 0:
                    if fmod(i, ndisplays) == 0:
                        nremain = i + 1 - ncmaps
                        ans = input(f'\n{nremain} colormaps to be displayed, ' 
                                    'continue (y/n):? ')
                        if ans.lower() != 'y':
                            break
                col_map = plt.get_cmap(cmn1)
                title = f"Colormap {cmn1}: {col_map.N} colors"
                MplColors.fig_colorbar_cmap(col_map, title)

    
    @staticmethod
    def display_colors_in_colormap\
        (cmap_name:str='hsv', ncolors:int=10) -> None:
        cmaps_names_set = [cmn1 for cmn1 in plt.colormaps()]
        if cmap_name not in cmaps_names_set:
            logging.append(f'{cmap_name} is not a valid colormap name. ' 
                           'It continues with hsv instead')
            cmap_name = 'hsv'
        colormap = plt.get_cmap(cmap_name)
        print(f'Colormap {cmap_name}: number of colors {colormap.N}. '
              f'{ncolors} colors are displayed')
        
        values = np.linspace(0, 1, ncolors)  
        
        # Map the numerical values to colors in the colormap
        colors = [colormap(value) for value in values]
        
        print('Color codes. Formats: RGBA, hex. RGBA')
        for color in colors:
            hex_code = mcolors.to_hex(color, keep_alpha=True)
            print(f'{color}, {hex_code}')

        cmap = ListedColormap(colors)
        title = f'Selected colors in colormap {cmap_name}'
        MplColors.fig_colorbar_cmap(cmap, title)

    
    @staticmethod
    def get_colors_in_colormap\
        (cmap_name:str, indexes: Union[int, slice]) ->None:
        cmaps_names_set = [cmn1 for cmn1 in plt.colormaps()]
        if cmap_name not in cmaps_names_set:
            logging.append(f'{cmap_name} is not a valid colormap name. ' 
                           'It continues with hsv instead')
            cmap_name = 'hsv'
        cmap = plt.get_cmap(cmap_name)
        print(f'Colormap {cmap_name}: number of colors {cmap.N}.')

        unique_indexes = set()
    
        for index in indexes:
            if isinstance(index, int):  # Check if it's an integer index
                if index not in unique_indexes:
                    unique_indexes.add(index)
            elif isinstance(index, slice):  # Check if it's a slice object
                start = index.start if index.start is not None else 0
                stop = index.stop if index.stop is not None else cmap.N
                step = index.step if index.step is not None else 1
                
                for i in range(start, stop, step):
                    if i not in unique_indexes:
                        unique_indexes.add(i)

        colors = [cmap(i) for i in unique_indexes]
        
        print('Color codes. Formats: RGBA, hex. RGBA')
        for color, i in zip(colors, unique_indexes):
            hex_code = mcolors.to_hex(color, keep_alpha=True)
            print(f'{i}, {hex_code}')

        cmap = ListedColormap(colors)
        title = f'Selected colors in colormap {cmap_name}'
        MplColors.fig_colorbar_cmap(cmap, title)


    @staticmethod
    def get_color_table_names():
        return MplColors.__COLOR_TABLE_NAMES.keys()

        
    @staticmethod
    def display_color_tables\
        (ctable_names: Union[str, List[str]]=[]) -> []:
        
        if not isinstance(ctable_names, (str, list)):
            logging.append('ctable_names must be of type str or [str]')
            return
        
        if isinstance(ctable_names, str):
            ctable_names = [ctable_names]
        
        table_names_set = MplColors.get_color_table_names()
        
        if ctable_names:
            valid_ctable_names = [ctn1 for ctn1 in ctable_names \
                if ctn1 in table_names_set]
        else:
            valid_ctable_names = table_names_set
        
        if not valid_ctable_names:
            logging.append('ctable_names does not have valid names, '
                           'all table colors are used instead')
        
        print('Number of colors in the color tables')
        for tcn1 in valid_ctable_names:
            colors_dict = MplColors.__COLOR_TABLE_NAMES[tcn1]
            color_names = [key for key in colors_dict]            
            print(f'Color table {tcn1}. Number of colors {len(color_names)}')
        
        for tcn1 in valid_ctable_names:
            colors_dict = MplColors.__COLOR_TABLE_NAMES[tcn1]
       
            color_list = list(colors_dict.values())
            cmap1 = ListedColormap(color_list)
            title = f"Color table {tcn1}: {cmap1.N} colors"
            MplColors.fig_colorbar_cmap(cmap1, title)

    
    @staticmethod
    def display_colors_in_color_table\
        (ctable_name:str='tableau', ncolors:int=10) -> None:
        table_names_set = MplColors.get_color_table_names()
        if ctable_name not in table_names_set:
            logging.append(f'{ctable_name} is not a valid table color name. ' 
                           'It continues with tableau instead')
            ctable_name = 'tableau'
        colors_dict = MplColors.__COLOR_TABLE_NAMES[ctable_name]
        colors_dict_keys = list(colors_dict.keys())
        colors_dict_values = [v1.lower() for v1 in colors_dict.values()]
        cmap1 = ListedColormap(colors_dict_values)            
            
        print(f'Color table {ctable_name}: number of colors {cmap1.N}. '
              f'{ncolors} colors are displayed')

        values = np.linspace(0, 1, ncolors)  
        
        # Map the numerical values to colors in the colormap
        colors = [cmap1(value) for value in values]
        hex_colors = [mcolors.to_hex(clr1, keep_alpha=False) for clr1 in colors]        
        indexes = [colors_dict_values.index(clr1) for clr1 in hex_colors]
        keys = [colors_dict_keys[i] for i in indexes]
        cmap1 = ListedColormap(colors)
        
        print('Color codes. Formats: hex RGBA, hex. RGBA')
        for key, hclr1 in zip(keys, hex_colors):
            print(f'{key}, {hclr1}')

        title = f'Selected colors in color table {ctable_name}'
        MplColors.fig_colorbar_cmap(cmap1, title)
