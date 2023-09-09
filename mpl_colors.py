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
from time import time
from typing import Union, List
import traceback

import littleLogging as logging

class MplColors():

    __COLOR_TABLE_NAMES = \
        {'BASE_COLORS': mcolors.BASE_COLORS,
         'CSS4_COLORS': mcolors.CSS4_COLORS, 
         'TABLEAU_COLORS': mcolors.TABLEAU_COLORS,
         'XKCD_COLORS': mcolors.XKCD_COLORS}
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
        
        fig, ax = plt.subplots(figsize=(MplColors.__COLOR_BAR['length'],
                                        MplColors.__COLOR_BAR['height']))
        colorbar.ColorbarBase(ax, cmap=cmap1, orientation = 'horizontal')
        plt.title(f"Selected named colors: {cmap1.N} colors")
        plt.show()


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
    def display_colormaps(cmap_names: Union[str, List[str]]=[], 
                          ndisplays:int=5) -> None:
        def plot_colormap(cmap_name:str) -> None:
            fig, ax = plt.subplots(figsize=(MplColors.__COLOR_BAR['length'],
                                            MplColors.__COLOR_BAR['height']))
            col_map = plt.get_cmap(cmap_name)
            colorbar.ColorbarBase(ax, cmap=col_map, orientation = 'horizontal')
            plt.title(f"Mapcolor {cmap_name}: {col_map.N} colors")
            plt.show()
    
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
                plot_colormap(cmn1)
        else:
            for i, cmn1 in enumerate(cmaps_names_set):
                if i > 0:
                    if fmod(i, ndisplays) == 0:
                        nremain = i + 1 - ncmaps
                        ans = input(f'\n{nremain} colormaps to be displayed, ' 
                                    'continue (y/n):? ')
                        if ans.lower() != 'y':
                            break
                plot_colormap(cmn1)
    
    
    @staticmethod
    def display_colors_in_colormap(cmap_name:str='hsv', ncolors:int=10, 
                                   correlative:bool=False) ->None:
        cmaps_names_set = [cmn1 for cmn1 in plt.colormaps()]
        if cmap_name not in cmaps_names_set:
            logging.append(f'{cmap_name} is not a valid colormap name. ' 
                           'It continues with hsv instead')
            cmap_name = 'hsv'
        colormap = plt.get_cmap(cmap_name)
        print(f'Colormap {cmap_name}: number of colors {colormap.N}. '
              f'{ncolors} colors are displayed')
        if correlative and ncolors<= colormap.N:
            values = [i for i in range(ncolors)]
        else:
            values = np.linspace(0, 1, ncolors)  
        
        # Map the numerical values to colors in the colormap
        colors = [colormap(value) for value in values]
        
        print('Color codes. Formats: RGBA, hex. RGBA')
        for color in colors:
            hex_code = mcolors.to_hex(color, keep_alpha=True)
            print(f'{color}, {hex_code}')
        
        # Plot a bar chart using the colors
        plt.bar(range(len(colors)), [1] * len(colors), color=colors)
        plt.show()

        
    @staticmethod
    def color_names_get(color_table: str='tableau', hex_code: bool=False) -> []:


        if color_table.lower() == 'base':
            colors = mcolors.BASE_COLORS
        elif color_table.lower() == 'css4':
            colors = mcolors.CSS4_COLORS
        elif color_table.lower() == 'tableau':
            colors = mcolors.TABLEAU_COLORS
        else:
            colors = mcolors.BASE_COLORS

        if hex_code:
            if color_table.lower() == 'base':
                return [(k, mcolors.to_hex(v)) for k, v in colors.items()]
            else:
                return [(k, v) for k, v in colors.items()]
        else:
            return [k for k in colors]

        
    @staticmethod
    def get_color_table_names():
        return MplColors.__COLOR_TABLE_NAMES.keys()


if __name__ == "__main__":

    startTime = time()

    try:

        mplc = MplColors()
        mplc.display_named_colors() 

    except Exception:
        msg = traceback.format_exc()
        logging.append(msg)
    finally:
        logging.dump()
        xtime = time() - startTime
        print(f'El script tardó {xtime:0.1f} s')

        